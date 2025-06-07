#!/usr/bin/env python3
"""
Project Structure Validation Script

This script validates that the AI Agent Frameworks Comparison Project
directory structure matches the specification and all required files exist.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


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
    
    def validate_all(self) -> bool:
        """
        Run all validation checks.
        
        Returns:
            True if all validations pass, False otherwise.
        """
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
    
    def _print_results(self) -> None:
        """Print validation results summary."""
        print("\n" + "="*60)
        print("📋 VALIDATION RESULTS SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
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
