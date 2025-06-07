"""
Configuration Validation Utility for AI Agent Framework Comparison Project.

This module provides comprehensive validation for configuration files,
environment variables, and framework-specific settings with migration support.

Usage:
    uv run python shared/config_validator.py [--framework dspy] [--fix-issues]
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator


@dataclass
class ValidationIssue:
    """Represents a configuration validation issue."""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'missing', 'invalid', 'deprecated', 'security'
    field: str
    message: str
    suggestion: Optional[str] = None
    auto_fixable: bool = False


class FrameworkConfig(BaseModel):
    """Base configuration model for framework validation."""
    
    # LLM Configuration
    openrouter_api_key: Optional[str] = Field(None, description="OpenRouter API key")
    openrouter_base_url: str = Field("https://openrouter.ai/api/v1", description="OpenRouter base URL")
    default_model: str = Field("deepseek/deepseek-r1", description="Default LLM model")
    
    # Langfuse Configuration
    langfuse_public_key: Optional[str] = Field(None, description="Langfuse public key")
    langfuse_secret_key: Optional[str] = Field(None, description="Langfuse secret key")
    langfuse_host: str = Field("http://localhost:3001", description="Langfuse host URL")
    langfuse_nextauth_secret: Optional[str] = Field(None, description="Langfuse NextAuth secret")
    langfuse_salt: Optional[str] = Field(None, description="Langfuse salt")
    
    # Database Configuration
    postgres_host: str = Field("localhost", description="PostgreSQL host")
    postgres_port: int = Field(5433, description="PostgreSQL port")
    postgres_user: str = Field("langfuse_user", description="PostgreSQL user")
    postgres_password: Optional[str] = Field(None, description="PostgreSQL password")
    postgres_db: str = Field("langfuse", description="PostgreSQL database name")
    
    @field_validator('openrouter_api_key')
    @classmethod
    def validate_openrouter_key(cls, v):
        """Validate OpenRouter API key format."""
        if v and not v.startswith('sk-or-'):
            raise ValueError("OpenRouter API key must start with 'sk-or-'")
        return v
    
    @field_validator('langfuse_nextauth_secret')
    @classmethod
    def validate_nextauth_secret(cls, v):
        """Validate NextAuth secret strength."""
        if v and len(v) < 32:
            raise ValueError("NextAuth secret must be at least 32 characters")
        return v
    
    @field_validator('langfuse_salt')
    @classmethod
    def validate_salt(cls, v):
        """Validate salt format and strength."""
        if v and len(v) < 32:
            raise ValueError("Salt must be at least 32 characters")
        return v


class ConfigValidator:
    """
    Comprehensive configuration validator for AI agent frameworks.
    
    This class validates configuration files, environment variables,
    and provides migration utilities for configuration updates.
    """
    
    def __init__(self, framework: str = "dspy"):
        """
        Initialize the ConfigValidator.
        
        Args:
            framework: Framework name (dspy, crewai, pocketflow, google_adk, pydantic_ai)
        """
        self.framework = framework
        self.logger = logging.getLogger(__name__)
        self.issues: List[ValidationIssue] = []
        
        # Framework-specific paths
        self.framework_path = Path(framework)
        self.env_file = self.framework_path / ".env"
        self.env_template = self.framework_path / ".env.template"
        
        # Required environment variables by category
        self.required_vars = {
            'critical': [
                'OPENROUTER_API_KEY'
            ],
            'important': [
                'LANGFUSE_NEXTAUTH_SECRET',
                'LANGFUSE_SALT',
                'POSTGRES_PASSWORD'
            ],
            'optional': [
                'LANGFUSE_PUBLIC_KEY',
                'LANGFUSE_SECRET_KEY'
            ]
        }
    
    def validate_configuration(self) -> List[ValidationIssue]:
        """
        Perform comprehensive configuration validation.
        
        Returns:
            List of validation issues found
        """
        self.issues = []
        
        # Check if framework directory exists
        if not self.framework_path.exists():
            self.issues.append(ValidationIssue(
                severity='error',
                category='missing',
                field='framework_directory',
                message=f"Framework directory '{self.framework}' does not exist",
                suggestion=f"Create the {self.framework} directory or check the framework name"
            ))
            return self.issues
        
        # Validate environment file
        self._validate_env_file()
        
        # Validate environment variables
        self._validate_env_variables()
        
        # Validate configuration values
        self._validate_config_values()
        
        # Check for deprecated settings
        self._check_deprecated_settings()
        
        # Validate security settings
        self._validate_security_settings()
        
        return self.issues
    
    def _validate_env_file(self) -> None:
        """Validate the existence and structure of .env file."""
        if not self.env_file.exists():
            self.issues.append(ValidationIssue(
                severity='error',
                category='missing',
                field='env_file',
                message=f"Environment file not found: {self.env_file}",
                suggestion=f"Copy {self.env_template} to {self.env_file} and configure it",
                auto_fixable=True
            ))
            return
        
        # Check file permissions
        try:
            stat = self.env_file.stat()
            permissions = oct(stat.st_mode)[-3:]
            if permissions != '600':
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='security',
                    field='env_file_permissions',
                    message=f"Environment file has insecure permissions: {permissions}",
                    suggestion="Set permissions to 600: chmod 600 .env",
                    auto_fixable=True
                ))
        except Exception as e:
            self.logger.warning(f"Could not check file permissions: {e}")
    
    def _validate_env_variables(self) -> None:
        """Validate required environment variables."""
        if not self.env_file.exists():
            return
        
        # Load environment variables
        env_vars = self._load_env_file()
        
        # Check critical variables
        for var in self.required_vars['critical']:
            if var not in env_vars or not env_vars[var]:
                self.issues.append(ValidationIssue(
                    severity='error',
                    category='missing',
                    field=var,
                    message=f"Critical environment variable '{var}' is missing or empty",
                    suggestion=f"Set {var} in your .env file"
                ))
        
        # Check important variables
        for var in self.required_vars['important']:
            if var not in env_vars or not env_vars[var]:
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='missing',
                    field=var,
                    message=f"Important environment variable '{var}' is missing or empty",
                    suggestion=f"Set {var} in your .env file for full functionality"
                ))
        
        # Check for placeholder values
        self._check_placeholder_values(env_vars)
    
    def _validate_config_values(self) -> None:
        """Validate configuration values using Pydantic model."""
        if not self.env_file.exists():
            return
        
        env_vars = self._load_env_file()
        
        try:
            # Create configuration object for validation
            config_data = {
                'openrouter_api_key': env_vars.get('OPENROUTER_API_KEY'),
                'langfuse_nextauth_secret': env_vars.get('LANGFUSE_NEXTAUTH_SECRET'),
                'langfuse_salt': env_vars.get('LANGFUSE_SALT'),
                'postgres_password': env_vars.get('POSTGRES_PASSWORD'),
                'postgres_port': int(env_vars.get('POSTGRES_PORT', 5433))
            }
            
            # Validate using Pydantic model
            FrameworkConfig(**config_data)
            
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity='error',
                category='invalid',
                field='configuration',
                message=f"Configuration validation failed: {str(e)}",
                suggestion="Check your configuration values against the schema"
            ))
    
    def _check_placeholder_values(self, env_vars: Dict[str, str]) -> None:
        """Check for placeholder values that should be replaced."""
        placeholder_patterns = [
            r'your_.*_here',
            r'replace_.*',
            r'change_.*',
            r'example_.*',
            r'.*_placeholder'
        ]
        
        for var, value in env_vars.items():
            if not value:
                continue
                
            for pattern in placeholder_patterns:
                if re.search(pattern, value.lower()):
                    self.issues.append(ValidationIssue(
                        severity='error',
                        category='invalid',
                        field=var,
                        message=f"Variable '{var}' contains placeholder value: {value}",
                        suggestion=f"Replace placeholder value in {var} with actual configuration"
                    ))
                    break
    
    def _check_deprecated_settings(self) -> None:
        """Check for deprecated configuration settings."""
        if not self.env_file.exists():
            return
        
        env_vars = self._load_env_file()
        
        # Define deprecated variables and their replacements
        deprecated_vars = {
            'OPENAI_API_KEY': 'OPENROUTER_API_KEY',
            'ANTHROPIC_API_KEY': 'OPENROUTER_API_KEY',
            'GOOGLE_API_KEY': 'OPENROUTER_API_KEY',
            'AZURE_OPENAI_API_KEY': 'OPENROUTER_API_KEY'
        }
        
        for old_var, new_var in deprecated_vars.items():
            if old_var in env_vars:
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='deprecated',
                    field=old_var,
                    message=f"Variable '{old_var}' is deprecated",
                    suggestion=f"Use '{new_var}' instead for OpenRouter integration"
                ))
    
    def _validate_security_settings(self) -> None:
        """Validate security-related configuration."""
        if not self.env_file.exists():
            return
        
        env_vars = self._load_env_file()
        
        # Check secret strength
        security_vars = ['LANGFUSE_NEXTAUTH_SECRET', 'LANGFUSE_SALT', 'POSTGRES_PASSWORD']
        
        for var in security_vars:
            value = env_vars.get(var, '')
            if value:
                if len(value) < 16:
                    self.issues.append(ValidationIssue(
                        severity='error',
                        category='security',
                        field=var,
                        message=f"Variable '{var}' is too short ({len(value)} < 16 characters)",
                        suggestion=f"Generate a stronger value for {var} using the secret generation utility"
                    ))
                elif len(value) < 32 and var in ['LANGFUSE_NEXTAUTH_SECRET', 'LANGFUSE_SALT']:
                    self.issues.append(ValidationIssue(
                        severity='warning',
                        category='security',
                        field=var,
                        message=f"Variable '{var}' should be at least 32 characters",
                        suggestion=f"Consider generating a longer value for {var}"
                    ))
    
    def _load_env_file(self) -> Dict[str, str]:
        """Load environment variables from .env file."""
        env_vars = {}
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")  # Remove quotes
                        env_vars[key] = value
                    
        except Exception as e:
            self.logger.error(f"Error reading .env file: {e}")
        
        return env_vars
    
    def fix_auto_fixable_issues(self) -> int:
        """
        Automatically fix issues that can be resolved programmatically.
        
        Returns:
            Number of issues fixed
        """
        fixed_count = 0
        
        for issue in self.issues:
            if not issue.auto_fixable:
                continue
            
            try:
                if issue.field == 'env_file' and issue.category == 'missing':
                    # Copy template to .env
                    if self.env_template.exists():
                        import shutil
                        shutil.copy2(self.env_template, self.env_file)
                        self.logger.info(f"Created {self.env_file} from template")
                        fixed_count += 1
                
                elif issue.field == 'env_file_permissions' and issue.category == 'security':
                    # Fix file permissions
                    self.env_file.chmod(0o600)
                    self.logger.info(f"Fixed permissions for {self.env_file}")
                    fixed_count += 1
                    
            except Exception as e:
                self.logger.error(f"Failed to fix issue {issue.field}: {e}")
        
        return fixed_count
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive validation report.
        
        Returns:
            Formatted validation report
        """
        if not self.issues:
            return f"✅ Configuration validation passed for {self.framework} framework"
        
        # Group issues by severity
        errors = [i for i in self.issues if i.severity == 'error']
        warnings = [i for i in self.issues if i.severity == 'warning']
        info = [i for i in self.issues if i.severity == 'info']
        
        report_lines = [
            f"🔧 Configuration Validation Report: {self.framework.upper()}",
            "=" * 60
        ]
        
        if errors:
            report_lines.extend([
                f"\n❌ ERRORS ({len(errors)}):",
                "-" * 20
            ])
            for error in errors:
                report_lines.append(f"  • {error.field}: {error.message}")
                if error.suggestion:
                    report_lines.append(f"    💡 {error.suggestion}")
        
        if warnings:
            report_lines.extend([
                f"\n⚠️  WARNINGS ({len(warnings)}):",
                "-" * 20
            ])
            for warning in warnings:
                report_lines.append(f"  • {warning.field}: {warning.message}")
                if warning.suggestion:
                    report_lines.append(f"    💡 {warning.suggestion}")
        
        if info:
            report_lines.extend([
                f"\nℹ️  INFO ({len(info)}):",
                "-" * 20
            ])
            for item in info:
                report_lines.append(f"  • {item.field}: {item.message}")
        
        # Summary
        report_lines.extend([
            "\n" + "=" * 60,
            f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(info)} info"
        ])
        
        if errors:
            report_lines.append("❌ Configuration validation FAILED - fix errors before proceeding")
        elif warnings:
            report_lines.append("⚠️  Configuration validation PASSED with warnings")
        else:
            report_lines.append("✅ Configuration validation PASSED")
        
        return "\n".join(report_lines)


def main():
    """Main entry point for the configuration validator CLI."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Validate framework configuration files and environment variables"
    )

    parser.add_argument(
        "--framework",
        choices=["dspy", "crewai", "pocketflow", "google_adk", "pydantic_ai"],
        default="dspy",
        help="Framework to validate (default: dspy)"
    )

    parser.add_argument(
        "--fix-issues",
        action="store_true",
        help="Automatically fix issues that can be resolved programmatically"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize validator
    validator = ConfigValidator(framework=args.framework)

    print(f"🔍 Validating {args.framework} framework configuration...")

    # Perform validation
    issues = validator.validate_configuration()

    # Auto-fix issues if requested
    if args.fix_issues:
        fixed_count = validator.fix_auto_fixable_issues()
        if fixed_count > 0:
            print(f"🔧 Automatically fixed {fixed_count} issues")
            # Re-validate after fixes
            issues = validator.validate_configuration()

    # Generate and display report
    report = validator.generate_report()
    print(report)

    # Exit with appropriate code
    errors = [i for i in issues if i.severity == 'error']
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
