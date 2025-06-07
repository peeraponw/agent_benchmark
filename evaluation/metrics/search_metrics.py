"""
Web search evaluation metrics.

This module provides specialized metrics for evaluating web search integration
including source credibility, information freshness, and query-answer relevance.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Union
from urllib.parse import urlparse
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .base_metrics import BaseMetric, MetricResult, safe_divide


class SourceCredibilityMetric(BaseMetric):
    """
    Source credibility metric for web search results.
    
    Evaluates the credibility of sources based on domain reputation and content indicators.
    """
    
    def __init__(self):
        super().__init__(
            name="SourceCredibility",
            description="Credibility score based on domain reputation and content quality indicators"
        )
        
        # Define credible domain patterns and high-credibility domains
        self.high_credibility_domains = {
            'edu', 'gov', 'org'  # Educational, government, and organization domains
        }
        
        self.credible_domains = {
            'wikipedia.org', 'britannica.com', 'nature.com', 'science.org',
            'pubmed.ncbi.nlm.nih.gov', 'scholar.google.com', 'arxiv.org',
            'reuters.com', 'bbc.com', 'npr.org', 'pbs.org'
        }
        
        self.low_credibility_indicators = {
            'blog', 'forum', 'social', 'wiki', 'user-generated'
        }
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate source credibility score.
        
        Args:
            expected: Not used for this metric
            actual: List of sources/URLs or source information
            **kwargs: Additional parameters like 'source_metadata'
            
        Returns:
            MetricResult with credibility score
        """
        sources = self._normalize_sources(actual)
        
        if not sources:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "No sources provided"}
            )
        
        credibility_scores = []
        source_details = []
        
        for source in sources:
            score, details = self._evaluate_source_credibility(source)
            credibility_scores.append(score)
            source_details.append(details)
        
        # Calculate overall credibility as weighted average
        # Give more weight to higher-scoring sources
        weights = np.array(credibility_scores)
        if np.sum(weights) > 0:
            overall_score = np.average(credibility_scores, weights=weights)
        else:
            overall_score = 0.0
        
        return MetricResult(
            name=self.name,
            score=overall_score,
            metadata={
                "individual_scores": credibility_scores,
                "source_details": source_details,
                "num_sources": len(sources),
                "avg_score": np.mean(credibility_scores) if credibility_scores else 0.0
            }
        )
    
    def _normalize_sources(self, sources: Any) -> List[str]:
        """Normalize sources to list of strings."""
        if isinstance(sources, str):
            # Try to extract URLs from text
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sources)
            return urls if urls else [sources]
        elif isinstance(sources, (list, tuple)):
            return [str(source) for source in sources]
        else:
            return [str(sources)]
    
    def _evaluate_source_credibility(self, source: str) -> tuple[float, Dict[str, Any]]:
        """Evaluate credibility of a single source."""
        details = {"source": source, "factors": []}
        score = 0.5  # Base score
        
        # Check if it's a URL
        if source.startswith(('http://', 'https://')):
            parsed_url = urlparse(source)
            domain = parsed_url.netloc.lower()
            
            # Remove 'www.' prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            details["domain"] = domain
            
            # Check domain credibility
            domain_parts = domain.split('.')
            tld = domain_parts[-1] if domain_parts else ''
            
            if tld in self.high_credibility_domains:
                score += 0.3
                details["factors"].append(f"High credibility TLD: {tld}")
            
            if domain in self.credible_domains:
                score += 0.4
                details["factors"].append(f"Known credible domain: {domain}")
            
            # Check for low credibility indicators
            for indicator in self.low_credibility_indicators:
                if indicator in domain.lower():
                    score -= 0.2
                    details["factors"].append(f"Low credibility indicator: {indicator}")
            
            # Check for HTTPS
            if source.startswith('https://'):
                score += 0.1
                details["factors"].append("Secure HTTPS connection")
            
        else:
            # Non-URL source, evaluate based on content
            source_lower = source.lower()
            
            # Check for academic or official indicators
            academic_indicators = ['university', 'institute', 'research', 'study', 'journal', 'publication']
            for indicator in academic_indicators:
                if indicator in source_lower:
                    score += 0.2
                    details["factors"].append(f"Academic indicator: {indicator}")
                    break
            
            # Check for low credibility indicators
            for indicator in self.low_credibility_indicators:
                if indicator in source_lower:
                    score -= 0.2
                    details["factors"].append(f"Low credibility indicator: {indicator}")
        
        # Ensure score is in [0, 1] range
        score = max(0.0, min(1.0, score))
        details["final_score"] = score
        
        return score, details


class InformationFreshnessMetric(BaseMetric):
    """
    Information freshness metric for web search results.
    
    Evaluates how recent and up-to-date the information is.
    """
    
    def __init__(self, max_age_days: int = 365):
        """
        Initialize information freshness metric.
        
        Args:
            max_age_days: Maximum age in days for information to be considered fresh
        """
        super().__init__(
            name="InformationFreshness",
            description=f"Information freshness with max age of {max_age_days} days"
        )
        self.max_age_days = max_age_days
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate information freshness score.
        
        Args:
            expected: Expected publication date or recency requirement
            actual: Actual publication dates or content with dates
            **kwargs: Additional parameters like 'query_date'
            
        Returns:
            MetricResult with freshness score
        """
        query_date = kwargs.get('query_date', datetime.now())
        if isinstance(query_date, str):
            query_date = datetime.fromisoformat(query_date.replace('Z', '+00:00'))
        
        dates = self._extract_dates(actual)
        
        if not dates:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "No dates found in content"}
            )
        
        freshness_scores = []
        date_details = []
        
        for date in dates:
            score, details = self._calculate_date_freshness(date, query_date)
            freshness_scores.append(score)
            date_details.append(details)
        
        # Use the best (most recent) freshness score
        overall_score = max(freshness_scores) if freshness_scores else 0.0
        
        return MetricResult(
            name=self.name,
            score=overall_score,
            metadata={
                "individual_scores": freshness_scores,
                "date_details": date_details,
                "query_date": query_date.isoformat(),
                "max_age_days": self.max_age_days,
                "best_score": overall_score
            }
        )
    
    def _extract_dates(self, content: Any) -> List[datetime]:
        """Extract dates from content."""
        dates = []
        content_str = str(content)
        
        # Common date patterns
        date_patterns = [
            r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b',  # YYYY-MM-DD
            r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',  # MM/DD/YYYY
            r'\b(\d{1,2})-(\d{1,2})-(\d{4})\b',  # MM-DD-YYYY
            r'\b(\w+)\s+(\d{1,2}),?\s+(\d{4})\b'  # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, content_str)
            for match in matches:
                try:
                    if len(match) == 3:
                        if pattern.endswith(r'(\d{4})\b'):  # YYYY-MM-DD
                            year, month, day = int(match[0]), int(match[1]), int(match[2])
                        elif 'w+' in pattern:  # Month DD, YYYY
                            month_name, day, year = match[0], int(match[1]), int(match[2])
                            month = self._month_name_to_number(month_name)
                            if month == 0:
                                continue
                        else:  # MM/DD/YYYY or MM-DD-YYYY
                            month, day, year = int(match[0]), int(match[1]), int(match[2])
                        
                        date = datetime(year, month, day)
                        dates.append(date)
                except (ValueError, TypeError):
                    continue
        
        return dates
    
    def _month_name_to_number(self, month_name: str) -> int:
        """Convert month name to number."""
        months = {
            'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
            'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6,
            'july': 7, 'jul': 7, 'august': 8, 'aug': 8, 'september': 9, 'sep': 9,
            'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
        }
        return months.get(month_name.lower(), 0)
    
    def _calculate_date_freshness(self, date: datetime, query_date: datetime) -> tuple[float, Dict[str, Any]]:
        """Calculate freshness score for a single date."""
        age_days = (query_date - date).days
        
        details = {
            "date": date.isoformat(),
            "age_days": age_days,
            "query_date": query_date.isoformat()
        }
        
        if age_days < 0:
            # Future date, treat as very fresh
            score = 1.0
            details["note"] = "Future date"
        elif age_days <= self.max_age_days:
            # Linear decay from 1.0 to 0.0 over max_age_days
            score = 1.0 - (age_days / self.max_age_days)
            details["note"] = "Within freshness window"
        else:
            # Too old
            score = 0.0
            details["note"] = "Exceeds maximum age"
        
        details["freshness_score"] = score
        return score, details


class QueryAnswerRelevanceMetric(BaseMetric):
    """
    Query-answer relevance metric for web search results.
    
    Measures how well the search results answer the original query.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize query-answer relevance metric.
        
        Args:
            model_name: Sentence transformer model for similarity calculation
        """
        super().__init__(
            name="QueryAnswerRelevance",
            description=f"Query-answer relevance using {model_name}"
        )
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy load the sentence transformer model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate query-answer relevance score.
        
        Args:
            expected: Original query/question
            actual: Search results or answer content
            **kwargs: Additional parameters
            
        Returns:
            MetricResult with relevance score
        """
        query = str(expected).strip()
        content = str(actual).strip()
        
        if not query or not content:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "Empty query or content"}
            )
        
        # Split content into chunks for analysis
        content_chunks = self._split_content(content)
        
        # Calculate relevance for each chunk
        relevance_scores = []
        for chunk in content_chunks:
            embeddings = self.model.encode([query, chunk])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            relevance_scores.append(max(0.0, similarity))
        
        # Use maximum relevance as the overall score
        max_relevance = max(relevance_scores) if relevance_scores else 0.0
        avg_relevance = np.mean(relevance_scores) if relevance_scores else 0.0
        
        return MetricResult(
            name=self.name,
            score=max_relevance,
            metadata={
                "max_relevance": max_relevance,
                "avg_relevance": avg_relevance,
                "num_chunks": len(relevance_scores),
                "chunk_scores": relevance_scores,
                "query_length": len(query),
                "content_length": len(content)
            }
        )
    
    def _split_content(self, content: str, max_chunk_size: int = 500) -> List[str]:
        """Split content into smaller chunks for analysis."""
        if len(content) <= max_chunk_size:
            return [content]
        
        # Split by paragraphs first, then sentences
        paragraphs = content.split('\n\n')
        chunks = []
        
        for paragraph in paragraphs:
            if len(paragraph) <= max_chunk_size:
                chunks.append(paragraph)
            else:
                # Split long paragraphs by sentences
                sentences = re.split(r'[.!?]+', paragraph)
                current_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(current_chunk) + len(sentence) <= max_chunk_size:
                        current_chunk += sentence + ". "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + ". "
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content]


class SearchMetrics:
    """
    Comprehensive web search evaluation metrics suite.
    
    Combines multiple metrics for thorough evaluation of web search integration.
    """
    
    def __init__(self,
                 include_credibility: bool = True,
                 include_freshness: bool = True,
                 include_relevance: bool = True,
                 semantic_model: str = "all-MiniLM-L6-v2",
                 max_age_days: int = 365):
        """
        Initialize search metrics suite.
        
        Args:
            include_credibility: Whether to include source credibility
            include_freshness: Whether to include information freshness
            include_relevance: Whether to include query-answer relevance
            semantic_model: Model name for semantic similarity calculations
            max_age_days: Maximum age for freshness calculation
        """
        self.metrics = {}
        
        if include_credibility:
            self.metrics['credibility'] = SourceCredibilityMetric()
        
        if include_freshness:
            self.metrics['freshness'] = InformationFreshnessMetric(max_age_days)
        
        if include_relevance:
            self.metrics['relevance'] = QueryAnswerRelevanceMetric(semantic_model)
    
    def evaluate(self, 
                 query: str,
                 search_results: List[Dict[str, Any]],
                 answer: str = None) -> Dict[str, MetricResult]:
        """
        Evaluate web search results.
        
        Args:
            query: Original search query
            search_results: List of search result dictionaries with 'url', 'content', 'date' etc.
            answer: Generated answer based on search results (optional)
            
        Returns:
            Dictionary of metric results
        """
        results = {}
        
        # Extract sources and content from search results
        sources = [result.get('url', '') for result in search_results]
        content = '\n\n'.join([result.get('content', '') for result in search_results])
        dates = [result.get('date', '') for result in search_results]
        
        # Evaluate source credibility
        if 'credibility' in self.metrics:
            results['credibility'] = self.metrics['credibility'].calculate(None, sources)
        
        # Evaluate information freshness
        if 'freshness' in self.metrics:
            results['freshness'] = self.metrics['freshness'].calculate(None, dates)
        
        # Evaluate query-answer relevance
        if 'relevance' in self.metrics:
            evaluation_content = answer if answer else content
            results['relevance'] = self.metrics['relevance'].calculate(query, evaluation_content)
        
        return results
