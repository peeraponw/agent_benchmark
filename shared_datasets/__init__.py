"""
Shared Dataset Management Package for AI Agent Framework Comparison.

This package provides comprehensive dataset management functionality with a
modular architecture for loading, validating, and managing test datasets.

Main Components:
- DatasetManager: Main interface for dataset operations
- DatasetItem: Core data model for dataset items
- DatasetLoader: File loading utilities
- DatasetStatistics: Statistical analysis tools
- DatasetIOManager: Import/export functionality
- Custom exceptions for better error handling

Usage:
    from shared_datasets import DatasetManager, DatasetItem
    
    manager = DatasetManager("path/to/datasets")
    qa_items = manager.load_qa_dataset()
    stats = manager.get_comprehensive_stats()
"""

# Import main classes for easy access
from .dataset_manager import DatasetManager
from .core.models import DatasetItem, DifficultyLevel
from .core.exceptions import (
    DatasetError,
    DatasetValidationError,
    DatasetNotFoundError,
    DatasetFormatError,
    DatasetImportError,
    DatasetExportError
)
from .loaders import DatasetLoader
from .statistics import DatasetStatistics
from .io_utils import DatasetIOManager

__version__ = "1.0.0"
__author__ = "AI Agent Framework Comparison Project"

__all__ = [
    # Main interface
    'DatasetManager',
    
    # Core models
    'DatasetItem',
    'DifficultyLevel',
    
    # Modular components
    'DatasetLoader',
    'DatasetStatistics', 
    'DatasetIOManager',
    
    # Exceptions
    'DatasetError',
    'DatasetValidationError',
    'DatasetNotFoundError',
    'DatasetFormatError',
    'DatasetImportError',
    'DatasetExportError'
]
