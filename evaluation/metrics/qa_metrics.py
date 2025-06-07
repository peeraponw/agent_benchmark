"""
Question-Answering evaluation metrics.

This module provides specialized metrics for evaluating Q&A systems including
BLEU score, ROUGE score, semantic similarity, and factual accuracy checking.
"""

import re
import nltk
from typing import Any, Dict, List, Optional, Set
from collections import Counter
import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .base_metrics import BaseMetric, MetricResult, TextSimilarityMetric, safe_divide

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class BLEUMetric(TextSimilarityMetric):
    """
    BLEU (Bilingual Evaluation Understudy) score for text similarity.
    
    Measures n-gram overlap between expected and actual text with brevity penalty.
    """
    
    def __init__(self, max_n: int = 4, case_sensitive: bool = False):
        """
        Initialize BLEU metric.
        
        Args:
            max_n: Maximum n-gram size to consider
            case_sensitive: Whether to perform case-sensitive comparison
        """
        super().__init__(
            name="BLEU",
            description=f"BLEU score with n-grams up to {max_n}",
            case_sensitive=case_sensitive
        )
        self.max_n = max_n
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate BLEU score between expected and actual text.
        
        Args:
            expected: Expected/reference text
            actual: Actual/candidate text
            
        Returns:
            MetricResult with BLEU score
        """
        expected_text = self.preprocess_text(str(expected))
        actual_text = self.preprocess_text(str(actual))
        
        expected_tokens = expected_text.split()
        actual_tokens = actual_text.split()
        
        if not actual_tokens:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "Empty actual text"}
            )
        
        # Calculate n-gram precisions
        precisions = []
        for n in range(1, self.max_n + 1):
            expected_ngrams = self._get_ngrams(expected_tokens, n)
            actual_ngrams = self._get_ngrams(actual_tokens, n)
            
            if not actual_ngrams:
                precisions.append(0.0)
                continue
            
            # Count matches
            matches = 0
            for ngram in actual_ngrams:
                if ngram in expected_ngrams:
                    matches += min(actual_ngrams[ngram], expected_ngrams[ngram])
            
            precision = safe_divide(matches, sum(actual_ngrams.values()))
            precisions.append(precision)
        
        # Calculate geometric mean of precisions
        if all(p > 0 for p in precisions):
            geometric_mean = np.exp(np.mean(np.log(precisions)))
        else:
            geometric_mean = 0.0
        
        # Apply brevity penalty
        brevity_penalty = self._calculate_brevity_penalty(len(expected_tokens), len(actual_tokens))
        bleu_score = brevity_penalty * geometric_mean
        
        return MetricResult(
            name=self.name,
            score=bleu_score,
            metadata={
                "precisions": precisions,
                "brevity_penalty": brevity_penalty,
                "expected_length": len(expected_tokens),
                "actual_length": len(actual_tokens)
            }
        )
    
    def _get_ngrams(self, tokens: List[str], n: int) -> Counter:
        """Get n-grams from token list."""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n])
            ngrams.append(ngram)
        return Counter(ngrams)
    
    def _calculate_brevity_penalty(self, ref_length: int, cand_length: int) -> float:
        """Calculate brevity penalty for BLEU score."""
        if cand_length >= ref_length:
            return 1.0
        else:
            return np.exp(1 - ref_length / cand_length)


class ROUGEMetric(TextSimilarityMetric):
    """
    ROUGE (Recall-Oriented Understudy for Gisting Evaluation) score.
    
    Measures recall-based overlap between expected and actual text.
    """
    
    def __init__(self, rouge_types: List[str] = None, case_sensitive: bool = False):
        """
        Initialize ROUGE metric.
        
        Args:
            rouge_types: List of ROUGE types to calculate (e.g., ['rouge1', 'rouge2', 'rougeL'])
            case_sensitive: Whether to perform case-sensitive comparison
        """
        if rouge_types is None:
            rouge_types = ['rouge1', 'rouge2', 'rougeL']
        
        super().__init__(
            name="ROUGE",
            description=f"ROUGE scores: {', '.join(rouge_types)}",
            case_sensitive=case_sensitive
        )
        self.rouge_types = rouge_types
        self.scorer = rouge_scorer.RougeScorer(rouge_types, use_stemmer=True)
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate ROUGE scores between expected and actual text.
        
        Args:
            expected: Expected/reference text
            actual: Actual/candidate text
            
        Returns:
            MetricResult with ROUGE scores
        """
        expected_text = self.preprocess_text(str(expected))
        actual_text = self.preprocess_text(str(actual))
        
        scores = self.scorer.score(expected_text, actual_text)
        
        # Extract F1 scores for each ROUGE type
        rouge_scores = {}
        total_score = 0.0
        
        for rouge_type in self.rouge_types:
            if rouge_type in scores:
                f1_score = scores[rouge_type].fmeasure
                rouge_scores[rouge_type] = f1_score
                total_score += f1_score
        
        # Average F1 score across all ROUGE types
        average_score = safe_divide(total_score, len(self.rouge_types))
        
        return MetricResult(
            name=self.name,
            score=average_score,
            metadata={
                "rouge_scores": rouge_scores,
                "detailed_scores": {
                    rouge_type: {
                        "precision": scores[rouge_type].precision,
                        "recall": scores[rouge_type].recall,
                        "fmeasure": scores[rouge_type].fmeasure
                    }
                    for rouge_type in self.rouge_types if rouge_type in scores
                }
            }
        )


class SemanticSimilarityMetric(BaseMetric):
    """
    Semantic similarity using sentence transformers.
    
    Measures semantic similarity between texts using pre-trained embeddings.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize semantic similarity metric.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        super().__init__(
            name="SemanticSimilarity",
            description=f"Semantic similarity using {model_name}"
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
        Calculate semantic similarity between expected and actual text.
        
        Args:
            expected: Expected/reference text
            actual: Actual/candidate text
            
        Returns:
            MetricResult with semantic similarity score
        """
        expected_text = str(expected).strip()
        actual_text = str(actual).strip()
        
        if not expected_text or not actual_text:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "Empty text"}
            )
        
        # Generate embeddings
        embeddings = self.model.encode([expected_text, actual_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        # Ensure score is in [0, 1] range
        similarity = max(0.0, min(1.0, similarity))
        
        return MetricResult(
            name=self.name,
            score=similarity,
            metadata={
                "model_name": self.model_name,
                "expected_length": len(expected_text),
                "actual_length": len(actual_text)
            }
        )


class FactualAccuracyMetric(BaseMetric):
    """
    Factual accuracy checking using keyword and entity matching.
    
    Measures how well the actual answer preserves factual information from expected answer.
    """
    
    def __init__(self, case_sensitive: bool = False, use_stemming: bool = True):
        """
        Initialize factual accuracy metric.
        
        Args:
            case_sensitive: Whether to perform case-sensitive comparison
            use_stemming: Whether to use stemming for word matching
        """
        super().__init__(
            name="FactualAccuracy",
            description="Factual accuracy based on keyword and entity preservation"
        )
        self.case_sensitive = case_sensitive
        self.use_stemming = use_stemming
        
        if use_stemming:
            try:
                from nltk.stem import PorterStemmer
                self.stemmer = PorterStemmer()
            except ImportError:
                self.stemmer = None
                self.use_stemming = False
        else:
            self.stemmer = None
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate factual accuracy between expected and actual text.
        
        Args:
            expected: Expected/reference text containing facts
            actual: Actual/candidate text to check for factual accuracy
            
        Returns:
            MetricResult with factual accuracy score
        """
        expected_text = str(expected)
        actual_text = str(actual)
        
        if not self.case_sensitive:
            expected_text = expected_text.lower()
            actual_text = actual_text.lower()
        
        # Extract important terms (numbers, proper nouns, key phrases)
        expected_facts = self._extract_facts(expected_text)
        actual_facts = self._extract_facts(actual_text)
        
        if not expected_facts:
            return MetricResult(
                name=self.name,
                score=1.0,  # No facts to verify
                metadata={"reason": "No facts found in expected text"}
            )
        
        # Calculate fact preservation ratio
        preserved_facts = 0
        for fact in expected_facts:
            if self._fact_present(fact, actual_facts):
                preserved_facts += 1
        
        accuracy = safe_divide(preserved_facts, len(expected_facts))
        
        return MetricResult(
            name=self.name,
            score=accuracy,
            metadata={
                "expected_facts": list(expected_facts),
                "actual_facts": list(actual_facts),
                "preserved_facts": preserved_facts,
                "total_facts": len(expected_facts)
            }
        )
    
    def _extract_facts(self, text: str) -> Set[str]:
        """Extract factual information from text."""
        facts = set()
        
        # Extract numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        facts.update(numbers)
        
        # Extract capitalized words (potential proper nouns)
        if self.case_sensitive:
            proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', text)
            facts.update(proper_nouns)
        
        # Extract quoted phrases
        quoted = re.findall(r'"([^"]*)"', text)
        facts.update(quoted)
        
        # Extract important keywords (longer words, excluding common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        important_words = [w for w in words if len(w) > 3 and w not in stop_words]
        
        if self.use_stemming and self.stemmer:
            important_words = [self.stemmer.stem(w) for w in important_words]
        
        facts.update(important_words)
        
        return facts
    
    def _fact_present(self, fact: str, actual_facts: Set[str]) -> bool:
        """Check if a fact is present in the actual facts."""
        if fact in actual_facts:
            return True
        
        # Check for partial matches for longer facts
        if len(fact) > 5:
            for actual_fact in actual_facts:
                if fact in actual_fact or actual_fact in fact:
                    return True
        
        return False


class QAMetrics:
    """
    Comprehensive Q&A evaluation metrics suite.
    
    Combines multiple metrics for thorough evaluation of Q&A systems.
    """
    
    def __init__(self, 
                 include_bleu: bool = True,
                 include_rouge: bool = True,
                 include_semantic: bool = True,
                 include_factual: bool = True,
                 semantic_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize Q&A metrics suite.
        
        Args:
            include_bleu: Whether to include BLEU score
            include_rouge: Whether to include ROUGE score
            include_semantic: Whether to include semantic similarity
            include_factual: Whether to include factual accuracy
            semantic_model: Model name for semantic similarity
        """
        self.metrics = {}
        
        if include_bleu:
            self.metrics['bleu'] = BLEUMetric()
        
        if include_rouge:
            self.metrics['rouge'] = ROUGEMetric()
        
        if include_semantic:
            self.metrics['semantic'] = SemanticSimilarityMetric(semantic_model)
        
        if include_factual:
            self.metrics['factual'] = FactualAccuracyMetric()
    
    def evaluate(self, expected: Any, actual: Any) -> Dict[str, MetricResult]:
        """
        Evaluate Q&A response using all configured metrics.
        
        Args:
            expected: Expected/reference answer
            actual: Actual/candidate answer
            
        Returns:
            Dictionary of metric results
        """
        results = {}
        
        for metric_name, metric in self.metrics.items():
            try:
                result = metric.calculate(expected, actual)
                results[metric_name] = result
            except Exception as e:
                # Return zero score if metric calculation fails
                results[metric_name] = MetricResult(
                    name=metric.name,
                    score=0.0,
                    metadata={"error": str(e)}
                )
        
        return results
    
    def get_overall_score(self, results: Dict[str, MetricResult], weights: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate overall weighted score from individual metric results.
        
        Args:
            results: Dictionary of metric results
            weights: Optional weights for each metric (defaults to equal weights)
            
        Returns:
            Overall weighted score
        """
        if not results:
            return 0.0
        
        if weights is None:
            weights = {name: 1.0 for name in results.keys()}
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric_name, result in results.items():
            weight = weights.get(metric_name, 1.0)
            total_score += result.score * weight
            total_weight += weight
        
        return safe_divide(total_score, total_weight)
