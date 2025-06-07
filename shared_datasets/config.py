"""
Configuration settings for the Shared Dataset Manager.

This module defines dataset file paths, naming conventions, validation rules,
and quality thresholds used across all AI agent framework evaluations.
"""

from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class SupportedFormat(str, Enum):
    """Supported file formats for dataset import/export."""
    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    TXT = "txt"
    MD = "md"
    PDF = "pdf"
    XML = "xml"


class DatasetConfig(BaseModel):
    """
    Configuration settings for dataset management.
    
    This class defines all the configuration parameters used by the
    DatasetManager for file paths, validation rules, and quality thresholds.
    """
    
    # Base paths
    dataset_root: Path = Field(
        default=Path("shared_datasets"),
        description="Root directory for all datasets"
    )
    
    # Dataset subdirectories
    qa_dir: str = Field(
        default="qa",
        description="Directory name for Q&A datasets"
    )
    
    rag_dir: str = Field(
        default="rag_documents",
        description="Directory name for RAG documents"
    )
    
    web_search_dir: str = Field(
        default="web_search",
        description="Directory name for web search queries"
    )
    
    multi_agent_dir: str = Field(
        default="multi_agent",
        description="Directory name for multi-agent scenarios"
    )
    
    # File naming conventions
    questions_file: str = Field(
        default="questions.json",
        description="Filename for Q&A questions"
    )
    
    answers_file: str = Field(
        default="answers.json",
        description="Filename for Q&A answers"
    )
    
    metadata_file: str = Field(
        default="metadata.json",
        description="Filename for dataset metadata"
    )
    
    # Validation rules
    max_question_length: int = Field(
        default=1000,
        description="Maximum length for questions in characters"
    )
    
    max_answer_length: int = Field(
        default=5000,
        description="Maximum length for answers in characters"
    )
    
    min_confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum confidence score for answers"
    )
    
    max_confidence_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Maximum confidence score for answers"
    )
    
    # Quality thresholds
    min_dataset_size: int = Field(
        default=1,
        description="Minimum number of items in a dataset"
    )
    
    max_dataset_size: int = Field(
        default=10000,
        description="Maximum number of items in a dataset"
    )
    
    required_qa_categories: List[str] = Field(
        default=["factual", "reasoning", "scientific", "mathematical", "creative"],
        description="Required categories for Q&A datasets"
    )
    
    required_difficulty_levels: List[str] = Field(
        default=["easy", "medium", "hard"],
        description="Required difficulty levels for datasets"
    )
    
    # File format settings
    supported_import_formats: List[SupportedFormat] = Field(
        default=[SupportedFormat.JSON, SupportedFormat.JSONL, SupportedFormat.CSV],
        description="Supported formats for dataset import"
    )
    
    supported_export_formats: List[SupportedFormat] = Field(
        default=[SupportedFormat.JSON, SupportedFormat.JSONL, SupportedFormat.CSV],
        description="Supported formats for dataset export"
    )
    
    # File size limits (in MB)
    max_file_size_mb: int = Field(
        default=100,
        description="Maximum file size for dataset files in MB"
    )
    
    max_document_size_mb: int = Field(
        default=10,
        description="Maximum size for individual documents in MB"
    )
    
    # Dataset versioning
    enable_versioning: bool = Field(
        default=True,
        description="Enable dataset versioning"
    )
    
    version_format: str = Field(
        default="v{major}.{minor}.{patch}",
        description="Version format string"
    )
    
    max_backup_versions: int = Field(
        default=5,
        description="Maximum number of backup versions to keep"
    )
    
    # RAG document settings
    rag_chunk_size: int = Field(
        default=512,
        description="Default chunk size for RAG documents in tokens"
    )
    
    rag_chunk_overlap: int = Field(
        default=50,
        description="Overlap between chunks in tokens"
    )
    
    rag_supported_formats: List[SupportedFormat] = Field(
        default=[SupportedFormat.PDF, SupportedFormat.TXT, SupportedFormat.MD],
        description="Supported formats for RAG documents"
    )
    
    # Multi-agent scenario settings
    max_agents_per_scenario: int = Field(
        default=10,
        description="Maximum number of agents per scenario"
    )
    
    required_agent_roles: List[str] = Field(
        default=["coordinator", "researcher", "analyst", "synthesizer"],
        description="Common agent roles for scenarios"
    )
    
    # Web search settings
    max_search_queries: int = Field(
        default=1000,
        description="Maximum number of search queries in dataset"
    )
    
    search_query_categories: List[str] = Field(
        default=["factual", "current_events", "research", "comparison"],
        description="Categories for web search queries"
    )
    
    model_config = {
        "env_file": ".env",
        "env_prefix": "DATASET_",
        "case_sensitive": False
    }
        
    def get_qa_path(self) -> Path:
        """Get the full path to Q&A dataset directory."""
        return self.dataset_root / self.qa_dir
    
    def get_rag_path(self) -> Path:
        """Get the full path to RAG documents directory."""
        return self.dataset_root / self.rag_dir
    
    def get_web_search_path(self) -> Path:
        """Get the full path to web search directory."""
        return self.dataset_root / self.web_search_dir
    
    def get_multi_agent_path(self) -> Path:
        """Get the full path to multi-agent scenarios directory."""
        return self.dataset_root / self.multi_agent_dir
    
    def get_questions_file_path(self) -> Path:
        """Get the full path to questions file."""
        return self.get_qa_path() / self.questions_file
    
    def get_answers_file_path(self) -> Path:
        """Get the full path to answers file."""
        return self.get_qa_path() / self.answers_file
    
    def get_metadata_file_path(self, dataset_type: str) -> Path:
        """
        Get the full path to metadata file for a specific dataset type.
        
        Args:
            dataset_type: Type of dataset (qa, rag, web_search, multi_agent)
            
        Returns:
            Path to the metadata file
        """
        if dataset_type == "qa":
            return self.get_qa_path() / self.metadata_file
        elif dataset_type == "rag":
            return self.get_rag_path() / self.metadata_file
        elif dataset_type == "web_search":
            return self.get_web_search_path() / self.metadata_file
        elif dataset_type == "multi_agent":
            return self.get_multi_agent_path() / self.metadata_file
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    def validate_file_size(self, file_path: Path) -> bool:
        """
        Validate that a file is within size limits.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file size is acceptable, False otherwise
        """
        if not file_path.exists():
            return False
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        return file_size_mb <= self.max_file_size_mb
    
    def is_supported_format(self, file_format: str, operation: str = "import") -> bool:
        """
        Check if a file format is supported for the given operation.
        
        Args:
            file_format: File format to check
            operation: Operation type ("import" or "export")
            
        Returns:
            True if format is supported, False otherwise
        """
        if operation == "import":
            return SupportedFormat(file_format) in self.supported_import_formats
        elif operation == "export":
            return SupportedFormat(file_format) in self.supported_export_formats
        else:
            raise ValueError(f"Unknown operation: {operation}")


# Global configuration instance
config = DatasetConfig()


def get_config() -> DatasetConfig:
    """Get the global dataset configuration instance."""
    return config
