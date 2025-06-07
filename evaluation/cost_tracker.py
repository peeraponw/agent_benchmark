"""
API cost tracking system for AI agent framework evaluation.

This module provides comprehensive cost tracking for various LLM API providers
including OpenAI, Anthropic, Google, and others with usage aggregation and reporting.
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json
from enum import Enum
try:
    from pydantic import BaseModel, Field, validator
except ImportError:
    # Fallback for older Pydantic versions
    from pydantic import BaseModel, Field
    from pydantic import validator


class APIProvider(Enum):
    """Enumeration of supported API providers."""
    OPENROUTER = "openrouter"
    CUSTOM = "custom"


class APIUsage(BaseModel):
    """
    Record of API usage for cost calculation.
    """
    provider: APIProvider = Field(..., description="API provider used")
    model: str = Field(..., min_length=1, description="Model name used")
    input_tokens: int = Field(..., ge=0, description="Number of input tokens")
    output_tokens: int = Field(..., ge=0, description="Number of output tokens")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of usage")
    request_id: Optional[str] = Field(default=None, description="Optional request identifier")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @validator('model')
    def validate_model_name(cls, v):
        """Ensure model name is not empty."""
        if not v.strip():
            raise ValueError('Model name cannot be empty')
        return v.strip()

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CostBreakdown(BaseModel):
    """
    Detailed cost breakdown for API usage.
    """
    provider: APIProvider = Field(..., description="API provider")
    model: str = Field(..., min_length=1, description="Model name")
    input_cost: float = Field(..., ge=0.0, description="Cost for input tokens")
    output_cost: float = Field(..., ge=0.0, description="Cost for output tokens")
    total_cost: float = Field(..., ge=0.0, description="Total cost")
    input_tokens: int = Field(..., ge=0, description="Number of input tokens")
    output_tokens: int = Field(..., ge=0, description="Number of output tokens")
    input_rate_per_1k: float = Field(..., ge=0.0, description="Input rate per 1K tokens")
    output_rate_per_1k: float = Field(..., ge=0.0, description="Output rate per 1K tokens")
    currency: str = Field(default="USD", description="Currency code")

    @validator('total_cost')
    def validate_total_cost(cls, v, values):
        """Ensure total cost equals input + output costs."""
        if 'input_cost' in values and 'output_cost' in values:
            expected_total = values['input_cost'] + values['output_cost']
            if abs(v - expected_total) > 0.0001:  # Allow for small floating point differences
                raise ValueError(f'Total cost {v} does not match sum of input and output costs {expected_total}')
        return v

    @validator('currency')
    def validate_currency(cls, v):
        """Ensure currency is a valid 3-letter code."""
        if len(v) != 3 or not v.isalpha():
            raise ValueError('Currency must be a 3-letter code')
        return v.upper()

    class Config:
        """Pydantic configuration."""
        validate_assignment = True


class APIUsageTracker:
    """
    Tracks API usage and calculates costs across multiple providers.
    
    Maintains up-to-date pricing information and provides detailed cost analysis.
    """
    
    def __init__(self):
        """Initialize the API usage tracker with current pricing."""
        self.usage_records: List[APIUsage] = []
        self.pricing_data = self._initialize_pricing()
    
    def _initialize_pricing(self) -> Dict[APIProvider, Dict[str, Dict[str, float]]]:
        """
        Initialize pricing data for OpenRouter and custom providers.

        Returns:
            Dictionary with pricing information per provider/model
        """
        return {
            APIProvider.OPENROUTER: {
                # OpenRouter pricing for popular models (per 1K tokens)
                "anthropic/claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
                "anthropic/claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "anthropic/claude-3-haiku": {"input": 0.00025, "output": 0.00125},
                "openai/gpt-4": {"input": 0.03, "output": 0.06},
                "openai/gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "openai/gpt-4o": {"input": 0.005, "output": 0.015},
                "openai/gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
                "openai/gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
                "google/gemini-pro": {"input": 0.0005, "output": 0.0015},
                "google/gemini-1.5-pro": {"input": 0.0035, "output": 0.0105},
                "google/gemini-1.5-flash": {"input": 0.00035, "output": 0.00105},
                "meta-llama/llama-3.1-70b-instruct": {"input": 0.0009, "output": 0.0009},
                "meta-llama/llama-3.1-8b-instruct": {"input": 0.00018, "output": 0.00018},
                "deepseek/deepseek-r1": {"input": 0.0014, "output": 0.0028},
                "deepseek/deepseek-chat": {"input": 0.00014, "output": 0.00028},
                "mistralai/mistral-large": {"input": 0.003, "output": 0.009},
                "mistralai/mistral-medium": {"input": 0.0027, "output": 0.0081},
                "cohere/command-r-plus": {"input": 0.003, "output": 0.015},
                "cohere/command-r": {"input": 0.0005, "output": 0.0015}
            },
            APIProvider.CUSTOM: {
                # Placeholder for custom provider pricing
                "custom-model": {"input": 0.001, "output": 0.002}
            }
        }
    
    def record_usage(self, 
                    provider: Union[APIProvider, str],
                    model: str,
                    input_tokens: int,
                    output_tokens: int,
                    request_id: Optional[str] = None,
                    **metadata) -> APIUsage:
        """
        Record API usage for cost tracking.
        
        Args:
            provider: API provider (enum or string)
            model: Model name used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            request_id: Optional request identifier
            **metadata: Additional metadata
            
        Returns:
            APIUsage record
        """
        if isinstance(provider, str):
            provider_lower = provider.lower()
            if provider_lower == "openrouter":
                provider = APIProvider.OPENROUTER
            else:
                provider = APIProvider.CUSTOM
        
        usage = APIUsage(
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            request_id=request_id,
            metadata=metadata
        )
        
        self.usage_records.append(usage)
        return usage
    
    def calculate_cost(self, usage: APIUsage) -> CostBreakdown:
        """
        Calculate cost for a specific API usage record.
        
        Args:
            usage: APIUsage record
            
        Returns:
            CostBreakdown with detailed cost information
        """
        provider_pricing = self.pricing_data.get(usage.provider, {})
        model_pricing = provider_pricing.get(usage.model, {"input": 0.0, "output": 0.0})
        
        input_rate = model_pricing["input"]
        output_rate = model_pricing["output"]
        
        # Calculate costs (rates are per 1K tokens)
        input_cost = (usage.input_tokens / 1000) * input_rate
        output_cost = (usage.output_tokens / 1000) * output_rate
        total_cost = input_cost + output_cost
        
        return CostBreakdown(
            provider=usage.provider,
            model=usage.model,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            input_rate_per_1k=input_rate,
            output_rate_per_1k=output_rate
        )
    
    def get_total_cost(self, 
                      provider: Optional[APIProvider] = None,
                      model: Optional[str] = None,
                      start_time: Optional[datetime] = None,
                      end_time: Optional[datetime] = None) -> float:
        """
        Calculate total cost for filtered usage records.
        
        Args:
            provider: Filter by specific provider
            model: Filter by specific model
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            Total cost in USD
        """
        filtered_records = self._filter_records(provider, model, start_time, end_time)
        
        total_cost = 0.0
        for usage in filtered_records:
            cost_breakdown = self.calculate_cost(usage)
            total_cost += cost_breakdown.total_cost
        
        return total_cost
    
    def get_usage_summary(self,
                         provider: Optional[APIProvider] = None,
                         model: Optional[str] = None,
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get comprehensive usage summary.
        
        Args:
            provider: Filter by specific provider
            model: Filter by specific model
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            Dictionary with usage statistics
        """
        filtered_records = self._filter_records(provider, model, start_time, end_time)
        
        if not filtered_records:
            return {
                "total_requests": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_cost": 0.0,
                "providers": {},
                "models": {}
            }
        
        # Aggregate statistics
        total_input_tokens = sum(r.input_tokens for r in filtered_records)
        total_output_tokens = sum(r.output_tokens for r in filtered_records)
        total_cost = self.get_total_cost(provider, model, start_time, end_time)
        
        # Group by provider
        providers = {}
        for usage in filtered_records:
            provider_name = usage.provider.value
            if provider_name not in providers:
                providers[provider_name] = {
                    "requests": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0.0
                }
            
            providers[provider_name]["requests"] += 1
            providers[provider_name]["input_tokens"] += usage.input_tokens
            providers[provider_name]["output_tokens"] += usage.output_tokens
            providers[provider_name]["cost"] += self.calculate_cost(usage).total_cost
        
        # Group by model
        models = {}
        for usage in filtered_records:
            model_name = usage.model
            if model_name not in models:
                models[model_name] = {
                    "requests": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0.0,
                    "provider": usage.provider.value
                }
            
            models[model_name]["requests"] += 1
            models[model_name]["input_tokens"] += usage.input_tokens
            models[model_name]["output_tokens"] += usage.output_tokens
            models[model_name]["cost"] += self.calculate_cost(usage).total_cost
        
        return {
            "total_requests": len(filtered_records),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_cost": total_cost,
            "providers": providers,
            "models": models,
            "time_range": {
                "start": min(r.timestamp for r in filtered_records).isoformat(),
                "end": max(r.timestamp for r in filtered_records).isoformat()
            }
        }
    
    def compare_providers(self, 
                         input_tokens: int,
                         output_tokens: int,
                         models: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        """
        Compare costs across different providers for given token usage.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            models: Optional list of specific models to compare
            
        Returns:
            Dictionary with cost comparison across providers
        """
        comparison = {}
        
        for provider, provider_pricing in self.pricing_data.items():
            comparison[provider.value] = {}
            
            for model, pricing in provider_pricing.items():
                if models and model not in models:
                    continue
                
                input_cost = (input_tokens / 1000) * pricing["input"]
                output_cost = (output_tokens / 1000) * pricing["output"]
                total_cost = input_cost + output_cost
                
                comparison[provider.value][model] = {
                    "input_cost": input_cost,
                    "output_cost": output_cost,
                    "total_cost": total_cost,
                    "input_rate": pricing["input"],
                    "output_rate": pricing["output"]
                }
        
        return comparison
    
    def export_usage_data(self, format_type: str = "json") -> str:
        """
        Export usage data in specified format.
        
        Args:
            format_type: Export format ("json" or "csv")
            
        Returns:
            Formatted usage data as string
        """
        if format_type.lower() == "json":
            return self._export_json()
        elif format_type.lower() == "csv":
            return self._export_csv()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def update_pricing(self, 
                      provider: APIProvider,
                      model: str,
                      input_rate: float,
                      output_rate: float) -> None:
        """
        Update pricing information for a specific provider/model.
        
        Args:
            provider: API provider
            model: Model name
            input_rate: Input token rate per 1K tokens
            output_rate: Output token rate per 1K tokens
        """
        if provider not in self.pricing_data:
            self.pricing_data[provider] = {}
        
        self.pricing_data[provider][model] = {
            "input": input_rate,
            "output": output_rate
        }
    
    def _filter_records(self,
                       provider: Optional[APIProvider] = None,
                       model: Optional[str] = None,
                       start_time: Optional[datetime] = None,
                       end_time: Optional[datetime] = None) -> List[APIUsage]:
        """Filter usage records based on criteria."""
        filtered = self.usage_records
        
        if provider:
            filtered = [r for r in filtered if r.provider == provider]
        
        if model:
            filtered = [r for r in filtered if r.model == model]
        
        if start_time:
            filtered = [r for r in filtered if r.timestamp >= start_time]
        
        if end_time:
            filtered = [r for r in filtered if r.timestamp <= end_time]
        
        return filtered
    
    def _export_json(self) -> str:
        """Export usage data as JSON."""
        data = {
            "usage_records": [
                {
                    **usage.dict(),
                    "cost": self.calculate_cost(usage).total_cost
                }
                for usage in self.usage_records
            ],
            "summary": self.get_usage_summary(),
            "pricing_data": {
                provider.value: models
                for provider, models in self.pricing_data.items()
            }
        }
        return json.dumps(data, indent=2, default=str)
    
    def _export_csv(self) -> str:
        """Export usage data as CSV."""
        lines = [
            "timestamp,provider,model,input_tokens,output_tokens,input_cost,output_cost,total_cost,request_id"
        ]
        
        for usage in self.usage_records:
            cost_breakdown = self.calculate_cost(usage)
            lines.append(
                f"{usage.timestamp.isoformat()},"
                f"{usage.provider.value},"
                f"{usage.model},"
                f"{usage.input_tokens},"
                f"{usage.output_tokens},"
                f"{cost_breakdown.input_cost:.6f},"
                f"{cost_breakdown.output_cost:.6f},"
                f"{cost_breakdown.total_cost:.6f},"
                f"{usage.request_id or ''}"
            )
        
        return "\n".join(lines)
