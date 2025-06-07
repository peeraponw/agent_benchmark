"""
Custom exception classes for dataset management.

This module provides specialized exception classes for different types of
dataset-related errors, enabling better error handling and user feedback.
"""

from typing import Optional, Any, Dict, List


class DatasetError(Exception):
    """
    Base exception class for all dataset-related errors.
    
    This is the parent class for all dataset management exceptions,
    providing common functionality and error context.
    """
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize the DatasetError.
        
        Args:
            message: Human-readable error message
            context: Additional context information about the error
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        """Return a formatted error message with context."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (Context: {context_str})"
        return self.message


class DatasetValidationError(DatasetError):
    """
    Exception raised when dataset validation fails.
    
    This exception is raised when data doesn't meet the required schema,
    format, or business logic constraints.
    """
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 value: Optional[Any] = None, validation_errors: Optional[List[str]] = None):
        """
        Initialize the DatasetValidationError.
        
        Args:
            message: Human-readable error message
            field: Name of the field that failed validation
            value: The invalid value that caused the error
            validation_errors: List of specific validation error messages
        """
        context = {}
        if field:
            context['field'] = field
        if value is not None:
            context['value'] = str(value)[:100]  # Truncate long values
        if validation_errors:
            context['validation_errors'] = validation_errors
        
        super().__init__(message, context)
        self.field = field
        self.value = value
        self.validation_errors = validation_errors or []


class DatasetNotFoundError(DatasetError):
    """
    Exception raised when a requested dataset or dataset item is not found.
    
    This exception is raised when attempting to access datasets, files,
    or specific dataset items that don't exist.
    """
    
    def __init__(self, message: str, dataset_type: Optional[str] = None, 
                 dataset_id: Optional[str] = None, file_path: Optional[str] = None):
        """
        Initialize the DatasetNotFoundError.
        
        Args:
            message: Human-readable error message
            dataset_type: Type of dataset that was not found
            dataset_id: ID of the specific dataset item that was not found
            file_path: Path to the file that was not found
        """
        context = {}
        if dataset_type:
            context['dataset_type'] = dataset_type
        if dataset_id:
            context['dataset_id'] = dataset_id
        if file_path:
            context['file_path'] = file_path
        
        super().__init__(message, context)
        self.dataset_type = dataset_type
        self.dataset_id = dataset_id
        self.file_path = file_path


class DatasetFormatError(DatasetError):
    """
    Exception raised when dataset format is invalid or unsupported.
    
    This exception is raised when files have invalid JSON, unsupported
    formats, or don't match expected structure.
    """
    
    def __init__(self, message: str, format_type: Optional[str] = None, 
                 file_path: Optional[str] = None, line_number: Optional[int] = None):
        """
        Initialize the DatasetFormatError.
        
        Args:
            message: Human-readable error message
            format_type: The format that was expected or failed
            file_path: Path to the file with format issues
            line_number: Line number where the format error occurred
        """
        context = {}
        if format_type:
            context['format_type'] = format_type
        if file_path:
            context['file_path'] = file_path
        if line_number:
            context['line_number'] = line_number
        
        super().__init__(message, context)
        self.format_type = format_type
        self.file_path = file_path
        self.line_number = line_number


class DatasetImportError(DatasetError):
    """
    Exception raised when dataset import operations fail.
    
    This exception is raised when importing data from external sources
    fails due to format issues, validation errors, or file access problems.
    """
    
    def __init__(self, message: str, source_path: Optional[str] = None, 
                 import_format: Optional[str] = None, items_processed: Optional[int] = None):
        """
        Initialize the DatasetImportError.
        
        Args:
            message: Human-readable error message
            source_path: Path to the source file being imported
            import_format: Format of the import file
            items_processed: Number of items successfully processed before error
        """
        context = {}
        if source_path:
            context['source_path'] = source_path
        if import_format:
            context['import_format'] = import_format
        if items_processed is not None:
            context['items_processed'] = items_processed
        
        super().__init__(message, context)
        self.source_path = source_path
        self.import_format = import_format
        self.items_processed = items_processed


class DatasetExportError(DatasetError):
    """
    Exception raised when dataset export operations fail.
    
    This exception is raised when exporting data to external formats
    fails due to format issues, file access problems, or data conversion errors.
    """
    
    def __init__(self, message: str, output_path: Optional[str] = None, 
                 export_format: Optional[str] = None, items_processed: Optional[int] = None):
        """
        Initialize the DatasetExportError.
        
        Args:
            message: Human-readable error message
            output_path: Path where the export was being written
            export_format: Format of the export file
            items_processed: Number of items successfully processed before error
        """
        context = {}
        if output_path:
            context['output_path'] = output_path
        if export_format:
            context['export_format'] = export_format
        if items_processed is not None:
            context['items_processed'] = items_processed
        
        super().__init__(message, context)
        self.output_path = output_path
        self.export_format = export_format
        self.items_processed = items_processed


def create_user_friendly_error_message(error: DatasetError) -> str:
    """
    Create a user-friendly error message with suggestions for resolution.
    
    Args:
        error: The dataset error to format
        
    Returns:
        Formatted error message with suggestions
    """
    base_message = str(error)
    suggestions = []
    
    if isinstance(error, DatasetValidationError):
        suggestions.extend([
            "• Check that all required fields are present and have valid values",
            "• Verify that data types match the expected schema",
            "• Use the dataset validator to identify specific validation issues"
        ])
        if error.field:
            suggestions.append(f"• Focus on fixing the '{error.field}' field")
    
    elif isinstance(error, DatasetNotFoundError):
        suggestions.extend([
            "• Verify that the dataset path is correct",
            "• Check that all required dataset files exist",
            "• Run the structure validation script to identify missing files"
        ])
        if error.file_path:
            suggestions.append(f"• Create the missing file: {error.file_path}")
    
    elif isinstance(error, DatasetFormatError):
        suggestions.extend([
            "• Validate JSON syntax using a JSON validator",
            "• Check that file encoding is UTF-8",
            "• Verify that the file structure matches the expected format"
        ])
        if error.line_number:
            suggestions.append(f"• Check line {error.line_number} for syntax errors")
    
    elif isinstance(error, DatasetImportError):
        suggestions.extend([
            "• Verify that the source file exists and is readable",
            "• Check that the import format is supported (json, jsonl, csv)",
            "• Validate the source data structure before importing"
        ])
    
    elif isinstance(error, DatasetExportError):
        suggestions.extend([
            "• Verify that the output directory exists and is writable",
            "• Check available disk space",
            "• Ensure the export format is supported"
        ])
    
    if suggestions:
        suggestion_text = "\n".join(suggestions)
        return f"{base_message}\n\nSuggestions:\n{suggestion_text}"
    
    return base_message
