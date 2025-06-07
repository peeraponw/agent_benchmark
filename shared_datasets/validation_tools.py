"""
Data Quality Validation Tools for AI Agent Framework Comparison Project.

This module provides essential validation utilities for ensuring data quality
across all datasets used in the evaluation framework.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import Counter
import re

from dataset_manager import DatasetManager, DatasetItem
from validator import DatasetValidator
from config import DatasetConfig


class DatasetIntegrityChecker:
    """
    Essential data integrity checking tools for dataset quality assurance.
    
    This class provides core validation functionality to ensure datasets
    meet quality standards for AI agent framework evaluation.
    """
    
    def __init__(self, config: DatasetConfig = None):
        """
        Initialize the integrity checker.
        
        Args:
            config: Dataset configuration instance
        """
        self.config = config or DatasetConfig()
        self.logger = logging.getLogger(__name__)
        
    def check_schema_compliance(self, dataset_items: List[DatasetItem]) -> Dict[str, Any]:
        """
        Check if all dataset items comply with the expected schema.
        
        Args:
            dataset_items: List of dataset items to validate
            
        Returns:
            Dictionary containing validation results and statistics
        """
        results = {
            'total_items': len(dataset_items),
            'valid_items': 0,
            'invalid_items': 0,
            'schema_errors': [],
            'missing_fields': Counter(),
            'invalid_types': Counter()
        }
        
        required_fields = ['id', 'input_data', 'expected_output', 'metadata']
        
        for i, item in enumerate(dataset_items):
            try:
                # Check required fields
                item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
                
                for field in required_fields:
                    if field not in item_dict or item_dict[field] is None:
                        results['missing_fields'][field] += 1
                        results['schema_errors'].append(f"Item {i}: Missing field '{field}'")
                
                # Check ID uniqueness and format
                if 'id' in item_dict:
                    if not isinstance(item_dict['id'], str) or len(item_dict['id']) == 0:
                        results['invalid_types']['id'] += 1
                        results['schema_errors'].append(f"Item {i}: Invalid ID format")
                
                # Check metadata structure
                if 'metadata' in item_dict and not isinstance(item_dict['metadata'], dict):
                    results['invalid_types']['metadata'] += 1
                    results['schema_errors'].append(f"Item {i}: Metadata must be a dictionary")
                
                if len([error for error in results['schema_errors'] if f"Item {i}:" in error]) == 0:
                    results['valid_items'] += 1
                else:
                    results['invalid_items'] += 1
                    
            except Exception as e:
                results['invalid_items'] += 1
                results['schema_errors'].append(f"Item {i}: Exception during validation: {str(e)}")
        
        return results
    
    def detect_duplicates(self, dataset_items: List[DatasetItem]) -> Dict[str, Any]:
        """
        Detect duplicate items in the dataset.
        
        Args:
            dataset_items: List of dataset items to check
            
        Returns:
            Dictionary containing duplicate detection results
        """
        results = {
            'total_items': len(dataset_items),
            'duplicate_ids': [],
            'duplicate_content': [],
            'unique_items': 0
        }
        
        # Check for duplicate IDs
        ids = []
        id_to_index = {}
        
        for i, item in enumerate(dataset_items):
            item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
            item_id = item_dict.get('id', f'item_{i}')
            
            if item_id in id_to_index:
                results['duplicate_ids'].append({
                    'id': item_id,
                    'indices': [id_to_index[item_id], i]
                })
            else:
                id_to_index[item_id] = i
            
            ids.append(item_id)
        
        # Check for duplicate content (simplified)
        content_hashes = []
        content_to_indices = {}
        
        for i, item in enumerate(dataset_items):
            item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
            
            # Create a simple content hash based on input_data
            input_data = item_dict.get('input_data', '')
            if isinstance(input_data, dict):
                content_key = str(sorted(input_data.items()))
            else:
                content_key = str(input_data).lower().strip()
            
            content_hash = hash(content_key)
            
            if content_hash in content_to_indices:
                results['duplicate_content'].append({
                    'content_hash': content_hash,
                    'indices': content_to_indices[content_hash] + [i],
                    'sample_content': str(input_data)[:100] + '...' if len(str(input_data)) > 100 else str(input_data)
                })
            else:
                content_to_indices[content_hash] = [i]
        
        results['unique_items'] = len(dataset_items) - len(results['duplicate_ids']) - len(results['duplicate_content'])
        
        return results
    
    def verify_completeness(self, dataset_type: str, dataset_items: List[DatasetItem]) -> Dict[str, Any]:
        """
        Verify dataset completeness against expected requirements.
        
        Args:
            dataset_type: Type of dataset (qa, rag, web_search, multi_agent)
            dataset_items: List of dataset items to check
            
        Returns:
            Dictionary containing completeness verification results
        """
        results = {
            'dataset_type': dataset_type,
            'total_items': len(dataset_items),
            'completeness_score': 0.0,
            'missing_categories': [],
            'category_distribution': Counter(),
            'difficulty_distribution': Counter(),
            'recommendations': []
        }
        
        # Define minimum requirements for each dataset type
        requirements = {
            'qa': {
                'min_items': 100,
                'required_categories': ['factual', 'reasoning', 'contextual', 'multi_step'],
                'required_difficulties': ['easy', 'medium', 'hard']
            },
            'web_search': {
                'min_items': 75,
                'required_categories': ['current_events', 'fact_checking', 'research', 'local_information', 'comparative'],
                'required_difficulties': ['easy', 'medium', 'hard']
            },
            'rag': {
                'min_items': 50,
                'required_categories': ['definition', 'application', 'comparison', 'synthesis'],
                'required_difficulties': ['easy', 'medium', 'hard', 'expert']
            },
            'multi_agent': {
                'min_items': 15,
                'required_categories': ['simple', 'medium', 'complex', 'expert'],
                'required_difficulties': ['simple', 'medium', 'complex', 'expert']
            }
        }
        
        if dataset_type not in requirements:
            results['recommendations'].append(f"Unknown dataset type: {dataset_type}")
            return results
        
        req = requirements[dataset_type]
        
        # Check minimum item count
        if len(dataset_items) < req['min_items']:
            results['recommendations'].append(f"Dataset has {len(dataset_items)} items, minimum required: {req['min_items']}")
        
        # Analyze category and difficulty distribution
        for item in dataset_items:
            item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
            metadata = item_dict.get('metadata', {})
            
            # Extract category
            category = (
                item_dict.get('category') or 
                metadata.get('category') or 
                item_dict.get('query_type') or
                item_dict.get('complexity') or
                'unknown'
            )
            results['category_distribution'][category] += 1
            
            # Extract difficulty
            difficulty = (
                item_dict.get('difficulty') or 
                metadata.get('difficulty') or 
                item_dict.get('complexity') or
                'unknown'
            )
            results['difficulty_distribution'][difficulty] += 1
        
        # Check for missing required categories
        found_categories = set(results['category_distribution'].keys())
        required_categories = set(req['required_categories'])
        missing_categories = required_categories - found_categories
        
        if missing_categories:
            results['missing_categories'] = list(missing_categories)
            results['recommendations'].append(f"Missing required categories: {', '.join(missing_categories)}")
        
        # Check for missing required difficulties
        found_difficulties = set(results['difficulty_distribution'].keys())
        required_difficulties = set(req['required_difficulties'])
        missing_difficulties = required_difficulties - found_difficulties
        
        if missing_difficulties:
            results['recommendations'].append(f"Missing required difficulties: {', '.join(missing_difficulties)}")
        
        # Calculate completeness score
        item_score = min(1.0, len(dataset_items) / req['min_items'])
        category_score = len(found_categories & required_categories) / len(required_categories)
        difficulty_score = len(found_difficulties & required_difficulties) / len(required_difficulties)
        
        results['completeness_score'] = (item_score + category_score + difficulty_score) / 3
        
        return results


class DatasetStatisticsGenerator:
    """
    Generate comprehensive statistics and reports for datasets.
    
    This class provides essential statistical analysis for dataset quality
    assessment and reporting.
    """
    
    def __init__(self, config: DatasetConfig = None):
        """
        Initialize the statistics generator.
        
        Args:
            config: Dataset configuration instance
        """
        self.config = config or DatasetConfig()
        self.logger = logging.getLogger(__name__)
    
    def generate_dataset_summary(self, dataset_manager: DatasetManager) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of all datasets.
        
        Args:
            dataset_manager: DatasetManager instance
            
        Returns:
            Dictionary containing dataset summary statistics
        """
        summary = {
            'generation_timestamp': dataset_manager._get_current_timestamp(),
            'datasets': {},
            'overall_statistics': {
                'total_items': 0,
                'total_datasets': 0,
                'quality_score': 0.0
            }
        }
        
        # Analyze each dataset type
        dataset_types = ['qa', 'web_search', 'rag', 'multi_agent']
        
        for dataset_type in dataset_types:
            try:
                if dataset_type == 'qa':
                    items = dataset_manager.load_qa_dataset()
                elif dataset_type == 'web_search':
                    items = dataset_manager.load_search_queries()
                elif dataset_type == 'rag':
                    # For RAG, we'll analyze the ground truth queries
                    ground_truth_path = dataset_manager.dataset_path / 'rag_documents' / 'ground_truth' / 'expected_retrievals.json'
                    if ground_truth_path.exists():
                        with open(ground_truth_path, 'r') as f:
                            items = json.load(f)
                    else:
                        items = []
                elif dataset_type == 'multi_agent':
                    items = dataset_manager.load_multiagent_scenarios()
                else:
                    items = []
                
                if items:
                    # Generate statistics for this dataset
                    checker = DatasetIntegrityChecker(self.config)
                    
                    # Convert to DatasetItem format if needed
                    if dataset_type in ['qa', 'web_search'] and items and hasattr(items[0], 'to_dict'):
                        dataset_items = items
                    else:
                        # Convert raw data to DatasetItem-like format for analysis
                        dataset_items = []
                        for i, item in enumerate(items):
                            if isinstance(item, dict):
                                dataset_items.append(item)
                    
                    schema_results = checker.check_schema_compliance(dataset_items)
                    duplicate_results = checker.detect_duplicates(dataset_items)
                    completeness_results = checker.verify_completeness(dataset_type, dataset_items)
                    
                    summary['datasets'][dataset_type] = {
                        'item_count': len(items),
                        'schema_compliance': {
                            'valid_items': schema_results['valid_items'],
                            'invalid_items': schema_results['invalid_items'],
                            'compliance_rate': schema_results['valid_items'] / max(1, len(items))
                        },
                        'duplicate_analysis': {
                            'duplicate_ids': len(duplicate_results['duplicate_ids']),
                            'duplicate_content': len(duplicate_results['duplicate_content']),
                            'uniqueness_rate': duplicate_results['unique_items'] / max(1, len(items))
                        },
                        'completeness': {
                            'score': completeness_results['completeness_score'],
                            'missing_categories': completeness_results['missing_categories'],
                            'recommendations': completeness_results['recommendations']
                        }
                    }
                    
                    summary['overall_statistics']['total_items'] += len(items)
                    summary['overall_statistics']['total_datasets'] += 1
                
            except Exception as e:
                self.logger.error(f"Error analyzing {dataset_type} dataset: {e}")
                summary['datasets'][dataset_type] = {
                    'error': str(e),
                    'item_count': 0
                }
        
        # Calculate overall quality score
        if summary['overall_statistics']['total_datasets'] > 0:
            quality_scores = []
            for dataset_info in summary['datasets'].values():
                if 'completeness' in dataset_info:
                    quality_scores.append(dataset_info['completeness']['score'])
            
            if quality_scores:
                summary['overall_statistics']['quality_score'] = sum(quality_scores) / len(quality_scores)
        
        return summary


def main():
    """
    Main function to run dataset validation and generate reports.
    """
    # Initialize components
    config = DatasetConfig()
    dataset_manager = DatasetManager(config.dataset_root)
    stats_generator = DatasetStatisticsGenerator(config)
    
    # Generate comprehensive dataset summary
    summary = stats_generator.generate_dataset_summary(dataset_manager)
    
    # Save summary report
    report_path = config.dataset_root / 'validation_report.json'
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Dataset validation report saved to: {report_path}")
    print(f"Overall quality score: {summary['overall_statistics']['quality_score']:.2f}")
    print(f"Total items across all datasets: {summary['overall_statistics']['total_items']}")


if __name__ == "__main__":
    main()
