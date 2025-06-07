"""
Core data models for dataset management.

This module contains the Pydantic models that define the structure and
validation rules for dataset items and related data structures.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum

from .exceptions import DatasetValidationError


class DifficultyLevel(str, Enum):
    """Enumeration for dataset item difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    CREATIVE = "creative"


class DatasetItem(BaseModel):
    """
    Core data model for individual dataset items.
    
    This model provides a standardized structure for all types of test data
    across different evaluation scenarios (Q&A, RAG, multi-agent, etc.).
    
    The model includes comprehensive validation to ensure data quality and
    consistency across all dataset types.
    """
    
    id: str = Field(
        ...,
        description="Unique identifier for the dataset item",
        min_length=1,
        max_length=100
    )
    
    input_data: Any = Field(
        ...,
        description="Input data for the test case - can be question, query, scenario, etc."
    )
    
    expected_output: Any = Field(
        ...,
        description="Expected output or ground truth for evaluation"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context and metadata for the dataset item"
    )
    
    difficulty_level: Optional[DifficultyLevel] = Field(
        None,
        description="Difficulty level categorization"
    )
    
    category: Optional[str] = Field(
        None,
        description="Category or type classification for grouping",
        max_length=50
    )
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """
        Validate that ID follows expected format.
        
        Args:
            v: The ID value to validate
            
        Returns:
            The validated ID
            
        Raises:
            DatasetValidationError: If ID format is invalid
        """
        if not v or not isinstance(v, str):
            raise DatasetValidationError(
                "ID must be a non-empty string",
                field="id",
                value=v
            )

        # Check for valid ID format (alphanumeric with underscores and hyphens)
        if not v.replace('_', '').replace('-', '').isalnum():
            raise DatasetValidationError(
                "ID must contain only alphanumeric characters, underscores, and hyphens",
                field="id",
                value=v,
                validation_errors=[
                    "Use only letters, numbers, underscores (_), and hyphens (-)",
                    "Avoid spaces and special characters"
                ]
            )

        return v

    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, v):
        """
        Ensure metadata is a valid dictionary.
        
        Args:
            v: The metadata value to validate
            
        Returns:
            The validated metadata
            
        Raises:
            DatasetValidationError: If metadata is not a dictionary
        """
        if not isinstance(v, dict):
            raise DatasetValidationError(
                "Metadata must be a dictionary",
                field="metadata",
                value=v,
                validation_errors=[
                    "Provide metadata as a JSON object/dictionary",
                    "Use key-value pairs for additional information"
                ]
            )
        return v
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """
        Validate category field.
        
        Args:
            v: The category value to validate
            
        Returns:
            The validated category
            
        Raises:
            DatasetValidationError: If category is invalid
        """
        if v is not None:
            if not isinstance(v, str):
                raise DatasetValidationError(
                    "Category must be a string",
                    field="category",
                    value=v
                )
            
            if len(v.strip()) == 0:
                raise DatasetValidationError(
                    "Category cannot be empty or whitespace only",
                    field="category",
                    value=v
                )
        
        return v

    @model_validator(mode='after')
    def validate_consistency(self):
        """
        Validate consistency between fields and business logic.
        
        Returns:
            The validated model instance
            
        Raises:
            DatasetValidationError: If validation fails
        """
        validation_errors = []
        
        # Ensure input_data and expected_output are not None
        if self.input_data is None:
            validation_errors.append("input_data cannot be None")

        if self.expected_output is None:
            validation_errors.append("expected_output cannot be None")
        
        # Validate input_data structure for common types
        if isinstance(self.input_data, dict):
            if not self.input_data:
                validation_errors.append("input_data dictionary cannot be empty")
        elif isinstance(self.input_data, str):
            if len(self.input_data.strip()) == 0:
                validation_errors.append("input_data string cannot be empty or whitespace only")
        
        # Validate expected_output structure
        if isinstance(self.expected_output, dict):
            if not self.expected_output:
                validation_errors.append("expected_output dictionary cannot be empty")
        elif isinstance(self.expected_output, str):
            if len(self.expected_output.strip()) == 0:
                validation_errors.append("expected_output string cannot be empty or whitespace only")
        
        # Validate metadata consistency
        if self.metadata:
            # Check for reserved metadata keys that might conflict with model fields
            # Note: category and difficulty_level are allowed in metadata for backward compatibility
            reserved_keys = {'id', 'input_data', 'expected_output'}
            conflicting_keys = set(self.metadata.keys()) & reserved_keys
            if conflicting_keys:
                validation_errors.append(
                    f"Metadata contains reserved keys: {', '.join(conflicting_keys)}"
                )
        
        if validation_errors:
            raise DatasetValidationError(
                "Dataset item validation failed",
                validation_errors=validation_errors
            )

        return self
    
    class Config:
        """Pydantic model configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"  # Prevent additional fields
        json_schema_extra = {
            "examples": [
                {
                    "id": "qa_001",
                    "input_data": {
                        "question": "What is the capital of France?",
                        "expected_response_type": "factual"
                    },
                    "expected_output": {
                        "answer": "Paris",
                        "explanation": "Paris is the capital and largest city of France.",
                        "sources": ["https://en.wikipedia.org/wiki/Paris"],
                        "confidence": 1.0
                    },
                    "metadata": {
                        "question_type": "factual",
                        "domain": "geography"
                    },
                    "difficulty_level": "easy",
                    "category": "factual"
                }
            ]
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary.
        
        Returns:
            Dictionary representation of the dataset item
        """
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatasetItem':
        """
        Create a DatasetItem from a dictionary with enhanced error handling.
        
        Args:
            data: Dictionary containing dataset item data
            
        Returns:
            DatasetItem instance
            
        Raises:
            DatasetValidationError: If data is invalid
        """
        try:
            return cls(**data)
        except Exception as e:
            # Convert Pydantic validation errors to our custom exception
            if hasattr(e, 'errors'):
                # Pydantic ValidationError
                error_messages = []
                for error in e.errors():
                    field = '.'.join(str(loc) for loc in error['loc'])
                    message = error['msg']
                    error_messages.append(f"{field}: {message}")
                
                raise DatasetValidationError(
                    f"Failed to create DatasetItem from dictionary",
                    validation_errors=error_messages
                )
            else:
                # Other exceptions
                raise DatasetValidationError(
                    f"Failed to create DatasetItem: {str(e)}"
                )
    
    def validate_for_use_case(self, use_case_type: str) -> None:
        """
        Validate that the dataset item is suitable for a specific use case.
        
        Args:
            use_case_type: Type of use case (qa, rag, web_search, multi_agent)
            
        Raises:
            DatasetValidationError: If item is not suitable for the use case
        """
        validation_errors = []
        
        if use_case_type == "qa":
            # Q&A specific validation
            if isinstance(self.input_data, dict):
                if "question" not in self.input_data:
                    validation_errors.append("Q&A items must have 'question' in input_data")
            elif not isinstance(self.input_data, str):
                validation_errors.append("Q&A input_data must be a string or dict with 'question'")
        
        elif use_case_type == "web_search":
            # Web search specific validation
            if isinstance(self.input_data, dict):
                if "query" not in self.input_data:
                    validation_errors.append("Web search items must have 'query' in input_data")
            elif not isinstance(self.input_data, str):
                validation_errors.append("Web search input_data must be a string or dict with 'query'")
        
        elif use_case_type == "rag":
            # RAG specific validation
            if isinstance(self.expected_output, dict):
                if "expected_sources" not in self.expected_output:
                    validation_errors.append("RAG items should have 'expected_sources' in expected_output")
        
        elif use_case_type == "multi_agent":
            # Multi-agent specific validation
            if isinstance(self.input_data, dict):
                if "required_agents" not in self.input_data:
                    validation_errors.append("Multi-agent items should have 'required_agents' in input_data")
        
        if validation_errors:
            raise DatasetValidationError(
                f"Dataset item not suitable for {use_case_type} use case",
                validation_errors=validation_errors
            )
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the dataset item for reporting.
        
        Returns:
            Dictionary containing item summary information
        """
        summary = {
            "id": self.id,
            "category": self.category,
            "difficulty_level": self.difficulty_level,
            "has_metadata": bool(self.metadata),
            "metadata_keys": list(self.metadata.keys()) if self.metadata else []
        }
        
        # Add type information for input_data and expected_output
        summary["input_data_type"] = type(self.input_data).__name__
        summary["expected_output_type"] = type(self.expected_output).__name__
        
        # Add size information for string data
        if isinstance(self.input_data, str):
            summary["input_data_length"] = len(self.input_data)
        if isinstance(self.expected_output, str):
            summary["expected_output_length"] = len(self.expected_output)
        
        return summary
