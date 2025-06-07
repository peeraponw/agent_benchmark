#!/usr/bin/env python3
"""
Secret Generation Utility for AI Agent Framework Comparison Project.

This script generates secure random secrets for environment configuration,
focusing on essential security requirements for Langfuse and database setup.

Usage:
    uv run python generate_secrets.py [--output-format env|json|yaml]
"""

import secrets
import string
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


class SecretGenerator:
    """
    Utility class for generating secure secrets for the project.
    
    Generates cryptographically secure random strings suitable for
    authentication secrets, database passwords, and API keys.
    """
    
    def __init__(self, min_length: int = 32):
        """
        Initialize the SecretGenerator.
        
        Args:
            min_length: Minimum length for generated secrets (default: 32)
        """
        self.min_length = max(min_length, 32)  # Enforce minimum 32 characters
        
        # Character sets for different types of secrets
        self.alphanumeric = string.ascii_letters + string.digits
        self.alphanumeric_symbols = string.ascii_letters + string.digits + "!@#$%^&*"
        self.hex_chars = string.hexdigits.lower()
    
    def generate_secure_string(self, length: Optional[int] = None, 
                             include_symbols: bool = False) -> str:
        """
        Generate a cryptographically secure random string.
        
        Args:
            length: Length of the string (uses min_length if None)
            include_symbols: Whether to include special symbols
            
        Returns:
            Secure random string
        """
        if length is None:
            length = self.min_length
        
        length = max(length, self.min_length)  # Enforce minimum length
        
        charset = self.alphanumeric_symbols if include_symbols else self.alphanumeric
        return ''.join(secrets.choice(charset) for _ in range(length))
    
    def generate_hex_string(self, length: Optional[int] = None) -> str:
        """
        Generate a cryptographically secure hexadecimal string.
        
        Args:
            length: Length of the string (uses min_length if None)
            
        Returns:
            Secure random hexadecimal string
        """
        if length is None:
            length = self.min_length
            
        length = max(length, self.min_length)  # Enforce minimum length
        return ''.join(secrets.choice(self.hex_chars) for _ in range(length))
    
    def generate_langfuse_nextauth_secret(self) -> str:
        """
        Generate a secure NextAuth secret for Langfuse.
        
        Returns:
            64-character secure random string suitable for NextAuth
        """
        return self.generate_secure_string(64, include_symbols=True)
    
    def generate_langfuse_salt(self) -> str:
        """
        Generate a secure salt for Langfuse.
        
        Returns:
            32-character secure random hexadecimal string
        """
        return self.generate_hex_string(32)
    
    def generate_database_password(self) -> str:
        """
        Generate a secure database password.
        
        Returns:
            48-character secure random string with symbols
        """
        return self.generate_secure_string(48, include_symbols=True)
    
    def generate_api_key(self) -> str:
        """
        Generate a secure API key.
        
        Returns:
            40-character secure random alphanumeric string
        """
        return self.generate_secure_string(40, include_symbols=False)
    
    def generate_all_secrets(self) -> Dict[str, str]:
        """
        Generate all required secrets for the project.
        
        Returns:
            Dictionary containing all generated secrets
        """
        return {
            'LANGFUSE_NEXTAUTH_SECRET': self.generate_langfuse_nextauth_secret(),
            'LANGFUSE_SALT': self.generate_langfuse_salt(),
            'POSTGRES_PASSWORD': self.generate_database_password(),
            'LANGFUSE_DB_PASSWORD': self.generate_database_password(),
            'GENERAL_API_KEY': self.generate_api_key(),
            'BACKUP_SECRET': self.generate_secure_string(32)
        }


def format_secrets_as_env(secrets_dict: Dict[str, str]) -> str:
    """
    Format secrets as environment variable assignments.
    
    Args:
        secrets_dict: Dictionary of secret names and values
        
    Returns:
        Formatted environment variable string
    """
    lines = [
        "# Generated secrets for AI Agent Framework Comparison Project",
        f"# Generated on: {Path(__file__).stat().st_mtime}",
        "# WARNING: Keep these secrets secure and never commit to version control",
        "",
        "# Langfuse Authentication Secrets",
        f"LANGFUSE_NEXTAUTH_SECRET={secrets_dict['LANGFUSE_NEXTAUTH_SECRET']}",
        f"LANGFUSE_SALT={secrets_dict['LANGFUSE_SALT']}",
        "",
        "# Database Passwords",
        f"POSTGRES_PASSWORD={secrets_dict['POSTGRES_PASSWORD']}",
        f"LANGFUSE_DB_PASSWORD={secrets_dict['LANGFUSE_DB_PASSWORD']}",
        "",
        "# Additional Secrets",
        f"GENERAL_API_KEY={secrets_dict['GENERAL_API_KEY']}",
        f"BACKUP_SECRET={secrets_dict['BACKUP_SECRET']}",
        ""
    ]
    return "\n".join(lines)


def format_secrets_as_json(secrets_dict: Dict[str, str]) -> str:
    """
    Format secrets as JSON.
    
    Args:
        secrets_dict: Dictionary of secret names and values
        
    Returns:
        JSON formatted string
    """
    return json.dumps(secrets_dict, indent=2)


def format_secrets_as_yaml(secrets_dict: Dict[str, str]) -> str:
    """
    Format secrets as YAML.
    
    Args:
        secrets_dict: Dictionary of secret names and values
        
    Returns:
        YAML formatted string
    """
    lines = [
        "# Generated secrets for AI Agent Framework Comparison Project",
        "# WARNING: Keep these secrets secure and never commit to version control",
        ""
    ]
    
    for key, value in secrets_dict.items():
        lines.append(f"{key}: {value}")
    
    return "\n".join(lines)


def main():
    """Main entry point for the secret generation utility."""
    parser = argparse.ArgumentParser(
        description="Generate secure secrets for AI Agent Framework Comparison Project"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["env", "json", "yaml"],
        default="env",
        help="Output format for generated secrets (default: env)"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path (prints to stdout if not specified)"
    )
    
    parser.add_argument(
        "--min-length",
        type=int,
        default=32,
        help="Minimum length for generated secrets (default: 32)"
    )
    
    args = parser.parse_args()
    
    # Generate secrets
    generator = SecretGenerator(min_length=args.min_length)
    secrets_dict = generator.generate_all_secrets()
    
    # Format output
    if args.output_format == "env":
        output = format_secrets_as_env(secrets_dict)
    elif args.output_format == "json":
        output = format_secrets_as_json(secrets_dict)
    elif args.output_format == "yaml":
        output = format_secrets_as_yaml(secrets_dict)
    else:
        print(f"Error: Unsupported output format: {args.output_format}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    if args.output_file:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(output)
        
        print(f"Secrets generated and saved to: {output_path}")
        print("WARNING: Keep this file secure and never commit to version control!")
    else:
        print(output)


if __name__ == "__main__":
    main()
