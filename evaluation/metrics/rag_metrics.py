"""
Retrieval-Augmented Generation (RAG) evaluation metrics.

This module provides specialized metrics for evaluating RAG systems including
retrieval precision/recall, context relevance, and answer groundedness.
"""

import re
from typing import Any, Dict, List, Optional, Set, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .base_metrics import BaseMetric, MetricResult, safe_divide


class RetrievalPrecisionMetric(BaseMetric):
    """
    Precision metric for document retrieval in RAG systems.
    
    Measures what fraction of retrieved documents are relevant.
    """
    
    def __init__(self):
        super().__init__(
            name="RetrievalPrecision",
            description="Precision of retrieved documents (relevant retrieved / total retrieved)"
        )
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate retrieval precision.
        
        Args:
            expected: List of relevant document IDs or content
            actual: List of retrieved document IDs or content
            
        Returns:
            MetricResult with precision score
        """
        expected_docs = self._normalize_doc_list(expected)
        retrieved_docs = self._normalize_doc_list(actual)
        
        if not retrieved_docs:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "No documents retrieved"}
            )
        
        # Count relevant documents in retrieved set
        relevant_retrieved = len(set(expected_docs) & set(retrieved_docs))
        precision = safe_divide(relevant_retrieved, len(retrieved_docs))
        
        return MetricResult(
            name=self.name,
            score=precision,
            metadata={
                "relevant_retrieved": relevant_retrieved,
                "total_retrieved": len(retrieved_docs),
                "total_relevant": len(expected_docs)
            }
        )
    
    def _normalize_doc_list(self, docs: Any) -> List[str]:
        """Normalize document list to consistent format."""
        if isinstance(docs, str):
            return [docs]
        elif isinstance(docs, (list, tuple)):
            return [str(doc) for doc in docs]
        else:
            return [str(docs)]


class RetrievalRecallMetric(BaseMetric):
    """
    Recall metric for document retrieval in RAG systems.
    
    Measures what fraction of relevant documents were retrieved.
    """
    
    def __init__(self):
        super().__init__(
            name="RetrievalRecall",
            description="Recall of retrieved documents (relevant retrieved / total relevant)"
        )
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate retrieval recall.
        
        Args:
            expected: List of relevant document IDs or content
            actual: List of retrieved document IDs or content
            
        Returns:
            MetricResult with recall score
        """
        expected_docs = self._normalize_doc_list(expected)
        retrieved_docs = self._normalize_doc_list(actual)
        
        if not expected_docs:
            return MetricResult(
                name=self.name,
                score=1.0,  # No relevant documents to retrieve
                metadata={"reason": "No relevant documents"}
            )
        
        # Count relevant documents in retrieved set
        relevant_retrieved = len(set(expected_docs) & set(retrieved_docs))
        recall = safe_divide(relevant_retrieved, len(expected_docs))
        
        return MetricResult(
            name=self.name,
            score=recall,
            metadata={
                "relevant_retrieved": relevant_retrieved,
                "total_retrieved": len(retrieved_docs),
                "total_relevant": len(expected_docs)
            }
        )
    
    def _normalize_doc_list(self, docs: Any) -> List[str]:
        """Normalize document list to consistent format."""
        if isinstance(docs, str):
            return [docs]
        elif isinstance(docs, (list, tuple)):
            return [str(doc) for doc in docs]
        else:
            return [str(docs)]


class ContextRelevanceMetric(BaseMetric):
    """
    Context relevance metric for RAG systems.
    
    Measures how relevant the retrieved context is to the query.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", threshold: float = 0.5):
        """
        Initialize context relevance metric.
        
        Args:
            model_name: Sentence transformer model for similarity calculation
            threshold: Minimum similarity threshold for relevance
        """
        super().__init__(
            name="ContextRelevance",
            description=f"Context relevance using {model_name} (threshold: {threshold})"
        )
        self.model_name = model_name
        self.threshold = threshold
        self._model = None
    
    @property
    def model(self):
        """Lazy load the sentence transformer model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def calculate(self, expected: Any, actual: Any, **kwargs) -> MetricResult:
        """
        Calculate context relevance score.
        
        Args:
            expected: Query or question text
            actual: Retrieved context/documents
            **kwargs: Additional parameters (e.g., 'query' if expected is not the query)
            
        Returns:
            MetricResult with context relevance score
        """
        query = kwargs.get('query', str(expected))
        context = str(actual)
        
        if not query.strip() or not context.strip():
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "Empty query or context"}
            )
        
        # Split context into chunks if it's very long
        context_chunks = self._split_context(context)
        
        # Calculate similarity between query and each context chunk
        similarities = []
        for chunk in context_chunks:
            embeddings = self.model.encode([query, chunk])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            similarities.append(max(0.0, similarity))  # Ensure non-negative
        
        # Use maximum similarity as the relevance score
        max_similarity = max(similarities) if similarities else 0.0
        
        # Calculate percentage of chunks above threshold
        relevant_chunks = sum(1 for sim in similarities if sim >= self.threshold)
        relevance_ratio = safe_divide(relevant_chunks, len(similarities))
        
        return MetricResult(
            name=self.name,
            score=max_similarity,
            metadata={
                "max_similarity": max_similarity,
                "avg_similarity": np.mean(similarities) if similarities else 0.0,
                "relevance_ratio": relevance_ratio,
                "threshold": self.threshold,
                "num_chunks": len(similarities),
                "relevant_chunks": relevant_chunks
            }
        )
    
    def _split_context(self, context: str, max_chunk_size: int = 500) -> List[str]:
        """Split long context into smaller chunks."""
        if len(context) <= max_chunk_size:
            return [context]
        
        # Split by sentences first
        sentences = re.split(r'[.!?]+', context)
        chunks = []
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
        
        return chunks if chunks else [context]


class AnswerGroundednessMetric(BaseMetric):
    """
    Answer groundedness metric for RAG systems.
    
    Measures how well the generated answer is grounded in the provided context.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize answer groundedness metric.
        
        Args:
            model_name: Sentence transformer model for similarity calculation
        """
        super().__init__(
            name="AnswerGroundedness",
            description=f"Answer groundedness in context using {model_name}"
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
        Calculate answer groundedness score.
        
        Args:
            expected: Context/source documents
            actual: Generated answer
            **kwargs: Additional parameters
            
        Returns:
            MetricResult with groundedness score
        """
        context = str(expected)
        answer = str(actual)
        
        if not context.strip() or not answer.strip():
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "Empty context or answer"}
            )
        
        # Split answer into claims/sentences
        answer_claims = self._extract_claims(answer)
        
        if not answer_claims:
            return MetricResult(
                name=self.name,
                score=0.0,
                metadata={"reason": "No claims found in answer"}
            )
        
        # Check how many claims are supported by context
        supported_claims = 0
        claim_scores = []
        
        for claim in answer_claims:
            support_score = self._calculate_claim_support(claim, context)
            claim_scores.append(support_score)
            if support_score > 0.5:  # Threshold for considering a claim supported
                supported_claims += 1
        
        # Calculate overall groundedness
        groundedness = safe_divide(supported_claims, len(answer_claims))
        avg_support = np.mean(claim_scores) if claim_scores else 0.0
        
        return MetricResult(
            name=self.name,
            score=groundedness,
            metadata={
                "supported_claims": supported_claims,
                "total_claims": len(answer_claims),
                "avg_support_score": avg_support,
                "claim_scores": claim_scores,
                "claims": answer_claims
            }
        )
    
    def _extract_claims(self, answer: str) -> List[str]:
        """Extract individual claims from the answer."""
        # Split by sentences
        sentences = re.split(r'[.!?]+', answer)
        claims = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short sentences
                claims.append(sentence)
        
        return claims
    
    def _calculate_claim_support(self, claim: str, context: str) -> float:
        """Calculate how well a claim is supported by the context."""
        # Split context into chunks
        context_chunks = self._split_context(context)
        
        # Find the best supporting chunk
        max_similarity = 0.0
        
        for chunk in context_chunks:
            embeddings = self.model.encode([claim, chunk])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            max_similarity = max(max_similarity, similarity)
        
        return max(0.0, max_similarity)
    
    def _split_context(self, context: str, max_chunk_size: int = 300) -> List[str]:
        """Split context into smaller chunks for comparison."""
        if len(context) <= max_chunk_size:
            return [context]
        
        sentences = re.split(r'[.!?]+', context)
        chunks = []
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
        
        return chunks if chunks else [context]


class RAGMetrics:
    """
    Comprehensive RAG evaluation metrics suite.
    
    Combines multiple metrics for thorough evaluation of RAG systems.
    """
    
    def __init__(self, 
                 include_precision: bool = True,
                 include_recall: bool = True,
                 include_context_relevance: bool = True,
                 include_groundedness: bool = True,
                 semantic_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG metrics suite.
        
        Args:
            include_precision: Whether to include retrieval precision
            include_recall: Whether to include retrieval recall
            include_context_relevance: Whether to include context relevance
            include_groundedness: Whether to include answer groundedness
            semantic_model: Model name for semantic similarity calculations
        """
        self.metrics = {}
        
        if include_precision:
            self.metrics['precision'] = RetrievalPrecisionMetric()
        
        if include_recall:
            self.metrics['recall'] = RetrievalRecallMetric()
        
        if include_context_relevance:
            self.metrics['context_relevance'] = ContextRelevanceMetric(semantic_model)
        
        if include_groundedness:
            self.metrics['groundedness'] = AnswerGroundednessMetric(semantic_model)
    
    def evaluate_retrieval(self, relevant_docs: List[str], retrieved_docs: List[str]) -> Dict[str, MetricResult]:
        """
        Evaluate retrieval performance.
        
        Args:
            relevant_docs: List of relevant document IDs
            retrieved_docs: List of retrieved document IDs
            
        Returns:
            Dictionary of retrieval metric results
        """
        results = {}
        
        if 'precision' in self.metrics:
            results['precision'] = self.metrics['precision'].calculate(relevant_docs, retrieved_docs)
        
        if 'recall' in self.metrics:
            results['recall'] = self.metrics['recall'].calculate(relevant_docs, retrieved_docs)
        
        return results
    
    def evaluate_generation(self, query: str, context: str, answer: str) -> Dict[str, MetricResult]:
        """
        Evaluate generation performance.
        
        Args:
            query: Input query/question
            context: Retrieved context
            answer: Generated answer
            
        Returns:
            Dictionary of generation metric results
        """
        results = {}
        
        if 'context_relevance' in self.metrics:
            results['context_relevance'] = self.metrics['context_relevance'].calculate(
                query, context, query=query
            )
        
        if 'groundedness' in self.metrics:
            results['groundedness'] = self.metrics['groundedness'].calculate(context, answer)
        
        return results
    
    def evaluate_full_pipeline(self, 
                              query: str,
                              relevant_docs: List[str],
                              retrieved_docs: List[str],
                              context: str,
                              answer: str) -> Dict[str, MetricResult]:
        """
        Evaluate the full RAG pipeline.
        
        Args:
            query: Input query/question
            relevant_docs: List of relevant document IDs
            retrieved_docs: List of retrieved document IDs
            context: Retrieved context text
            answer: Generated answer
            
        Returns:
            Dictionary of all metric results
        """
        results = {}
        
        # Evaluate retrieval
        retrieval_results = self.evaluate_retrieval(relevant_docs, retrieved_docs)
        results.update(retrieval_results)
        
        # Evaluate generation
        generation_results = self.evaluate_generation(query, context, answer)
        results.update(generation_results)
        
        return results
