#!/usr/bin/env python3
"""
Template Customization Script for AI Agent Framework Infrastructure

This script provides functionality to customize Docker Compose and environment
templates for specific frameworks, including variable substitution, validation,
and conflict detection.
"""

import os
import re
import shutil
import socket
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
import yaml
import logging
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FrameworkConfig(BaseModel):
    """Configuration for a specific framework."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    name: str = Field(
        ...,
        description="Framework name (e.g., 'dspy', 'crewai')",
        min_length=1,
        max_length=50,
        pattern=r'^[a-z][a-z0-9_]*$'
    )
    qdrant_port: int = Field(
        ...,
        description="Port for Qdrant vector database",
        ge=1024,
        le=65535
    )
    langfuse_port: int = Field(
        ...,
        description="Port for Langfuse observability platform",
        ge=1024,
        le=65535
    )
    postgres_port: int = Field(
        ...,
        description="Port for PostgreSQL database",
        ge=1024,
        le=65535
    )
    network_subnet: int = Field(
        ...,
        description="Network subnet number for Docker network isolation",
        ge=20,
        le=24
    )
    postgres_user: str = Field(
        default="langfuse_user",
        description="PostgreSQL username",
        min_length=1,
        max_length=63
    )
    postgres_password: str = Field(
        default="langfuse_password",
        description="PostgreSQL password",
        min_length=1,
        max_length=100
    )

    @field_validator('name')
    @classmethod
    def validate_framework_name(cls, v: str) -> str:
        """Validate framework name follows naming conventions."""
        valid_frameworks = {'dspy', 'pocketflow', 'crewai', 'google_adk', 'pydantic_ai'}
        if v not in valid_frameworks:
            raise ValueError(f"Framework name must be one of: {', '.join(valid_frameworks)}")
        return v

    @field_validator('qdrant_port', 'langfuse_port', 'postgres_port')
    @classmethod
    def validate_port_uniqueness(cls, v: int, info) -> int:
        """Validate that ports are in expected ranges for each service."""
        field_name = info.field_name

        if field_name == 'qdrant_port' and not (6333 <= v <= 6337):
            raise ValueError(f"Qdrant port must be in range 6333-6337, got {v}")
        elif field_name == 'langfuse_port' and not (3000 <= v <= 3004):
            raise ValueError(f"Langfuse port must be in range 3000-3004, got {v}")
        elif field_name == 'postgres_port' and not (5432 <= v <= 5436):
            raise ValueError(f"PostgreSQL port must be in range 5432-5436, got {v}")

        return v

    @field_validator('postgres_user', 'postgres_password')
    @classmethod
    def validate_postgres_credentials(cls, v: str) -> str:
        """Validate PostgreSQL credentials don't contain unsafe characters."""
        if any(char in v for char in [';', '--', '/*', '*/', 'xp_', 'sp_']):
            raise ValueError("PostgreSQL credentials contain potentially unsafe characters")
        return v


class PortConflictDetector:
    """Detects and resolves port conflicts between frameworks."""
    
    def __init__(self):
        self.reserved_ports: Set[int] = set()
        self.framework_ports: Dict[str, List[int]] = {}
    
    def is_port_available(self, port: int, host: str = 'localhost') -> bool:
        """
        Check if a port is available on the specified host.
        
        Args:
            port: Port number to check
            host: Host to check (default: localhost)
            
        Returns:
            True if port is available, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                return result != 0
        except Exception as e:
            logger.warning(f"Error checking port {port}: {e}")
            return False
    
    def check_framework_ports(self, config: FrameworkConfig) -> List[str]:
        """
        Check for port conflicts for a framework configuration.
        
        Args:
            config: Framework configuration to check
            
        Returns:
            List of conflict messages (empty if no conflicts)
        """
        conflicts = []
        ports_to_check = [
            (config.qdrant_port, "Qdrant"),
            (config.langfuse_port, "Langfuse"),
            (config.postgres_port, "PostgreSQL")
        ]
        
        for port, service in ports_to_check:
            if not self.is_port_available(port):
                conflicts.append(f"{service} port {port} is already in use")
            
            if port in self.reserved_ports:
                conflicts.append(f"{service} port {port} is reserved by another framework")
        
        return conflicts
    
    def reserve_ports(self, framework_name: str, config: FrameworkConfig) -> None:
        """Reserve ports for a framework."""
        ports = [config.qdrant_port, config.langfuse_port, config.postgres_port]
        self.framework_ports[framework_name] = ports
        self.reserved_ports.update(ports)


class TemplateCustomizer:
    """Main class for customizing infrastructure templates."""
    
    # Default framework configurations
    DEFAULT_CONFIGS = {
        'dspy': FrameworkConfig(
            name='dspy',
            qdrant_port=6334,
            langfuse_port=3001,
            postgres_port=5433,
            network_subnet=21
        ),
        'pocketflow': FrameworkConfig(
            name='pocketflow',
            qdrant_port=6335,
            langfuse_port=3002,
            postgres_port=5434,
            network_subnet=22
        ),
        'crewai': FrameworkConfig(
            name='crewai',
            qdrant_port=6333,
            langfuse_port=3000,
            postgres_port=5432,
            network_subnet=20
        ),
        'google_adk': FrameworkConfig(
            name='google_adk',
            qdrant_port=6336,
            langfuse_port=3003,
            postgres_port=5435,
            network_subnet=23
        ),
        'pydantic_ai': FrameworkConfig(
            name='pydantic_ai',
            qdrant_port=6337,
            langfuse_port=3004,
            postgres_port=5436,
            network_subnet=24
        ),
    }
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize the template customizer.

        Args:
            base_dir: Base directory for the project (default: parent of current directory if in shared_infrastructure)
        """
        if base_dir is None:
            current_dir = Path.cwd()
            if current_dir.name == "shared_infrastructure":
                self.base_dir = current_dir.parent
                self.shared_infra_dir = current_dir
            else:
                self.base_dir = current_dir
                self.shared_infra_dir = self.base_dir / "shared_infrastructure"
        else:
            self.base_dir = base_dir
            self.shared_infra_dir = self.base_dir / "shared_infrastructure"

        self.port_detector = PortConflictDetector()

        # Validate base directory structure
        if not self.shared_infra_dir.exists():
            raise FileNotFoundError(f"Shared infrastructure directory not found: {self.shared_infra_dir}")
    
    def validate_environment_variables(self, framework_name: str, env_vars: Dict[str, str]) -> List[str]:
        """
        Validate required environment variables for a framework.
        
        Args:
            framework_name: Name of the framework
            env_vars: Dictionary of environment variables
            
        Returns:
            List of validation error messages
        """
        required_vars = [
            'FRAMEWORK_NAME',
            'QDRANT_PORT',
            'LANGFUSE_PORT',
            'POSTGRES_USER',
            'POSTGRES_PASSWORD',
            'NETWORK_SUBNET'
        ]
        
        errors = []
        
        for var in required_vars:
            if var not in env_vars or not env_vars[var]:
                errors.append(f"Missing required environment variable: {var}")
        
        # Validate framework name consistency
        if env_vars.get('FRAMEWORK_NAME') != framework_name:
            errors.append(f"Framework name mismatch: expected {framework_name}, got {env_vars.get('FRAMEWORK_NAME')}")
        
        # Validate port numbers
        for port_var in ['QDRANT_PORT', 'LANGFUSE_PORT']:
            if port_var in env_vars:
                try:
                    port = int(env_vars[port_var])
                    if not (1024 <= port <= 65535):
                        errors.append(f"Invalid port range for {port_var}: {port} (must be 1024-65535)")
                except ValueError:
                    errors.append(f"Invalid port number for {port_var}: {env_vars[port_var]}")
        
        # Validate network subnet
        if 'NETWORK_SUBNET' in env_vars:
            try:
                subnet = int(env_vars['NETWORK_SUBNET'])
                if not (20 <= subnet <= 24):
                    errors.append(f"Invalid network subnet: {subnet} (must be 20-24)")
            except ValueError:
                errors.append(f"Invalid network subnet: {env_vars['NETWORK_SUBNET']}")
        
        return errors
    
    def substitute_template_variables(self, template_content: str, variables: Dict[str, str]) -> str:
        """
        Substitute variables in template content.
        
        Args:
            template_content: Template content with ${VAR} placeholders
            variables: Dictionary of variable substitutions
            
        Returns:
            Content with variables substituted
        """
        result = template_content
        
        # Replace ${VAR} style variables
        for var_name, var_value in variables.items():
            pattern = f"${{{var_name}}}"
            result = result.replace(pattern, str(var_value))
        
        # Check for unsubstituted variables
        unsubstituted = re.findall(r'\$\{([^}]+)\}', result)
        if unsubstituted:
            logger.warning(f"Unsubstituted variables found: {unsubstituted}")
        
        return result
    
    def create_backup(self, target_path: Path) -> Optional[Path]:
        """
        Create a backup of an existing file.
        
        Args:
            target_path: Path to the file to backup
            
        Returns:
            Path to the backup file, or None if no backup was needed
        """
        if not target_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_path.with_suffix(f".backup_{timestamp}{target_path.suffix}")
        
        shutil.copy2(target_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        
        return backup_path

    def generate_framework_config(self, framework_name: str, custom_config: Optional[FrameworkConfig] = None) -> Dict[str, str]:
        """
        Generate environment variables for a framework.

        Args:
            framework_name: Name of the framework
            custom_config: Custom configuration (uses default if None)

        Returns:
            Dictionary of environment variables
        """
        config = custom_config or self.DEFAULT_CONFIGS.get(framework_name)
        if not config:
            raise ValueError(f"No configuration found for framework: {framework_name}")

        # Generate database URL
        db_url = f"postgresql://{config.postgres_user}:{config.postgres_password}@postgres:5432/langfuse"

        return {
            'FRAMEWORK_NAME': config.name,
            'QDRANT_PORT': str(config.qdrant_port),
            'LANGFUSE_PORT': str(config.langfuse_port),
            'POSTGRES_USER': config.postgres_user,
            'POSTGRES_PASSWORD': config.postgres_password,
            'LANGFUSE_DB_URL': db_url,
            'NETWORK_SUBNET': str(config.network_subnet),
            'LANGFUSE_NEXTAUTH_SECRET': f"{config.name}_nextauth_secret_change_me",
            'LANGFUSE_SALT': f"{config.name}_salt_change_me"
        }

    def customize_docker_compose(self, framework_name: str, output_dir: Optional[Path] = None) -> Path:
        """
        Customize Docker Compose template for a specific framework.

        Args:
            framework_name: Name of the framework
            output_dir: Output directory (default: framework directory)

        Returns:
            Path to the generated docker-compose.yaml file
        """
        # Read template
        template_path = self.shared_infra_dir / "docker-compose.template.yaml"
        if not template_path.exists():
            raise FileNotFoundError(f"Docker Compose template not found: {template_path}")

        with open(template_path, 'r') as f:
            template_content = f.read()

        # Generate variables
        variables = self.generate_framework_config(framework_name)

        # Validate environment variables
        validation_errors = self.validate_environment_variables(framework_name, variables)
        if validation_errors:
            raise ValueError(f"Environment validation failed: {validation_errors}")

        # Check for port conflicts
        config = self.DEFAULT_CONFIGS[framework_name]
        conflicts = self.port_detector.check_framework_ports(config)
        if conflicts:
            logger.warning(f"Port conflicts detected for {framework_name}: {conflicts}")

        # Substitute variables
        customized_content = self.substitute_template_variables(template_content, variables)

        # Determine output path
        if output_dir is None:
            output_dir = self.base_dir / framework_name

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "docker-compose.yaml"

        # Create backup if file exists
        self.create_backup(output_path)

        # Write customized file
        with open(output_path, 'w') as f:
            f.write(customized_content)

        logger.info(f"Generated Docker Compose file: {output_path}")
        return output_path

    def customize_env_template(self, framework_name: str, output_dir: Optional[Path] = None) -> Path:
        """
        Generate .env file from template for a specific framework.

        Args:
            framework_name: Name of the framework
            output_dir: Output directory (default: framework directory)

        Returns:
            Path to the generated .env file
        """
        # Generate variables
        variables = self.generate_framework_config(framework_name)

        # Determine output path
        if output_dir is None:
            output_dir = self.base_dir / framework_name

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / ".env"

        # Create backup if file exists
        self.create_backup(output_path)

        # Generate .env content
        env_content = "# Generated Environment Configuration\n"
        env_content += f"# Framework: {framework_name}\n"
        env_content += f"# Generated: {datetime.now().isoformat()}\n\n"

        for key, value in variables.items():
            env_content += f"{key}={value}\n"

        # Write .env file
        with open(output_path, 'w') as f:
            f.write(env_content)

        logger.info(f"Generated .env file: {output_path}")
        return output_path

    def customize_all_frameworks(self) -> Dict[str, Dict[str, Path]]:
        """
        Customize templates for all frameworks.

        Returns:
            Dictionary mapping framework names to generated file paths
        """
        results = {}

        for framework_name in self.DEFAULT_CONFIGS.keys():
            try:
                logger.info(f"Customizing templates for {framework_name}")

                docker_compose_path = self.customize_docker_compose(framework_name)
                env_path = self.customize_env_template(framework_name)

                # Reserve ports to prevent conflicts
                config = self.DEFAULT_CONFIGS[framework_name]
                self.port_detector.reserve_ports(framework_name, config)

                results[framework_name] = {
                    'docker_compose': docker_compose_path,
                    'env': env_path
                }

                logger.info(f"Successfully customized {framework_name}")

            except Exception as e:
                logger.error(f"Failed to customize {framework_name}: {e}")
                results[framework_name] = {'error': str(e)}

        return results


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Customize infrastructure templates for AI agent frameworks")
    parser.add_argument('--framework', '-f', help="Framework name to customize (default: all)")
    parser.add_argument('--output-dir', '-o', help="Output directory (default: framework directory)")
    parser.add_argument('--check-ports', '-p', action='store_true', help="Only check for port conflicts")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        customizer = TemplateCustomizer()

        if args.check_ports:
            # Only check for port conflicts
            for framework_name, config in customizer.DEFAULT_CONFIGS.items():
                conflicts = customizer.port_detector.check_framework_ports(config)
                if conflicts:
                    print(f"{framework_name}: {', '.join(conflicts)}")
                else:
                    print(f"{framework_name}: No conflicts")
            return

        if args.framework:
            # Customize specific framework
            if args.framework not in customizer.DEFAULT_CONFIGS:
                print(f"Error: Unknown framework '{args.framework}'")
                print(f"Available frameworks: {', '.join(customizer.DEFAULT_CONFIGS.keys())}")
                return

            output_dir = Path(args.output_dir) if args.output_dir else None
            customizer.customize_docker_compose(args.framework, output_dir)
            customizer.customize_env_template(args.framework, output_dir)
            print(f"Successfully customized {args.framework}")
        else:
            # Customize all frameworks
            results = customizer.customize_all_frameworks()

            print("\nCustomization Summary:")
            for framework, result in results.items():
                if 'error' in result:
                    print(f"  {framework}: FAILED - {result['error']}")
                else:
                    print(f"  {framework}: SUCCESS")

    except Exception as e:
        logger.error(f"Customization failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
