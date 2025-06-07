#!/usr/bin/env python3
"""
Project Structure Validation Script

This script validates that the AI Agent Frameworks Comparison Project
directory structure matches the specification and all required files exist.

Usage:
    uv run python validate_structure.py
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    details: str = ""


class StructureValidator:
    """Validates project structure against specification."""

    def __init__(self, project_root: Path = None):
        """
        Initialize validator.

        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.results: List[ValidationResult] = []
        self.console = Console() if RICH_AVAILABLE else None
    
    def validate_all(self) -> bool:
        """
        Run all validation checks.

        Returns:
            True if all validations pass, False otherwise.
        """
        if self.console:
            self.console.print(Panel.fit(
                "🔍 AI Agent Frameworks Comparison Project Structure Validation",
                style="bold blue"
            ))
            self.console.print(f"📁 Project Root: [bold]{self.project_root}[/bold]")
            self.console.print()
        else:
            print("🔍 Validating AI Agent Frameworks Comparison Project Structure...")
            print(f"📁 Project Root: {self.project_root}")
            print()
        
        # Run all validation checks
        self._validate_framework_directories()
        self._validate_shared_directories()
        self._validate_evaluation_structure()
        self._validate_shared_datasets()
        self._validate_documentation()
        self._validate_configuration_files()
        self._validate_infrastructure_templates()
        self._validate_environment_templates()
        self._validate_json_file_structure()
        self._validate_docker_template_syntax()
        
        # Print results
        self._print_results()
        
        # Return overall success
        return all(result.passed for result in self.results)
    
    def _validate_framework_directories(self) -> None:
        """Validate framework directory structure."""
        print("🏗️  Validating Framework Directories...")
        
        frameworks = ["crewai", "dspy", "pocketflow", "google_adk", "pydantic_ai"]
        
        for framework in frameworks:
            framework_path = self.project_root / framework
            
            if framework_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Framework directory '{framework}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Framework directory '{framework}' missing"
                ))
    
    def _validate_shared_directories(self) -> None:
        """Validate shared directory structure."""
        print("📂 Validating Shared Directories...")
        
        shared_dirs = [
            "shared_datasets",
            "evaluation", 
            "shared_infrastructure",
            "docs"
        ]
        
        for dir_name in shared_dirs:
            dir_path = self.project_root / dir_name
            
            if dir_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Shared directory '{dir_name}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Shared directory '{dir_name}' missing"
                ))
    
    def _validate_evaluation_structure(self) -> None:
        """Validate evaluation framework structure."""
        print("📊 Validating Evaluation Framework...")
        
        eval_path = self.project_root / "evaluation"
        required_files = [
            "__init__.py",
            "base_evaluator.py"
        ]
        required_dirs = [
            "metrics",
            "reports", 
            "benchmarks"
        ]
        
        for file_name in required_files:
            file_path = eval_path / file_name
            if file_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Evaluation file '{file_name}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Evaluation file '{file_name}' missing"
                ))
        
        for dir_name in required_dirs:
            dir_path = eval_path / dir_name
            if dir_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Evaluation directory '{dir_name}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Evaluation directory '{dir_name}' missing"
                ))
    
    def _validate_shared_datasets(self) -> None:
        """Validate shared datasets structure."""
        print("📋 Validating Shared Datasets...")
        
        datasets_path = self.project_root / "shared_datasets"
        
        # Check main dataset directories
        dataset_dirs = ["qa", "rag_documents", "web_search", "multi_agent"]
        for dir_name in dataset_dirs:
            dir_path = datasets_path / dir_name
            if dir_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Dataset directory '{dir_name}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Dataset directory '{dir_name}' missing"
                ))
        
        # Check specific files
        required_files = [
            "qa/questions.json",
            "qa/answers.json", 
            "qa/metadata.json",
            "rag_documents/documents/sample_document_1.txt",
            "rag_documents/ground_truth/expected_retrievals.json",
            "web_search/queries.json",
            "web_search/expected_sources.json",
            "multi_agent/research_tasks.json",
            "multi_agent/customer_service.json",
            "multi_agent/content_creation.json"
        ]
        
        for file_path in required_files:
            full_path = datasets_path / file_path
            if full_path.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Dataset file '{file_path}' exists"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Dataset file '{file_path}' missing"
                ))
    
    def _validate_documentation(self) -> None:
        """Validate documentation files."""
        print("📚 Validating Documentation...")
        
        doc_files = [
            "README.md",
            "ARCHITECTURE.md", 
            "GETTING_STARTED.md"
        ]
        
        for file_name in doc_files:
            file_path = self.project_root / file_name
            if file_path.exists() and file_path.stat().st_size > 100:  # Check file has content
                self.results.append(ValidationResult(
                    True, f"✅ Documentation file '{file_name}' exists and has content"
                ))
            elif file_path.exists():
                self.results.append(ValidationResult(
                    False, f"⚠️  Documentation file '{file_name}' exists but appears empty"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Documentation file '{file_name}' missing"
                ))
    
    def _validate_configuration_files(self) -> None:
        """Validate configuration files."""
        print("⚙️  Validating Configuration Files...")
        
        # Check .gitignore
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                content = f.read()
                if "framework-specific patterns" in content.lower():
                    self.results.append(ValidationResult(
                        True, "✅ .gitignore file exists with framework patterns"
                    ))
                else:
                    self.results.append(ValidationResult(
                        False, "⚠️  .gitignore exists but may be incomplete"
                    ))
        else:
            self.results.append(ValidationResult(
                False, "❌ .gitignore file missing"
            ))

    def _validate_infrastructure_templates(self) -> None:
        """Validate shared infrastructure templates."""
        print("🐳 Validating Infrastructure Templates...")

        infra_path = self.project_root / "shared_infrastructure"

        # Check Docker Compose template
        docker_template = infra_path / "docker-compose.template.yaml"
        if docker_template.exists():
            self.results.append(ValidationResult(
                True, "✅ Docker Compose template exists"
            ))

            # Validate template content
            try:
                with open(docker_template, 'r') as f:
                    content = f.read()

                required_services = ["qdrant", "langfuse", "postgres"]
                missing_services = []

                for service in required_services:
                    if service not in content:
                        missing_services.append(service)

                if not missing_services:
                    self.results.append(ValidationResult(
                        True, "✅ Docker template contains all required services"
                    ))
                else:
                    self.results.append(ValidationResult(
                        False, f"❌ Docker template missing services: {', '.join(missing_services)}"
                    ))

                # Check for environment variable placeholders
                env_vars = ["FRAMEWORK_NAME", "QDRANT_PORT", "LANGFUSE_PORT"]
                missing_vars = []

                for var in env_vars:
                    if f"${{{var}}}" not in content:
                        missing_vars.append(var)

                if not missing_vars:
                    self.results.append(ValidationResult(
                        True, "✅ Docker template has proper environment variable placeholders"
                    ))
                else:
                    self.results.append(ValidationResult(
                        False, f"❌ Docker template missing env vars: {', '.join(missing_vars)}"
                    ))

            except Exception as e:
                self.results.append(ValidationResult(
                    False, f"❌ Error reading Docker template: {str(e)}"
                ))
        else:
            self.results.append(ValidationResult(
                False, "❌ Docker Compose template missing"
            ))

        # Check External MCP Integration Guide
        mcp_guide = infra_path / "EXTERNAL_MCP_INTEGRATION.md"
        if mcp_guide.exists():
            self.results.append(ValidationResult(
                True, "✅ External MCP integration guide exists"
            ))
        else:
            self.results.append(ValidationResult(
                False, "❌ External MCP integration guide missing"
            ))

        # Check port allocation documentation
        port_doc = infra_path / "PORT_ALLOCATION.md"
        if port_doc.exists():
            self.results.append(ValidationResult(
                True, "✅ Port allocation documentation exists"
            ))
        else:
            self.results.append(ValidationResult(
                False, "❌ Port allocation documentation missing"
            ))

    def _validate_environment_templates(self) -> None:
        """Validate framework environment templates."""
        print("🔧 Validating Environment Templates...")

        frameworks = ["crewai", "dspy", "pocketflow", "google_adk", "pydantic_ai"]

        for framework in frameworks:
            framework_path = self.project_root / framework
            env_template = framework_path / ".env.template"

            if env_template.exists():
                self.results.append(ValidationResult(
                    True, f"✅ Environment template for '{framework}' exists"
                ))

                # Validate template content
                try:
                    with open(env_template, 'r') as f:
                        content = f.read()

                    # Check for required sections
                    required_sections = [
                        "Framework Identification",
                        "Infrastructure Port Configuration",
                        "LLM API Configuration",
                        "Database Connection URLs"
                    ]

                    missing_sections = []
                    for section in required_sections:
                        if section not in content:
                            missing_sections.append(section)

                    if not missing_sections:
                        self.results.append(ValidationResult(
                            True, f"✅ Environment template for '{framework}' has all required sections"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            False, f"❌ Environment template for '{framework}' missing sections: {', '.join(missing_sections)}"
                        ))

                    # Check for required environment variables
                    required_vars = [
                        "FRAMEWORK_NAME", "QDRANT_PORT", "LANGFUSE_PORT",
                        "OPENROUTER_API_KEY"
                    ]

                    missing_vars = []
                    for var in required_vars:
                        if f"{var}=" not in content:
                            missing_vars.append(var)

                    if not missing_vars:
                        self.results.append(ValidationResult(
                            True, f"✅ Environment template for '{framework}' has all required variables"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            False, f"❌ Environment template for '{framework}' missing variables: {', '.join(missing_vars)}"
                        ))

                except Exception as e:
                    self.results.append(ValidationResult(
                        False, f"❌ Error reading environment template for '{framework}': {str(e)}"
                    ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Environment template for '{framework}' missing"
                ))

    def _validate_json_file_structure(self) -> None:
        """Validate JSON file structure and syntax."""
        print("📄 Validating JSON File Structure...")

        datasets_path = self.project_root / "shared_datasets"

        # JSON files to validate
        json_files = [
            "qa/questions.json",
            "qa/answers.json",
            "qa/metadata.json",
            "rag_documents/ground_truth/expected_retrievals.json",
            "web_search/queries.json",
            "web_search/expected_sources.json",
            "multi_agent/research_tasks.json",
            "multi_agent/customer_service.json",
            "multi_agent/content_creation.json"
        ]

        for json_file in json_files:
            file_path = datasets_path / json_file

            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    # Basic structure validation
                    if isinstance(data, (dict, list)) and data:
                        self.results.append(ValidationResult(
                            True, f"✅ JSON file '{json_file}' has valid structure"
                        ))

                        # Specific validation based on file type
                        if "questions.json" in json_file:
                            self._validate_questions_json(data, json_file)
                        elif "metadata.json" in json_file:
                            self._validate_metadata_json(data, json_file)
                        elif "queries.json" in json_file:
                            self._validate_queries_json(data, json_file)

                    else:
                        self.results.append(ValidationResult(
                            False, f"❌ JSON file '{json_file}' is empty or has invalid structure"
                        ))

                except json.JSONDecodeError as e:
                    self.results.append(ValidationResult(
                        False, f"❌ JSON file '{json_file}' has syntax errors: {str(e)}"
                    ))
                except Exception as e:
                    self.results.append(ValidationResult(
                        False, f"❌ Error validating JSON file '{json_file}': {str(e)}"
                    ))
            else:
                # File doesn't exist - this is handled by other validation methods
                pass

    def _validate_questions_json(self, data: Any, file_name: str) -> None:
        """Validate questions.json structure."""
        if isinstance(data, list) and len(data) > 0:
            sample_question = data[0]
            required_fields = ["id", "question", "category"]

            missing_fields = [field for field in required_fields if field not in sample_question]

            if not missing_fields:
                self.results.append(ValidationResult(
                    True, f"✅ Questions JSON '{file_name}' has proper structure"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Questions JSON '{file_name}' missing fields: {', '.join(missing_fields)}"
                ))

    def _validate_metadata_json(self, data: Any, file_name: str) -> None:
        """Validate metadata.json structure."""
        if isinstance(data, dict):
            required_fields = ["dataset_name", "version", "description"]
            missing_fields = [field for field in required_fields if field not in data]

            if not missing_fields:
                self.results.append(ValidationResult(
                    True, f"✅ Metadata JSON '{file_name}' has proper structure"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Metadata JSON '{file_name}' missing fields: {', '.join(missing_fields)}"
                ))

    def _validate_queries_json(self, data: Any, file_name: str) -> None:
        """Validate queries.json structure."""
        if isinstance(data, list) and len(data) > 0:
            sample_query = data[0]
            required_fields = ["id", "query"]

            missing_fields = [field for field in required_fields if field not in sample_query]

            if not missing_fields:
                self.results.append(ValidationResult(
                    True, f"✅ Queries JSON '{file_name}' has proper structure"
                ))
            else:
                self.results.append(ValidationResult(
                    False, f"❌ Queries JSON '{file_name}' missing fields: {', '.join(missing_fields)}"
                ))

    def _validate_docker_template_syntax(self) -> None:
        """Validate Docker template syntax."""
        print("🐳 Validating Docker Template Syntax...")

        docker_template = self.project_root / "shared_infrastructure" / "docker-compose.template.yaml"

        if docker_template.exists():
            if not YAML_AVAILABLE:
                self.results.append(ValidationResult(
                    False, "❌ PyYAML not available - install with: pip install PyYAML"
                ))
                return

            try:
                with open(docker_template, 'r') as f:
                    content = f.read()

                # Parse YAML syntax
                yaml_data = yaml.safe_load(content)

                if yaml_data and isinstance(yaml_data, dict):
                    self.results.append(ValidationResult(
                        True, "✅ Docker template has valid YAML syntax"
                    ))

                    # Validate Docker Compose structure
                    required_top_level = ["version", "services"]
                    missing_top_level = [key for key in required_top_level if key not in yaml_data]

                    if not missing_top_level:
                        self.results.append(ValidationResult(
                            True, "✅ Docker template has proper Docker Compose structure"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            False, f"❌ Docker template missing top-level keys: {', '.join(missing_top_level)}"
                        ))

                    # Validate services structure
                    if "services" in yaml_data:
                        services = yaml_data["services"]
                        required_services = ["qdrant", "langfuse", "postgres"]

                        for service in required_services:
                            if service in services:
                                service_config = services[service]

                                # Check required service fields
                                if "image" in service_config or "build" in service_config:
                                    self.results.append(ValidationResult(
                                        True, f"✅ Service '{service}' has proper image/build configuration"
                                    ))
                                else:
                                    self.results.append(ValidationResult(
                                        False, f"❌ Service '{service}' missing image or build configuration"
                                    ))

                                # Check for container name
                                if "container_name" in service_config:
                                    container_name = service_config["container_name"]
                                    if "${FRAMEWORK_NAME}" in str(container_name):
                                        self.results.append(ValidationResult(
                                            True, f"✅ Service '{service}' has parameterized container name"
                                        ))
                                    else:
                                        self.results.append(ValidationResult(
                                            False, f"❌ Service '{service}' container name not parameterized"
                                        ))
                            else:
                                self.results.append(ValidationResult(
                                    False, f"❌ Required service '{service}' not found in template"
                                ))

                    # Validate environment variable usage
                    env_var_pattern = r'\$\{[A-Z_]+\}'
                    env_vars_found = re.findall(env_var_pattern, content)

                    if env_vars_found:
                        self.results.append(ValidationResult(
                            True, f"✅ Docker template uses environment variables: {len(set(env_vars_found))} unique vars"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            False, "❌ Docker template doesn't use environment variables for parameterization"
                        ))

                else:
                    self.results.append(ValidationResult(
                        False, "❌ Docker template has invalid YAML structure"
                    ))

            except yaml.YAMLError as e:
                self.results.append(ValidationResult(
                    False, f"❌ Docker template has YAML syntax errors: {str(e)}"
                ))
            except Exception as e:
                self.results.append(ValidationResult(
                    False, f"❌ Error validating Docker template: {str(e)}"
                ))
        else:
            # Template doesn't exist - this is handled by infrastructure validation
            pass
    
    def _print_results(self) -> None:
        """Print validation results summary."""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        if self.console:
            # Create results table
            table = Table(title="📋 Validation Results Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("✅ Passed", str(passed))
            table.add_row("❌ Failed", str(total - passed))
            table.add_row("📊 Success Rate", f"{passed/total*100:.1f}%")

            self.console.print(table)

            # Print failed checks if any
            failed_results = [r for r in self.results if not r.passed]
            if failed_results:
                self.console.print("\n[bold red]🚨 FAILED CHECKS:[/bold red]")
                for result in failed_results:
                    self.console.print(f"   {result.message}")
                    if result.details:
                        self.console.print(f"      [dim]{result.details}[/dim]")

            # Final status
            if passed == total:
                self.console.print(Panel.fit(
                    "🎉 ALL VALIDATIONS PASSED! Project structure is correct.",
                    style="bold green"
                ))
            else:
                self.console.print(Panel.fit(
                    "⚠️  Some validations failed. Please review and fix the issues above.",
                    style="bold yellow"
                ))
        else:
            # Fallback to plain text
            print("\n" + "="*60)
            print("📋 VALIDATION RESULTS SUMMARY")
            print("="*60)

            print(f"✅ Passed: {passed}")
            print(f"❌ Failed: {total - passed}")
            print(f"📊 Success Rate: {passed/total*100:.1f}%")

            # Print failed checks
            failed_results = [r for r in self.results if not r.passed]
            if failed_results:
                print("\n🚨 FAILED CHECKS:")
                for result in failed_results:
                    print(f"   {result.message}")
                    if result.details:
                        print(f"      {result.details}")

            print("\n" + "="*60)

            if passed == total:
                print("🎉 ALL VALIDATIONS PASSED! Project structure is correct.")
            else:
                print("⚠️  Some validations failed. Please review and fix the issues above.")

            print("="*60)


def main():
    """Main entry point for validation script."""
    # Create scripts directory if it doesn't exist
    scripts_dir = Path(__file__).parent
    scripts_dir.mkdir(exist_ok=True)
    
    # Run validation from project root
    project_root = scripts_dir.parent
    validator = StructureValidator(project_root)
    
    success = validator.validate_all()
    
    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
