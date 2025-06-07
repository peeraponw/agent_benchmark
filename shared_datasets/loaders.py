"""
Dataset loading utilities for different file formats.

This module provides specialized loaders for different file formats and
dataset types, with comprehensive error handling and validation.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .core.exceptions import (
    DatasetError,
    DatasetNotFoundError,
    DatasetFormatError
)


class DatasetLoader:
    """
    Utility class for loading datasets from various file formats.
    
    This class provides methods for loading and parsing different file formats
    with comprehensive error handling and validation.
    """
    
    def __init__(self, dataset_path: Union[str, Path]):
        """
        Initialize the DatasetLoader.
        
        Args:
            dataset_path: Path to the root directory containing datasets
        """
        self.dataset_path = Path(dataset_path)
        self.logger = logging.getLogger(__name__)
        self._validate_dataset_path()
    
    def _validate_dataset_path(self) -> None:
        """Validate that the dataset path exists and is accessible."""
        if not self.dataset_path.exists():
            raise DatasetNotFoundError(
                f"Dataset path does not exist: {self.dataset_path}",
                file_path=str(self.dataset_path)
            )
        
        if not self.dataset_path.is_dir():
            raise DatasetNotFoundError(
                f"Dataset path is not a directory: {self.dataset_path}",
                file_path=str(self.dataset_path)
            )
        
        self.logger.info(f"DatasetLoader initialized with path: {self.dataset_path}")
    
    def load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load and parse a JSON file safely with enhanced error handling.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of dictionaries from the JSON file
            
        Raises:
            DatasetNotFoundError: If the file doesn't exist
            DatasetFormatError: If the file contains invalid JSON
        """
        if not file_path.exists():
            raise DatasetNotFoundError(
                f"JSON file not found: {file_path}",
                file_path=str(file_path)
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise DatasetFormatError(
                    f"Expected list in JSON file, got {type(data).__name__}",
                    format_type="json",
                    file_path=str(file_path)
                )
            
            self.logger.info(f"Successfully loaded {len(data)} items from {file_path}")
            return data
            
        except json.JSONDecodeError as e:
            raise DatasetFormatError(
                f"Invalid JSON in file: {str(e)}",
                format_type="json",
                file_path=str(file_path),
                line_number=getattr(e, 'lineno', None)
            )
        except UnicodeDecodeError as e:
            raise DatasetFormatError(
                f"File encoding error: {str(e)}",
                format_type="json",
                file_path=str(file_path)
            )
        except Exception as e:
            raise DatasetError(
                f"Unexpected error loading JSON file: {str(e)}",
                context={"file_path": str(file_path)}
            )
    
    def load_jsonl_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load and parse a JSONL (JSON Lines) file safely.
        
        Args:
            file_path: Path to the JSONL file
            
        Returns:
            List of dictionaries from the JSONL file
            
        Raises:
            DatasetNotFoundError: If the file doesn't exist
            DatasetFormatError: If the file contains invalid JSON lines
        """
        if not file_path.exists():
            raise DatasetNotFoundError(
                f"JSONL file not found: {file_path}",
                file_path=str(file_path)
            )
        
        data = []
        line_number = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        raise DatasetFormatError(
                            f"Invalid JSON on line {line_number}: {str(e)}",
                            format_type="jsonl",
                            file_path=str(file_path),
                            line_number=line_number
                        )
            
            self.logger.info(f"Successfully loaded {len(data)} items from JSONL file {file_path}")
            return data
            
        except UnicodeDecodeError as e:
            raise DatasetFormatError(
                f"File encoding error: {str(e)}",
                format_type="jsonl",
                file_path=str(file_path)
            )
        except Exception as e:
            if isinstance(e, DatasetFormatError):
                raise
            raise DatasetError(
                f"Unexpected error loading JSONL file: {str(e)}",
                context={"file_path": str(file_path), "line_number": line_number}
            )
    
    def load_csv_file(self, file_path: Path, fieldnames: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Load and parse a CSV file safely.
        
        Args:
            file_path: Path to the CSV file
            fieldnames: Optional list of field names (uses header row if None)
            
        Returns:
            List of dictionaries from the CSV file
            
        Raises:
            DatasetNotFoundError: If the file doesn't exist
            DatasetFormatError: If the file contains invalid CSV data
        """
        if not file_path.exists():
            raise DatasetNotFoundError(
                f"CSV file not found: {file_path}",
                file_path=str(file_path)
            )
        
        data = []
        line_number = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                # Detect if file has header
                sample = f.read(1024)
                f.seek(0)
                
                if fieldnames:
                    reader = csv.DictReader(f, fieldnames=fieldnames)
                else:
                    reader = csv.DictReader(f)
                
                for line_number, row in enumerate(reader, 1):
                    # Convert empty strings to None for consistency
                    cleaned_row = {k: (v if v != '' else None) for k, v in row.items()}
                    data.append(cleaned_row)
            
            self.logger.info(f"Successfully loaded {len(data)} items from CSV file {file_path}")
            return data
            
        except UnicodeDecodeError as e:
            raise DatasetFormatError(
                f"File encoding error: {str(e)}",
                format_type="csv",
                file_path=str(file_path)
            )
        except csv.Error as e:
            raise DatasetFormatError(
                f"CSV parsing error: {str(e)}",
                format_type="csv",
                file_path=str(file_path),
                line_number=line_number
            )
        except Exception as e:
            raise DatasetError(
                f"Unexpected error loading CSV file: {str(e)}",
                context={"file_path": str(file_path), "line_number": line_number}
            )
    
    def load_document_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single document file and extract its content and metadata.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing document content and metadata, or None if failed
            
        Raises:
            DatasetNotFoundError: If the file doesn't exist
            DatasetFormatError: If the file format is unsupported or invalid
        """
        if not file_path.exists():
            raise DatasetNotFoundError(
                f"Document file not found: {file_path}",
                file_path=str(file_path)
            )
        
        try:
            # Read file content based on extension
            content = None
            file_extension = file_path.suffix.lower()
            
            if file_extension in {'.txt', '.md'}:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
            elif file_extension in {'.csv', '.xml'}:
                # For other formats, read as text for now
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                raise DatasetFormatError(
                    f"Unsupported document format: {file_extension}",
                    format_type=file_extension.lstrip('.'),
                    file_path=str(file_path)
                )
            
            # Extract metadata
            stat = file_path.stat()
            
            document = {
                'id': str(file_path.relative_to(self.dataset_path)),
                'filename': file_path.name,
                'filepath': str(file_path),
                'content': content,
                'format': file_extension.lstrip('.'),
                'size_bytes': stat.st_size,
                'created_date': stat.st_ctime,
                'modified_date': stat.st_mtime,
                'metadata': {
                    'source': 'local_file',
                    'domain': self._infer_domain_from_path(file_path),
                    'content_type': self._infer_content_type(file_path, content)
                }
            }
            
            return document
            
        except UnicodeDecodeError as e:
            raise DatasetFormatError(
                f"File encoding error: {str(e)}",
                format_type=file_extension.lstrip('.'),
                file_path=str(file_path)
            )
        except json.JSONDecodeError as e:
            raise DatasetFormatError(
                f"Invalid JSON in document: {str(e)}",
                format_type="json",
                file_path=str(file_path),
                line_number=getattr(e, 'lineno', None)
            )
        except Exception as e:
            if isinstance(e, (DatasetNotFoundError, DatasetFormatError)):
                raise
            
            self.logger.error(f"Error loading document {file_path}: {e}")
            return None
    
    def _infer_domain_from_path(self, file_path: Path) -> str:
        """
        Infer document domain from file path structure.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Inferred domain category
        """
        path_parts = file_path.parts
        
        # Look for domain indicators in path
        domain_keywords = {
            'technology': ['tech', 'software', 'programming', 'code'],
            'business': ['business', 'finance', 'marketing', 'sales'],
            'science': ['science', 'research', 'academic', 'study'],
            'legal': ['legal', 'law', 'policy', 'regulation'],
            'education': ['education', 'learning', 'tutorial', 'guide']
        }
        
        for part in path_parts:
            part_lower = part.lower()
            for domain, keywords in domain_keywords.items():
                if any(keyword in part_lower for keyword in keywords):
                    return domain
        
        return 'general'
    
    def _infer_content_type(self, file_path: Path, content: Any) -> str:
        """
        Infer content type from file extension and content.
        
        Args:
            file_path: Path to the document
            content: Document content
            
        Returns:
            Inferred content type
        """
        extension = file_path.suffix.lower()
        
        if extension == '.md':
            return 'markdown'
        elif extension == '.json':
            return 'structured_data'
        elif extension == '.csv':
            return 'tabular_data'
        elif extension == '.xml':
            return 'markup'
        elif extension == '.txt':
            # Try to infer from content
            if isinstance(content, str):
                if content.strip().startswith(('# ', '## ', '### ')):
                    return 'markdown'
                elif '<' in content and '>' in content:
                    return 'markup'
            return 'plain_text'
        else:
            return 'unknown'
