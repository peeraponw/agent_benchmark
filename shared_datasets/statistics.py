"""
Dataset statistics and analysis utilities.

This module provides comprehensive statistical analysis capabilities for
datasets, including distribution analysis, quality metrics, and reporting.
"""

import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .core.models import DatasetItem
from .core.exceptions import DatasetError, DatasetValidationError


class DatasetStatistics:
    """
    Utility class for calculating comprehensive dataset statistics.
    
    This class provides methods for analyzing dataset composition,
    quality metrics, and generating statistical reports.
    """
    
    def __init__(self):
        """Initialize the DatasetStatistics calculator."""
        self.logger = logging.getLogger(__name__)
    
    def calculate_qa_stats(self, qa_items: List[DatasetItem]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for Q&A dataset.
        
        Args:
            qa_items: List of Q&A DatasetItem objects
            
        Returns:
            Dictionary containing Q&A statistics
        """
        if not qa_items:
            return {'error': 'No Q&A items provided', 'total_items': 0}
        
        stats = {
            'total_items': len(qa_items),
            'categories': {},
            'difficulty_levels': {},
            'response_types': {},
            'question_lengths': [],
            'answer_lengths': [],
            'metadata_coverage': {},
            'quality_metrics': {}
        }
        
        # Analyze each item
        categories = Counter()
        difficulties = Counter()
        response_types = Counter()
        question_lengths = []
        answer_lengths = []
        metadata_keys = Counter()
        
        for item in qa_items:
            # Category analysis
            if item.category:
                categories[item.category] += 1
            
            # Difficulty analysis
            if item.difficulty_level:
                difficulties[item.difficulty_level] += 1
            
            # Extract question and answer for length analysis
            question_text = ""
            answer_text = ""
            
            if isinstance(item.input_data, dict):
                question_text = str(item.input_data.get('question', ''))
                response_type = item.input_data.get('expected_response_type', 'unknown')
                response_types[response_type] += 1
            elif isinstance(item.input_data, str):
                question_text = item.input_data
                response_types['text'] += 1
            
            if isinstance(item.expected_output, dict):
                answer_text = str(item.expected_output.get('answer', ''))
            elif isinstance(item.expected_output, str):
                answer_text = item.expected_output
            
            # Length analysis
            if question_text:
                question_lengths.append(len(question_text))
            if answer_text:
                answer_lengths.append(len(answer_text))
            
            # Metadata analysis
            if item.metadata:
                for key in item.metadata.keys():
                    metadata_keys[key] += 1
        
        # Compile statistics
        stats['categories'] = dict(categories)
        stats['difficulty_levels'] = dict(difficulties)
        stats['response_types'] = dict(response_types)
        stats['metadata_coverage'] = dict(metadata_keys)
        
        # Calculate length statistics
        if question_lengths:
            stats['question_length_stats'] = {
                'min': min(question_lengths),
                'max': max(question_lengths),
                'avg': sum(question_lengths) / len(question_lengths),
                'median': sorted(question_lengths)[len(question_lengths) // 2]
            }
        
        if answer_lengths:
            stats['answer_length_stats'] = {
                'min': min(answer_lengths),
                'max': max(answer_lengths),
                'avg': sum(answer_lengths) / len(answer_lengths),
                'median': sorted(answer_lengths)[len(answer_lengths) // 2]
            }
        
        # Quality metrics
        stats['quality_metrics'] = self._calculate_qa_quality_metrics(qa_items)
        
        return stats
    
    def calculate_rag_stats(self, rag_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for RAG documents.
        
        Args:
            rag_documents: List of RAG document dictionaries
            
        Returns:
            Dictionary containing RAG statistics
        """
        if not rag_documents:
            return {'error': 'No RAG documents provided', 'total_documents': 0}
        
        stats = {
            'total_documents': len(rag_documents),
            'formats': {},
            'domains': {},
            'content_types': {},
            'size_stats': {},
            'quality_metrics': {}
        }
        
        # Analyze documents
        formats = Counter()
        domains = Counter()
        content_types = Counter()
        sizes = []
        
        for doc in rag_documents:
            # Format analysis
            doc_format = doc.get('format', 'unknown')
            formats[doc_format] += 1
            
            # Domain analysis
            domain = doc.get('metadata', {}).get('domain', 'unknown')
            domains[domain] += 1
            
            # Content type analysis
            content_type = doc.get('metadata', {}).get('content_type', 'unknown')
            content_types[content_type] += 1
            
            # Size analysis
            size = doc.get('size_bytes', 0)
            if size > 0:
                sizes.append(size)
        
        # Compile statistics
        stats['formats'] = dict(formats)
        stats['domains'] = dict(domains)
        stats['content_types'] = dict(content_types)
        
        # Size statistics
        if sizes:
            stats['size_stats'] = {
                'min_bytes': min(sizes),
                'max_bytes': max(sizes),
                'avg_bytes': sum(sizes) / len(sizes),
                'total_bytes': sum(sizes)
            }
        
        # Quality metrics
        stats['quality_metrics'] = self._calculate_rag_quality_metrics(rag_documents)
        
        return stats
    
    def calculate_web_search_stats(self, search_items: List[DatasetItem]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for web search queries.
        
        Args:
            search_items: List of web search DatasetItem objects
            
        Returns:
            Dictionary containing web search statistics
        """
        if not search_items:
            return {'error': 'No web search items provided', 'total_queries': 0}
        
        stats = {
            'total_queries': len(search_items),
            'search_types': {},
            'categories': {},
            'difficulty_levels': {},
            'freshness_requirements': {},
            'query_lengths': [],
            'expected_source_counts': [],
            'quality_metrics': {}
        }
        
        # Analyze search queries
        search_types = Counter()
        categories = Counter()
        difficulties = Counter()
        freshness_reqs = Counter()
        query_lengths = []
        source_counts = []
        
        for item in search_items:
            # Category and difficulty
            if item.category:
                categories[item.category] += 1
            if item.difficulty_level:
                difficulties[item.difficulty_level] += 1
            
            # Extract search-specific data
            if isinstance(item.input_data, dict):
                search_type = item.input_data.get('search_type', 'general')
                search_types[search_type] += 1
                
                freshness = item.input_data.get('freshness_requirement', 'none')
                freshness_reqs[freshness] += 1
                
                query_text = item.input_data.get('query', '')
                if query_text:
                    query_lengths.append(len(query_text))
            
            # Expected sources analysis
            if isinstance(item.expected_output, dict):
                expected_sources = item.expected_output.get('expected_sources', [])
                if expected_sources:
                    source_counts.append(len(expected_sources))
        
        # Compile statistics
        stats['search_types'] = dict(search_types)
        stats['categories'] = dict(categories)
        stats['difficulty_levels'] = dict(difficulties)
        stats['freshness_requirements'] = dict(freshness_reqs)
        
        # Length and count statistics
        if query_lengths:
            stats['query_length_stats'] = {
                'min': min(query_lengths),
                'max': max(query_lengths),
                'avg': sum(query_lengths) / len(query_lengths)
            }
        
        if source_counts:
            stats['expected_source_stats'] = {
                'min': min(source_counts),
                'max': max(source_counts),
                'avg': sum(source_counts) / len(source_counts)
            }
        
        # Quality metrics
        stats['quality_metrics'] = self._calculate_web_search_quality_metrics(search_items)
        
        return stats
    
    def calculate_multi_agent_stats(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics for multi-agent scenarios.
        
        Args:
            scenarios: List of multi-agent scenario dictionaries
            
        Returns:
            Dictionary containing multi-agent statistics
        """
        if not scenarios:
            return {'error': 'No multi-agent scenarios provided', 'total_scenarios': 0}
        
        stats = {
            'total_scenarios': len(scenarios),
            'scenario_types': {},
            'complexity_levels': {},
            'coordination_patterns': {},
            'agent_roles': {},
            'agent_count_distribution': {},
            'quality_metrics': {}
        }
        
        # Analyze scenarios
        scenario_types = Counter()
        complexity_levels = Counter()
        coordination_patterns = Counter()
        all_roles = Counter()
        agent_counts = []
        
        for scenario in scenarios:
            # Basic categorization
            scenario_type = scenario.get('type', 'unknown')
            scenario_types[scenario_type] += 1
            
            complexity = scenario.get('complexity_level', 'unknown')
            complexity_levels[complexity_level] += 1
            
            coordination = scenario.get('coordination_pattern', 'unknown')
            coordination_patterns[coordination] += 1
            
            # Agent analysis
            required_agents = scenario.get('required_agents', [])
            if required_agents:
                agent_counts.append(len(required_agents))
                
                # Analyze agent roles
                for agent in required_agents:
                    if isinstance(agent, dict):
                        role = agent.get('role', 'unknown')
                        all_roles[role] += 1
                    elif isinstance(agent, str):
                        all_roles[agent] += 1
        
        # Compile statistics
        stats['scenario_types'] = dict(scenario_types)
        stats['complexity_levels'] = dict(complexity_levels)
        stats['coordination_patterns'] = dict(coordination_patterns)
        stats['agent_roles'] = dict(all_roles)
        
        # Agent count statistics
        if agent_counts:
            stats['avg_agents_per_scenario'] = sum(agent_counts) / len(agent_counts)
            agent_count_dist = Counter(agent_counts)
            stats['agent_count_distribution'] = dict(agent_count_dist)
        
        # Quality metrics
        stats['quality_metrics'] = self._calculate_multi_agent_quality_metrics(scenarios)

        return stats

    def calculate_overall_stats(self, all_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall dataset statistics across all dataset types.

        Args:
            all_stats: Dictionary containing statistics for all dataset types

        Returns:
            Dictionary containing overall statistics
        """
        overall = {
            'total_datasets': 0,
            'total_items': 0,
            'datasets_with_errors': 0,
            'coverage_analysis': {},
            'freshness_info': {
                'last_updated': datetime.now().isoformat(),
                'dataset_path': all_stats.get('dataset_path', 'unknown')
            }
        }

        # Count datasets and items
        for dataset_type, stats in all_stats.items():
            if dataset_type in ['qa_stats', 'rag_stats', 'web_search_stats', 'multi_agent_stats']:
                overall['total_datasets'] += 1

                if 'error' in stats:
                    overall['datasets_with_errors'] += 1
                else:
                    # Add item counts
                    if 'total_items' in stats:
                        overall['total_items'] += stats['total_items']
                    elif 'total_documents' in stats:
                        overall['total_items'] += stats['total_documents']
                    elif 'total_queries' in stats:
                        overall['total_items'] += stats['total_queries']
                    elif 'total_scenarios' in stats:
                        overall['total_items'] += stats['total_scenarios']

        # Coverage analysis
        overall['coverage_analysis'] = {
            'datasets_available': overall['total_datasets'],
            'datasets_functional': overall['total_datasets'] - overall['datasets_with_errors'],
            'coverage_percentage': (
                (overall['total_datasets'] - overall['datasets_with_errors']) /
                max(overall['total_datasets'], 1) * 100
            )
        }

        return overall

    def _calculate_qa_quality_metrics(self, qa_items: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate quality metrics specific to Q&A datasets."""
        metrics = {
            'completeness_score': 0.0,
            'diversity_score': 0.0,
            'metadata_richness': 0.0
        }

        if not qa_items:
            return metrics

        # Completeness: items with both question and answer
        complete_items = 0
        items_with_metadata = 0

        for item in qa_items:
            has_question = False
            has_answer = False

            if isinstance(item.input_data, dict):
                has_question = bool(item.input_data.get('question'))
            elif isinstance(item.input_data, str):
                has_question = bool(item.input_data.strip())

            if isinstance(item.expected_output, dict):
                has_answer = bool(item.expected_output.get('answer'))
            elif isinstance(item.expected_output, str):
                has_answer = bool(item.expected_output.strip())

            if has_question and has_answer:
                complete_items += 1

            if item.metadata:
                items_with_metadata += 1

        metrics['completeness_score'] = complete_items / len(qa_items)
        metrics['metadata_richness'] = items_with_metadata / len(qa_items)

        # Diversity: based on categories and difficulty levels
        categories = set(item.category for item in qa_items if item.category)
        difficulties = set(item.difficulty_level for item in qa_items if item.difficulty_level)

        # Simple diversity score based on variety
        category_diversity = min(len(categories) / 5, 1.0)  # Assume 5 is good diversity
        difficulty_diversity = min(len(difficulties) / 3, 1.0)  # Assume 3 is good diversity
        metrics['diversity_score'] = (category_diversity + difficulty_diversity) / 2

        return metrics

    def _calculate_rag_quality_metrics(self, rag_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate quality metrics specific to RAG documents."""
        metrics = {
            'format_diversity': 0.0,
            'domain_coverage': 0.0,
            'size_consistency': 0.0
        }

        if not rag_documents:
            return metrics

        # Format diversity
        formats = set(doc.get('format', 'unknown') for doc in rag_documents)
        metrics['format_diversity'] = min(len(formats) / 4, 1.0)  # Assume 4 formats is good

        # Domain coverage
        domains = set(doc.get('metadata', {}).get('domain', 'unknown') for doc in rag_documents)
        metrics['domain_coverage'] = min(len(domains) / 5, 1.0)  # Assume 5 domains is good

        # Size consistency (coefficient of variation)
        sizes = [doc.get('size_bytes', 0) for doc in rag_documents if doc.get('size_bytes', 0) > 0]
        if sizes and len(sizes) > 1:
            mean_size = sum(sizes) / len(sizes)
            variance = sum((size - mean_size) ** 2 for size in sizes) / len(sizes)
            std_dev = variance ** 0.5
            cv = std_dev / mean_size if mean_size > 0 else 1.0
            metrics['size_consistency'] = max(0, 1 - cv)  # Lower CV = higher consistency

        return metrics

    def _calculate_web_search_quality_metrics(self, search_items: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate quality metrics specific to web search queries."""
        metrics = {
            'query_diversity': 0.0,
            'source_coverage': 0.0,
            'freshness_awareness': 0.0
        }

        if not search_items:
            return metrics

        # Query type diversity
        search_types = set()
        freshness_reqs = set()
        items_with_sources = 0

        for item in search_items:
            if isinstance(item.input_data, dict):
                search_type = item.input_data.get('search_type', 'general')
                search_types.add(search_type)

                freshness = item.input_data.get('freshness_requirement')
                if freshness:
                    freshness_reqs.add(freshness)

            if isinstance(item.expected_output, dict):
                sources = item.expected_output.get('expected_sources', [])
                if sources:
                    items_with_sources += 1

        metrics['query_diversity'] = min(len(search_types) / 4, 1.0)  # Assume 4 types is good
        metrics['source_coverage'] = items_with_sources / len(search_items)
        metrics['freshness_awareness'] = min(len(freshness_reqs) / 3, 1.0)  # Assume 3 levels is good

        return metrics

    def _calculate_multi_agent_quality_metrics(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate quality metrics specific to multi-agent scenarios."""
        metrics = {
            'scenario_diversity': 0.0,
            'complexity_coverage': 0.0,
            'agent_role_diversity': 0.0
        }

        if not scenarios:
            return metrics

        # Scenario type diversity
        scenario_types = set(scenario.get('type', 'unknown') for scenario in scenarios)
        metrics['scenario_diversity'] = min(len(scenario_types) / 3, 1.0)  # Assume 3 types is good

        # Complexity coverage
        complexities = set(scenario.get('complexity_level', 'unknown') for scenario in scenarios)
        metrics['complexity_coverage'] = min(len(complexities) / 4, 1.0)  # Assume 4 levels is good

        # Agent role diversity
        all_roles = set()
        for scenario in scenarios:
            agents = scenario.get('required_agents', [])
            for agent in agents:
                if isinstance(agent, dict):
                    role = agent.get('role', 'unknown')
                    all_roles.add(role)
                elif isinstance(agent, str):
                    all_roles.add(agent)

        metrics['agent_role_diversity'] = min(len(all_roles) / 8, 1.0)  # Assume 8 roles is good

        return metrics

    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
