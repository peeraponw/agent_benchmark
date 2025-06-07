"""
Configuration settings for the evaluation framework.

This module provides centralized configuration for evaluation timeouts,
metric parameters, cost calculation rates, and export formats.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
import json
try:
    from pydantic import BaseModel, Field, validator
except ImportError:
    # Fallback for older Pydantic versions
    from pydantic import BaseModel, Field
    from pydantic import validator


class EvaluationConfig(BaseModel):
    """
    Configuration settings for evaluation framework.
    """
    # Timeout settings
    default_timeout_seconds: int = Field(default=300, ge=1, le=3600, description="Default timeout in seconds (5 minutes)")
    max_timeout_seconds: int = Field(default=1800, ge=60, le=7200, description="Maximum timeout in seconds (30 minutes)")
    retry_timeout_seconds: int = Field(default=60, ge=1, le=600, description="Retry timeout in seconds (1 minute)")

    # Performance monitoring settings
    performance_sampling_interval: float = Field(default=0.1, gt=0.0, le=10.0, description="Performance sampling interval in seconds")
    enable_disk_io_monitoring: bool = Field(default=False, description="Enable disk I/O monitoring")
    enable_network_io_monitoring: bool = Field(default=False, description="Enable network I/O monitoring")

    # Quality metrics settings
    semantic_similarity_model: str = Field(default="all-MiniLM-L6-v2", min_length=1, description="Sentence transformer model name")
    bleu_max_n: int = Field(default=4, ge=1, le=10, description="Maximum n-gram size for BLEU score")
    rouge_types: List[str] = Field(default=['rouge1', 'rouge2', 'rougeL'], description="ROUGE metric types to calculate")
    factual_accuracy_use_stemming: bool = Field(default=True, description="Use stemming for factual accuracy evaluation")

    # Cost tracking settings
    enable_cost_tracking: bool = Field(default=True, description="Enable API cost tracking")
    cost_update_interval_hours: int = Field(default=24, ge=1, le=168, description="Cost update interval in hours")
    default_currency: str = Field(default="USD", min_length=3, max_length=3, description="Default currency code")

    # Export settings
    default_export_format: str = Field(default="json", description="Default export format")
    export_include_raw_output: bool = Field(default=False, description="Include raw output in exports")
    export_include_metadata: bool = Field(default=True, description="Include metadata in exports")
    max_export_file_size_mb: int = Field(default=100, ge=1, le=1000, description="Maximum export file size in MB")

    # Retry settings
    max_retries: int = Field(default=3, ge=0, le=10, description="Maximum number of retries")
    retry_delay_seconds: float = Field(default=1.0, ge=0.1, le=60.0, description="Retry delay in seconds")
    exponential_backoff: bool = Field(default=True, description="Use exponential backoff for retries")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_to_file: bool = Field(default=True, description="Enable logging to file")
    log_file_path: str = Field(default="evaluation.log", min_length=1, description="Log file path")

    # Framework-specific settings
    framework_configs: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Framework-specific configurations")

    @validator('default_currency')
    def validate_currency(cls, v):
        """Ensure currency is a valid 3-letter code."""
        if not v.isalpha():
            raise ValueError('Currency must be alphabetic')
        return v.upper()

    @validator('default_export_format')
    def validate_export_format(cls, v):
        """Ensure export format is supported."""
        valid_formats = ['json', 'csv', 'html']
        if v.lower() not in valid_formats:
            raise ValueError(f'Export format must be one of: {valid_formats}')
        return v.lower()

    @validator('log_level')
    def validate_log_level(cls, v):
        """Ensure log level is valid."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()

    @validator('rouge_types')
    def validate_rouge_types(cls, v):
        """Ensure ROUGE types are valid."""
        valid_types = ['rouge1', 'rouge2', 'rougeL', 'rougeLsum']
        for rouge_type in v:
            if rouge_type not in valid_types:
                raise ValueError(f'Invalid ROUGE type: {rouge_type}. Valid types: {valid_types}')
        return v

    @validator('max_timeout_seconds')
    def validate_max_timeout(cls, v, values):
        """Ensure max timeout is greater than default timeout."""
        if 'default_timeout_seconds' in values and v < values['default_timeout_seconds']:
            raise ValueError('Max timeout must be greater than or equal to default timeout')
        return v

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"  # Don't allow extra fields


class ConfigManager:
    """
    Manager for loading and saving evaluation configuration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config_path = Path(config_path) if config_path else None
        self._config = EvaluationConfig()
        
        if self.config_path and self.config_path.exists():
            self.load_config()
    
    @property
    def config(self) -> EvaluationConfig:
        """Get current configuration."""
        return self._config
    
    def load_config(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        if config_path:
            self.config_path = Path(config_path)
        
        if not self.config_path or not self.config_path.exists():
            return
        
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.suffix.lower() == '.yaml' or self.config_path.suffix.lower() == '.yml':
                    config_data = yaml.safe_load(f)
                elif self.config_path.suffix.lower() == '.json':
                    config_data = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {self.config_path.suffix}")
            
            # Update configuration with loaded data
            self._update_config_from_dict(config_data)
            
        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_path}: {e}")
    
    def save_config(self, config_path: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save configuration file (optional)
        """
        if config_path:
            self.config_path = Path(config_path)
        
        if not self.config_path:
            raise ValueError("No config path specified")
        
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert config to dictionary
        config_dict = self._config_to_dict()
        
        try:
            with open(self.config_path, 'w') as f:
                if self.config_path.suffix.lower() == '.yaml' or self.config_path.suffix.lower() == '.yml':
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                elif self.config_path.suffix.lower() == '.json':
                    json.dump(config_dict, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config file format: {self.config_path.suffix}")
                    
        except Exception as e:
            print(f"Error: Failed to save config to {self.config_path}: {e}")
            raise
    
    def update_config(self, **kwargs) -> None:
        """
        Update configuration settings.

        Args:
            **kwargs: Configuration parameters to update
        """
        try:
            # Create updated config dict
            current_dict = self._config.dict()
            current_dict.update(kwargs)
            # Validate and create new config
            self._config = EvaluationConfig(**current_dict)
        except Exception as e:
            print(f"Error updating configuration: {e}")
            raise
    
    def get_framework_config(self, framework_name: str) -> Dict[str, Any]:
        """
        Get framework-specific configuration.
        
        Args:
            framework_name: Name of the framework
            
        Returns:
            Framework-specific configuration dictionary
        """
        return self._config.framework_configs.get(framework_name, {})
    
    def set_framework_config(self, framework_name: str, config: Dict[str, Any]) -> None:
        """
        Set framework-specific configuration.
        
        Args:
            framework_name: Name of the framework
            config: Configuration dictionary
        """
        self._config.framework_configs[framework_name] = config
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        # Create a new config instance with updated data
        current_dict = self._config.dict()
        current_dict.update(config_data)
        self._config = EvaluationConfig(**current_dict)

    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.dict()


# Global configuration manager instance
_config_manager = ConfigManager()


def get_config() -> EvaluationConfig:
    """
    Get the global evaluation configuration.
    
    Returns:
        Current evaluation configuration
    """
    return _config_manager.config


def load_config(config_path: str) -> None:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to configuration file
    """
    _config_manager.load_config(config_path)


def save_config(config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config_path: Path to save configuration file
    """
    _config_manager.save_config(config_path)


def update_config(**kwargs) -> None:
    """
    Update global configuration settings.
    
    Args:
        **kwargs: Configuration parameters to update
    """
    _config_manager.update_config(**kwargs)


def get_framework_config(framework_name: str) -> Dict[str, Any]:
    """
    Get framework-specific configuration.
    
    Args:
        framework_name: Name of the framework
        
    Returns:
        Framework-specific configuration dictionary
    """
    return _config_manager.get_framework_config(framework_name)


def set_framework_config(framework_name: str, config: Dict[str, Any]) -> None:
    """
    Set framework-specific configuration.
    
    Args:
        framework_name: Name of the framework
        config: Configuration dictionary
    """
    _config_manager.set_framework_config(framework_name, config)


# Default configuration values for different use cases
DEFAULT_QA_CONFIG = {
    "timeout_seconds": 60,
    "enable_bleu": True,
    "enable_rouge": True,
    "enable_semantic_similarity": True,
    "enable_factual_accuracy": True,
    "semantic_model": "all-MiniLM-L6-v2"
}

DEFAULT_RAG_CONFIG = {
    "timeout_seconds": 120,
    "enable_retrieval_metrics": True,
    "enable_context_relevance": True,
    "enable_groundedness": True,
    "context_relevance_threshold": 0.5,
    "semantic_model": "all-MiniLM-L6-v2"
}

DEFAULT_SEARCH_CONFIG = {
    "timeout_seconds": 180,
    "enable_credibility": True,
    "enable_freshness": True,
    "enable_relevance": True,
    "max_age_days": 365,
    "semantic_model": "all-MiniLM-L6-v2"
}

# Cost calculation rates for OpenRouter (updated regularly)
API_COST_RATES = {
    "openrouter": {
        # Default models for comparison project
        "anthropic/claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
        "google/gemini-2.0-flash-exp": {"input": 0.00035, "output": 0.00105},
        "deepseek/deepseek-r1": {"input": 0.0014, "output": 0.0028},

        # Additional popular models
        "anthropic/claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "anthropic/claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "openai/gpt-4": {"input": 0.03, "output": 0.06},
        "openai/gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "openai/gpt-4o": {"input": 0.005, "output": 0.015},
        "openai/gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "google/gemini-pro": {"input": 0.0005, "output": 0.0015},
        "google/gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
        "meta-llama/llama-3.1-70b-instruct": {"input": 0.0009, "output": 0.0009},
        "meta-llama/llama-3.1-8b-instruct": {"input": 0.00018, "output": 0.00018},
        "mistralai/mistral-large": {"input": 0.003, "output": 0.009},
        "cohere/command-r-plus": {"input": 0.003, "output": 0.015}
    },
    "custom": {
        "custom-model": {"input": 0.001, "output": 0.002}
    }
}

# Export format configurations
EXPORT_FORMATS = {
    "json": {
        "extension": ".json",
        "mime_type": "application/json",
        "supports_nested_data": True
    },
    "csv": {
        "extension": ".csv",
        "mime_type": "text/csv",
        "supports_nested_data": False
    },
    "html": {
        "extension": ".html",
        "mime_type": "text/html",
        "supports_nested_data": True
    }
}
