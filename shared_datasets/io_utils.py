"""
Input/Output utilities for dataset import and export operations.

This module provides comprehensive import/export functionality for different
file formats with compression support and data validation.
"""

import csv
import gzip
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .core.models import DatasetItem
from .core.exceptions import (
    DatasetError,
    DatasetImportError,
    DatasetExportError,
    DatasetFormatError,
    DatasetValidationError
)
from .loaders import DatasetLoader


class DatasetIOManager:
    """
    Utility class for dataset import and export operations.
    
    This class provides methods for importing and exporting datasets
    in various formats with comprehensive error handling and validation.
    """
    
    def __init__(self, dataset_path: Union[str, Path]):
        """
        Initialize the DatasetIOManager.
        
        Args:
            dataset_path: Path to the root directory containing datasets
        """
        self.dataset_path = Path(dataset_path)
        self.logger = logging.getLogger(__name__)
        self.loader = DatasetLoader(dataset_path)
    
    def export_dataset(self, dataset_type: str, format: str, output_path: Path, 
                      data: List[Any], compress: bool = False) -> None:
        """
        Export dataset to specified format and location.
        
        Args:
            dataset_type: Type of dataset to export (qa, rag, web_search, multi_agent)
            format: Export format (json, jsonl, csv)
            output_path: Path where to save the exported data
            data: Data to export
            compress: Whether to compress the output file using gzip
            
        Raises:
            DatasetExportError: If export operation fails
        """
        if format not in ['json', 'jsonl', 'csv']:
            raise DatasetExportError(
                f"Unsupported export format: {format}",
                export_format=format
            )
        
        if not data:
            raise DatasetExportError(
                "Cannot export empty dataset",
                output_path=str(output_path),
                export_format=format
            )
        
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Adjust output path for compression
            final_output_path = output_path
            if compress:
                final_output_path = output_path.with_suffix(f"{output_path.suffix}.gz")
            
            # Export based on format
            if format == 'json':
                self._export_json(data, final_output_path, compress)
            elif format == 'jsonl':
                self._export_jsonl(data, final_output_path, compress)
            elif format == 'csv':
                self._export_csv(data, final_output_path, dataset_type, compress)
            
            self.logger.info(f"Successfully exported {len(data)} items to {final_output_path}")
            
        except Exception as e:
            if isinstance(e, DatasetExportError):
                raise
            raise DatasetExportError(
                f"Export operation failed: {str(e)}",
                output_path=str(output_path),
                export_format=format
            )
    
    def import_dataset(self, source_path: Path, format: str, dataset_type: str) -> List[Dict[str, Any]]:
        """
        Import dataset from external source with validation.
        
        Args:
            source_path: Path to the source file
            format: Source format (json, jsonl, csv)
            dataset_type: Target dataset type (qa, rag, web_search, multi_agent)
            
        Returns:
            List of imported data items
            
        Raises:
            DatasetImportError: If import operation fails
        """
        if not source_path.exists():
            raise DatasetImportError(
                f"Source file not found: {source_path}",
                source_path=str(source_path)
            )
        
        if format not in ['json', 'jsonl', 'csv']:
            raise DatasetImportError(
                f"Unsupported import format: {format}",
                source_path=str(source_path),
                import_format=format
            )
        
        try:
            # Import based on format
            if format == 'json':
                imported_data = self.loader.load_json_file(source_path)
            elif format == 'jsonl':
                imported_data = self.loader.load_jsonl_file(source_path)
            elif format == 'csv':
                imported_data = self.loader.load_csv_file(source_path)
            else:
                raise DatasetImportError(
                    f"Unsupported format: {format}",
                    source_path=str(source_path),
                    import_format=format
                )
            
            # Validate imported data
            self._validate_imported_data(imported_data, dataset_type)
            
            self.logger.info(f"Successfully imported {len(imported_data)} items from {source_path}")
            return imported_data
            
        except (DatasetError, DatasetImportError) as e:
            if isinstance(e, DatasetImportError):
                raise
            raise DatasetImportError(
                f"Import operation failed: {str(e)}",
                source_path=str(source_path),
                import_format=format
            )
        except Exception as e:
            raise DatasetImportError(
                f"Unexpected error during import: {str(e)}",
                source_path=str(source_path),
                import_format=format
            )
    
    def save_json_file(self, data: List[Dict[str, Any]], file_path: Path, 
                      create_backup: bool = True) -> None:
        """
        Save data to a JSON file safely with backup support.
        
        Args:
            data: List of dictionaries to save
            file_path: Path where to save the file
            create_backup: Whether to create a backup of existing file
            
        Raises:
            DatasetExportError: If save operation fails
        """
        try:
            # Create backup if file exists and backup is requested
            if create_backup and file_path.exists():
                backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
                file_path.rename(backup_path)
                self.logger.info(f"Created backup: {backup_path}")
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully saved {len(data)} items to {file_path}")
            
        except Exception as e:
            raise DatasetExportError(
                f"Error saving JSON file: {str(e)}",
                output_path=str(file_path),
                export_format="json"
            )
    
    def _export_json(self, data: List[Any], output_path: Path, compress: bool) -> None:
        """Export data as JSON format."""
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        if compress:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                f.write(json_data)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
    
    def _export_jsonl(self, data: List[Any], output_path: Path, compress: bool) -> None:
        """Export data as JSONL format."""
        if compress:
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    def _export_csv(self, data: List[Any], output_path: Path, dataset_type: str, compress: bool) -> None:
        """Export data as CSV format."""
        if not data:
            raise DatasetExportError(
                "Cannot export empty data to CSV",
                output_path=str(output_path),
                export_format="csv"
            )
        
        # Define column mappings for different dataset types
        fieldnames = self._get_csv_fieldnames(data, dataset_type)
        
        # Prepare data for CSV export
        csv_data = []
        for item in data:
            if isinstance(item, DatasetItem):
                row = self._dataset_item_to_csv_row(item)
            elif isinstance(item, dict):
                row = self._dict_to_csv_row(item, fieldnames)
            else:
                row = {'data': str(item)}
            csv_data.append(row)
        
        # Write CSV
        if compress:
            with gzip.open(output_path, 'wt', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
        else:
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
    
    def _get_csv_fieldnames(self, data: List[Any], dataset_type: str) -> List[str]:
        """Get appropriate fieldnames for CSV export based on dataset type."""
        if dataset_type == 'qa':
            return ['id', 'input_data', 'expected_output', 'category', 'difficulty_level', 'metadata']
        elif dataset_type == 'rag':
            return ['id', 'filename', 'content', 'format', 'size_bytes', 'domain', 'content_type']
        elif dataset_type == 'web_search':
            return ['id', 'input_data', 'expected_output', 'category', 'difficulty_level', 'metadata']
        elif dataset_type == 'multi_agent':
            return ['id', 'type', 'title', 'description', 'agent_count', 'complexity_level']
        else:
            # Fallback: use all keys from first item
            if data and isinstance(data[0], dict):
                return list(data[0].keys())
            return ['data']
    
    def _dataset_item_to_csv_row(self, item: DatasetItem) -> Dict[str, Any]:
        """Convert DatasetItem to CSV row."""
        return {
            'id': item.id,
            'input_data': json.dumps(item.input_data) if isinstance(item.input_data, dict) else str(item.input_data),
            'expected_output': json.dumps(item.expected_output) if isinstance(item.expected_output, dict) else str(item.expected_output),
            'category': item.category or '',
            'difficulty_level': item.difficulty_level or '',
            'metadata': json.dumps(item.metadata) if item.metadata else '{}'
        }
    
    def _dict_to_csv_row(self, item: Dict[str, Any], fieldnames: List[str]) -> Dict[str, Any]:
        """Convert dictionary to CSV row with specified fieldnames."""
        row = {}
        for field in fieldnames:
            value = item.get(field, '')
            if isinstance(value, (dict, list)):
                row[field] = json.dumps(value)
            else:
                row[field] = str(value) if value is not None else ''
        return row
    
    def _validate_imported_data(self, data: List[Dict[str, Any]], dataset_type: str) -> None:
        """
        Validate imported data structure.
        
        Args:
            data: Imported data to validate
            dataset_type: Type of dataset being imported
            
        Raises:
            DatasetValidationError: If validation fails
        """
        if not data:
            raise DatasetValidationError("Imported data is empty")
        
        required_fields = {
            'qa': ['id'],
            'rag': ['id', 'content'],
            'web_search': ['id'],
            'multi_agent': ['id', 'type']
        }
        
        required = required_fields.get(dataset_type, ['id'])
        validation_errors = []
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                validation_errors.append(f"Item {i}: Expected dictionary, got {type(item).__name__}")
                continue
            
            for field in required:
                if field not in item or not item[field]:
                    validation_errors.append(f"Item {i}: Missing required field '{field}'")
        
        if validation_errors:
            raise DatasetValidationError(
                f"Imported data validation failed for {dataset_type} dataset",
                validation_errors=validation_errors
            )
