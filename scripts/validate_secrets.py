#!/usr/bin/env python3
"""
Secret Validation Utility for AI Agent Framework Comparison Project.

This script validates environment configuration secrets to ensure they meet
basic security requirements and are not using default/example values.

Usage:
    uv run python validate_secrets.py [--env-file path/to/.env] [--strict]
"""

import re
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of secret validation."""
    is_valid: bool
    message: str
    severity: str  # 'error', 'warning', 'info'


class SecretValidator:
    """
    Utility class for validating environment secrets.
    
    Validates secret strength, checks for default values, and identifies
    common security vulnerabilities in environment configuration.
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the SecretValidator.
        
        Args:
            strict_mode: Enable strict validation rules
        """
        self.strict_mode = strict_mode
        
        # Common weak passwords and default values
        self.weak_passwords = {
            'password', 'password123', '123456', 'admin', 'root', 'user',
            'test', 'demo', 'example', 'changeme', 'default', 'secret',
            'qwerty', 'abc123', 'letmein', 'welcome', 'monkey', 'dragon'
        }
        
        # Default/example values that should be replaced
        self.default_values = {
            'your_api_key_here', 'your_secret_here', 'your_password_here',
            'your_nextauth_secret', 'your_salt_here', 'your_key_here',
            'replace_with_actual_key', 'change_this_value', 'example_value',
            'your_nextauth_secret_here_32_chars_minimum',
            'your_salt_here_32_chars_minimum', 'langfuse_user', 'langfuse_password'
        }
        
        # Required secrets and their minimum lengths
        self.required_secrets = {
            'LANGFUSE_NEXTAUTH_SECRET': 32,
            'LANGFUSE_SALT': 32,
            'POSTGRES_PASSWORD': 16,
            'OPENROUTER_API_KEY': 20
        }
    
    def validate_secret_strength(self, secret: str, min_length: int = 32) -> ValidationResult:
        """
        Validate the strength of a secret.
        
        Args:
            secret: The secret to validate
            min_length: Minimum required length
            
        Returns:
            ValidationResult with validation status and message
        """
        if not secret:
            return ValidationResult(False, "Secret is empty", "error")
        
        if len(secret) < min_length:
            return ValidationResult(
                False, 
                f"Secret too short: {len(secret)} < {min_length} characters", 
                "error"
            )
        
        # Check for weak passwords
        if secret.lower() in self.weak_passwords:
            return ValidationResult(False, "Secret is a common weak password", "error")
        
        # Check for default values
        if secret.lower() in {v.lower() for v in self.default_values}:
            return ValidationResult(False, "Secret appears to be a default/example value", "error")
        
        # Check character diversity (in strict mode)
        if self.strict_mode:
            has_upper = any(c.isupper() for c in secret)
            has_lower = any(c.islower() for c in secret)
            has_digit = any(c.isdigit() for c in secret)
            has_symbol = any(not c.isalnum() for c in secret)
            
            diversity_score = sum([has_upper, has_lower, has_digit, has_symbol])
            
            if diversity_score < 3:
                return ValidationResult(
                    False,
                    f"Secret lacks character diversity (score: {diversity_score}/4)",
                    "warning" if diversity_score >= 2 else "error"
                )
        
        return ValidationResult(True, "Secret meets security requirements", "info")
    
    def check_for_default_values(self, secret: str) -> ValidationResult:
        """
        Check if a secret contains default or example values.
        
        Args:
            secret: The secret to check
            
        Returns:
            ValidationResult with check status and message
        """
        secret_lower = secret.lower()
        
        for default_value in self.default_values:
            if default_value.lower() in secret_lower:
                return ValidationResult(
                    False,
                    f"Secret contains default value pattern: '{default_value}'",
                    "error"
                )
        
        # Check for common placeholder patterns
        placeholder_patterns = [
            r'your_\w+_here',
            r'replace_\w+',
            r'change_\w+',
            r'example_\w+',
            r'\w+_placeholder'
        ]
        
        for pattern in placeholder_patterns:
            if re.search(pattern, secret_lower):
                return ValidationResult(
                    False,
                    f"Secret contains placeholder pattern: {pattern}",
                    "error"
                )
        
        return ValidationResult(True, "No default values detected", "info")
    
    def validate_environment_file(self, env_file_path: Path) -> List[ValidationResult]:
        """
        Validate all secrets in an environment file.
        
        Args:
            env_file_path: Path to the .env file
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        if not env_file_path.exists():
            results.append(ValidationResult(
                False,
                f"Environment file not found: {env_file_path}",
                "error"
            ))
            return results
        
        try:
            with open(env_file_path, 'r') as f:
                content = f.read()
        except Exception as e:
            results.append(ValidationResult(
                False,
                f"Error reading environment file: {e}",
                "error"
            ))
            return results
        
        # Parse environment variables
        env_vars = self._parse_env_file(content)
        
        # Validate required secrets
        for secret_name, min_length in self.required_secrets.items():
            if secret_name not in env_vars:
                results.append(ValidationResult(
                    False,
                    f"Required secret '{secret_name}' not found",
                    "error"
                ))
                continue
            
            secret_value = env_vars[secret_name]
            
            # Validate strength
            strength_result = self.validate_secret_strength(secret_value, min_length)
            strength_result.message = f"{secret_name}: {strength_result.message}"
            results.append(strength_result)
            
            # Check for defaults
            default_result = self.check_for_default_values(secret_value)
            if not default_result.is_valid:
                default_result.message = f"{secret_name}: {default_result.message}"
                results.append(default_result)
        
        # Validate other secrets that look important
        sensitive_patterns = ['SECRET', 'PASSWORD', 'KEY', 'TOKEN', 'SALT']
        for var_name, var_value in env_vars.items():
            if any(pattern in var_name.upper() for pattern in sensitive_patterns):
                if var_name not in self.required_secrets:
                    # Basic validation for other sensitive variables
                    if len(var_value) < 16:
                        results.append(ValidationResult(
                            False,
                            f"{var_name}: Secret too short ({len(var_value)} < 16 characters)",
                            "warning"
                        ))
                    
                    default_result = self.check_for_default_values(var_value)
                    if not default_result.is_valid:
                        default_result.message = f"{var_name}: {default_result.message}"
                        results.append(default_result)
        
        return results
    
    def _parse_env_file(self, content: str) -> Dict[str, str]:
        """
        Parse environment file content into key-value pairs.
        
        Args:
            content: Content of the .env file
            
        Returns:
            Dictionary of environment variables
        """
        env_vars = {}
        
        for line in content.split('\n'):
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
        
        return env_vars


def print_validation_results(results: List[ValidationResult]) -> bool:
    """
    Print validation results with color coding.
    
    Args:
        results: List of validation results
        
    Returns:
        True if all validations passed, False otherwise
    """
    errors = [r for r in results if r.severity == 'error']
    warnings = [r for r in results if r.severity == 'warning']
    info = [r for r in results if r.severity == 'info']
    
    print("🔒 Secret Validation Results")
    print("=" * 50)
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for result in errors:
            print(f"  • {result.message}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for result in warnings:
            print(f"  • {result.message}")
    
    if info:
        print(f"\n✅ PASSED ({len(info)}):")
        for result in info:
            print(f"  • {result.message}")
    
    print("\n" + "=" * 50)
    
    if errors:
        print("❌ VALIDATION FAILED: Please fix the errors above")
        return False
    elif warnings:
        print("⚠️  VALIDATION PASSED WITH WARNINGS: Consider addressing warnings")
        return True
    else:
        print("✅ ALL VALIDATIONS PASSED: Secrets meet security requirements")
        return True


def main():
    """Main entry point for the secret validation utility."""
    parser = argparse.ArgumentParser(
        description="Validate environment secrets for security compliance"
    )
    
    parser.add_argument(
        "--env-file",
        type=str,
        help="Path to .env file to validate (searches common locations if not specified)"
    )
    
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation rules"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = SecretValidator(strict_mode=args.strict)
    
    # Determine env file path
    if args.env_file:
        env_file_path = Path(args.env_file)
    else:
        # Search for common .env file locations
        possible_paths = [
            Path(".env"),
            Path("../.env"),
            Path("dspy/.env"),
            Path("crewai/.env"),
            Path("pocketflow/.env"),
            Path("google_adk/.env"),
            Path("pydantic_ai/.env")
        ]
        
        env_file_path = None
        for path in possible_paths:
            if path.exists():
                env_file_path = path
                break
        
        if not env_file_path:
            print("❌ No .env file found. Please specify --env-file or create a .env file.")
            sys.exit(1)
    
    print(f"🔍 Validating secrets in: {env_file_path}")
    
    # Validate secrets
    results = validator.validate_environment_file(env_file_path)
    
    # Print results and exit with appropriate code
    success = print_validation_results(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
