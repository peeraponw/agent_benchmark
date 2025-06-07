"""
Dataset validation and quality control for AI Agent Framework Comparison.

This module provides comprehensive validation and quality control functionality
for all types of datasets used in the evaluation framework.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import Counter, defaultdict
from pydantic import ValidationError

from .config import DatasetConfig


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.stats: Dict[str, Any] = {}
    
    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)
    
    def add_info(self, message: str) -> None:
        """Add an info message."""
        self.info.append(message)
    
    def add_stat(self, key: str, value: Any) -> None:
        """Add a statistic."""
        self.stats[key] = value
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of validation results."""
        return {
            'is_valid': self.is_valid,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'info_count': len(self.info),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'stats': self.stats
        }


class DatasetValidator:
    """
    Comprehensive dataset validation and quality control.
    
    This class provides validation for all dataset types including schema validation,
    data quality checks, completeness verification, and consistency analysis.
    """
    
    def __init__(self, config: Optional[DatasetConfig] = None):
        """
        Initialize the DatasetValidator.
        
        Args:
            config: Dataset configuration instance
        """
        self.config = config or DatasetConfig()
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Set up logging for validation operations."""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def validate_dataset_items(self, items: List[Any]) -> ValidationResult:
        """
        Validate a list of DatasetItem objects.
        
        Args:
            items: List of DatasetItem objects to validate
            
        Returns:
            ValidationResult containing validation status and details
        """
        result = ValidationResult()
        
        if not items:
            result.add_error("Dataset is empty")
            return result
        
        # Basic size validation
        if len(items) < self.config.min_dataset_size:
            result.add_error(f"Dataset too small: {len(items)} < {self.config.min_dataset_size}")
        
        if len(items) > self.config.max_dataset_size:
            result.add_error(f"Dataset too large: {len(items)} > {self.config.max_dataset_size}")
        
        # Schema validation
        self._validate_schema(items, result)
        
        # Data quality checks
        self._validate_data_quality(items, result)
        
        # Completeness checks
        self._validate_completeness(items, result)
        
        # Consistency checks
        self._validate_consistency(items, result)
        
        # Duplication checks
        self._validate_duplicates(items, result)
        
        # Generate statistics
        self._generate_statistics(items, result)
        
        return result
    
    def _validate_schema(self, items: List[Any], result: ValidationResult) -> None:
        """Validate schema compliance for all items."""
        schema_errors = 0
        
        for i, item in enumerate(items):
            try:
                # Pydantic validation is already done during object creation
                # Additional custom validations can be added here
                if not item.id:
                    result.add_error(f"Item {i}: Missing or empty ID")
                    schema_errors += 1
                
                if item.input_data is None:
                    result.add_error(f"Item {i} ({item.id}): input_data is None")
                    schema_errors += 1
                
                if item.expected_output is None:
                    result.add_error(f"Item {i} ({item.id}): expected_output is None")
                    schema_errors += 1
                    
            except ValidationError as e:
                result.add_error(f"Item {i}: Schema validation failed: {e}")
                schema_errors += 1
        
        result.add_stat('schema_errors', schema_errors)
        
        if schema_errors == 0:
            result.add_info("All items pass schema validation")
    
    def _validate_data_quality(self, items: List[Any], result: ValidationResult) -> None:
        """Validate data quality for all items."""
        quality_issues = 0
        
        for item in items:
            # Check for empty or trivial content
            if isinstance(item.input_data, str) and len(item.input_data.strip()) < 5:
                result.add_warning(f"Item {item.id}: Input data seems too short")
                quality_issues += 1
            
            if isinstance(item.expected_output, str) and len(item.expected_output.strip()) < 2:
                result.add_warning(f"Item {item.id}: Expected output seems too short")
                quality_issues += 1
            
            # Check for reasonable content length
            if isinstance(item.input_data, str) and len(item.input_data) > self.config.max_question_length:
                result.add_warning(f"Item {item.id}: Input data exceeds recommended length")
                quality_issues += 1
            
            if isinstance(item.expected_output, str) and len(item.expected_output) > self.config.max_answer_length:
                result.add_warning(f"Item {item.id}: Expected output exceeds recommended length")
                quality_issues += 1
        
        result.add_stat('quality_issues', quality_issues)
    
    def _validate_completeness(self, items: List[Any], result: ValidationResult) -> None:
        """Validate dataset completeness."""
        # Check category distribution
        categories = [item.category for item in items if item.category]
        category_counts = Counter(categories)
        
        missing_categories = set(self.config.required_qa_categories) - set(categories)
        if missing_categories:
            result.add_warning(f"Missing required categories: {missing_categories}")
        
        # Check difficulty level distribution
        difficulty_levels = [item.difficulty_level for item in items if item.difficulty_level]
        difficulty_counts = Counter(difficulty_levels)
        
        missing_difficulties = set(self.config.required_difficulty_levels) - set(difficulty_levels)
        if missing_difficulties:
            result.add_warning(f"Missing required difficulty levels: {missing_difficulties}")
        
        result.add_stat('category_distribution', dict(category_counts))
        result.add_stat('difficulty_distribution', dict(difficulty_counts))
    
    def _validate_consistency(self, items: List[Any], result: ValidationResult) -> None:
        """Validate internal consistency."""
        consistency_issues = 0
        
        # Check for consistent metadata structure
        metadata_keys = set()
        for item in items:
            if item.metadata:
                metadata_keys.update(item.metadata.keys())
        
        # Check if all items have similar metadata structure
        for item in items:
            if item.metadata:
                missing_keys = metadata_keys - set(item.metadata.keys())
                if len(missing_keys) > len(metadata_keys) * 0.5:  # More than 50% keys missing
                    result.add_warning(f"Item {item.id}: Inconsistent metadata structure")
                    consistency_issues += 1
        
        result.add_stat('consistency_issues', consistency_issues)
    
    def _validate_duplicates(self, items: List[Any], result: ValidationResult) -> None:
        """Check for duplicate items."""
        # Check for duplicate IDs
        ids = [item.id for item in items]
        duplicate_ids = [id for id, count in Counter(ids).items() if count > 1]
        
        if duplicate_ids:
            result.add_error(f"Duplicate IDs found: {duplicate_ids}")
        
        # Check for similar content (basic check)
        input_data_strings = []
        for item in items:
            if isinstance(item.input_data, str):
                input_data_strings.append((item.id, item.input_data.lower().strip()))
            elif isinstance(item.input_data, dict) and 'question' in item.input_data:
                input_data_strings.append((item.id, str(item.input_data['question']).lower().strip()))
        
        # Simple duplicate content detection
        content_map = defaultdict(list)
        for item_id, content in input_data_strings:
            content_map[content].append(item_id)
        
        duplicate_content = {content: ids for content, ids in content_map.items() if len(ids) > 1}
        if duplicate_content:
            result.add_warning(f"Potential duplicate content found for items: {list(duplicate_content.values())}")
        
        result.add_stat('duplicate_ids', len(duplicate_ids))
        result.add_stat('duplicate_content_groups', len(duplicate_content))
    
    def _generate_statistics(self, items: List[Any], result: ValidationResult) -> None:
        """Generate comprehensive statistics."""
        result.add_stat('total_items', len(items))
        result.add_stat('items_with_metadata', sum(1 for item in items if item.metadata))
        result.add_stat('items_with_category', sum(1 for item in items if item.category))
        result.add_stat('items_with_difficulty', sum(1 for item in items if item.difficulty_level))
        
        # Content type analysis
        input_types = Counter()
        output_types = Counter()
        
        for item in items:
            input_types[type(item.input_data).__name__] += 1
            output_types[type(item.expected_output).__name__] += 1
        
        result.add_stat('input_data_types', dict(input_types))
        result.add_stat('expected_output_types', dict(output_types))
    
    def generate_quality_report(self, validation_result: ValidationResult) -> str:
        """
        Generate a human-readable quality report.
        
        Args:
            validation_result: ValidationResult from validation
            
        Returns:
            Formatted quality report string
        """
        report = []
        report.append("=== Dataset Quality Report ===\n")
        
        # Overall status
        status = "PASS" if validation_result.is_valid else "FAIL"
        report.append(f"Overall Status: {status}\n")
        
        # Summary statistics
        stats = validation_result.stats
        report.append(f"Total Items: {stats.get('total_items', 0)}")
        report.append(f"Schema Errors: {stats.get('schema_errors', 0)}")
        report.append(f"Quality Issues: {stats.get('quality_issues', 0)}")
        report.append(f"Consistency Issues: {stats.get('consistency_issues', 0)}")
        report.append(f"Duplicate IDs: {stats.get('duplicate_ids', 0)}")
        report.append("")
        
        # Distribution analysis
        if 'category_distribution' in stats:
            report.append("Category Distribution:")
            for category, count in stats['category_distribution'].items():
                report.append(f"  {category}: {count}")
            report.append("")
        
        if 'difficulty_distribution' in stats:
            report.append("Difficulty Distribution:")
            for difficulty, count in stats['difficulty_distribution'].items():
                report.append(f"  {difficulty}: {count}")
            report.append("")
        
        # Errors and warnings
        if validation_result.errors:
            report.append("ERRORS:")
            for error in validation_result.errors:
                report.append(f"  - {error}")
            report.append("")
        
        if validation_result.warnings:
            report.append("WARNINGS:")
            for warning in validation_result.warnings:
                report.append(f"  - {warning}")
            report.append("")
        
        return "\n".join(report)
