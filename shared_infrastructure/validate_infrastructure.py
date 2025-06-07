#!/usr/bin/env python3
"""
Infrastructure Validation Tools for AI Agent Framework Infrastructure

This script provides comprehensive validation and health checking for the
infrastructure services including Qdrant, Langfuse, PostgreSQL, and MCP servers.
"""

import json
import socket
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
from pydantic import BaseModel, Field, ConfigDict

# Optional dependencies - gracefully handle missing packages
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    """Status information for a service."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    name: str = Field(
        ...,
        description="Service name (e.g., 'Qdrant', 'PostgreSQL', 'Langfuse')",
        min_length=1,
        max_length=50
    )
    host: str = Field(
        ...,
        description="Service host address",
        min_length=1,
        max_length=255
    )
    port: int = Field(
        ...,
        description="Service port number",
        ge=1,
        le=65535
    )
    status: str = Field(
        ...,
        description="Service health status",
        pattern=r'^(healthy|unhealthy|unreachable)$'
    )
    response_time_ms: Optional[float] = Field(
        default=None,
        description="Response time in milliseconds",
        ge=0
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if service is unhealthy",
        max_length=1000
    )
    additional_info: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional service-specific information"
    )


class FrameworkHealthReport(BaseModel):
    """Health report for a complete framework infrastructure."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    framework_name: str = Field(
        ...,
        description="Name of the framework being reported on",
        min_length=1,
        max_length=50,
        pattern=r'^[a-z][a-z0-9_]*$'
    )
    timestamp: datetime = Field(
        ...,
        description="Timestamp when the health report was generated"
    )
    overall_status: str = Field(
        ...,
        description="Overall health status of the framework",
        pattern=r'^(healthy|degraded|unhealthy)$'
    )
    services: List[ServiceStatus] = Field(
        ...,
        description="List of individual service status reports",
        min_length=0
    )
    summary: Dict[str, Any] = Field(
        ...,
        description="Summary statistics and information"
    )


class ServiceValidator:
    """Base class for service validation."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def check_port_connectivity(self, host: str, port: int) -> Tuple[bool, Optional[str]]:
        """
        Check if a port is reachable.
        
        Args:
            host: Host to check
            port: Port to check
            
        Returns:
            Tuple of (is_reachable, error_message)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((host, port))
                if result == 0:
                    return True, None
                else:
                    return False, f"Connection refused on {host}:{port}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"


class QdrantValidator(ServiceValidator):
    """Validator for Qdrant vector database."""
    
    def validate_service(self, host: str, port: int) -> ServiceStatus:
        """
        Validate Qdrant service health and functionality.

        Args:
            host: Qdrant host
            port: Qdrant port

        Returns:
            ServiceStatus object with validation results
        """
        if not REQUESTS_AVAILABLE:
            return ServiceStatus(
                name="Qdrant",
                host=host,
                port=port,
                status="unhealthy",
                error_message="requests library not available - install with: pip install requests"
            )

        start_time = time.time()

        # Check port connectivity
        is_reachable, conn_error = self.check_port_connectivity(host, port)
        if not is_reachable:
            return ServiceStatus(
                name="Qdrant",
                host=host,
                port=port,
                status="unreachable",
                error_message=conn_error
            )

        try:
            # Check health endpoint
            health_url = f"http://{host}:{port}/health"
            response = requests.get(health_url, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                # Test basic functionality
                collections_url = f"http://{host}:{port}/collections"
                collections_response = requests.get(collections_url, timeout=self.timeout)
                
                additional_info = {
                    "health_status": response.json() if response.content else {},
                    "collections_accessible": collections_response.status_code == 200,
                    "version": response.headers.get("server", "unknown")
                }
                
                return ServiceStatus(
                    name="Qdrant",
                    host=host,
                    port=port,
                    status="healthy",
                    response_time_ms=response_time,
                    additional_info=additional_info
                )
            else:
                return ServiceStatus(
                    name="Qdrant",
                    host=host,
                    port=port,
                    status="unhealthy",
                    response_time_ms=response_time,
                    error_message=f"Health check failed: HTTP {response.status_code}"
                )
                
        except requests.RequestException as e:
            return ServiceStatus(
                name="Qdrant",
                host=host,
                port=port,
                status="unhealthy",
                error_message=f"HTTP request failed: {str(e)}"
            )


class PostgreSQLValidator(ServiceValidator):
    """Validator for PostgreSQL database."""
    
    def validate_service(self, host: str, port: int, database: str,
                        username: str, password: str) -> ServiceStatus:
        """
        Validate PostgreSQL service health and connectivity.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            username: Database username
            password: Database password

        Returns:
            ServiceStatus object with validation results
        """
        if not PSYCOPG2_AVAILABLE:
            return ServiceStatus(
                name="PostgreSQL",
                host=host,
                port=port,
                status="unhealthy",
                error_message="psycopg2 library not available - install with: pip install psycopg2-binary"
            )

        start_time = time.time()

        # Check port connectivity
        is_reachable, conn_error = self.check_port_connectivity(host, port)
        if not is_reachable:
            return ServiceStatus(
                name="PostgreSQL",
                host=host,
                port=port,
                status="unreachable",
                error_message=conn_error
            )

        try:
            # Test database connection
            conn_string = f"host={host} port={port} dbname={database} user={username} password={password}"
            conn = psycopg2.connect(conn_string)
            
            response_time = (time.time() - start_time) * 1000
            
            # Test basic functionality
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            additional_info = {
                "version": version,
                "table_count": table_count,
                "database": database
            }
            
            return ServiceStatus(
                name="PostgreSQL",
                host=host,
                port=port,
                status="healthy",
                response_time_ms=response_time,
                additional_info=additional_info
            )
            
        except psycopg2.Error as e:
            return ServiceStatus(
                name="PostgreSQL",
                host=host,
                port=port,
                status="unhealthy",
                error_message=f"Database connection failed: {str(e)}"
            )


class LangfuseValidator(ServiceValidator):
    """Validator for Langfuse observability platform."""
    
    def validate_service(self, host: str, port: int) -> ServiceStatus:
        """
        Validate Langfuse service health and functionality.

        Args:
            host: Langfuse host
            port: Langfuse port

        Returns:
            ServiceStatus object with validation results
        """
        if not REQUESTS_AVAILABLE:
            return ServiceStatus(
                name="Langfuse",
                host=host,
                port=port,
                status="unhealthy",
                error_message="requests library not available - install with: pip install requests"
            )

        start_time = time.time()

        # Check port connectivity
        is_reachable, conn_error = self.check_port_connectivity(host, port)
        if not is_reachable:
            return ServiceStatus(
                name="Langfuse",
                host=host,
                port=port,
                status="unreachable",
                error_message=conn_error
            )

        try:
            # Check health endpoint
            health_url = f"http://{host}:{port}/api/public/health"
            response = requests.get(health_url, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                health_data = response.json() if response.content else {}
                
                # Test API accessibility
                api_url = f"http://{host}:{port}/api/public/projects"
                api_response = requests.get(api_url, timeout=self.timeout)
                
                additional_info = {
                    "health_data": health_data,
                    "api_accessible": api_response.status_code in [200, 401, 403],  # 401/403 means API is working but needs auth
                    "version": health_data.get("version", "unknown")
                }
                
                return ServiceStatus(
                    name="Langfuse",
                    host=host,
                    port=port,
                    status="healthy",
                    response_time_ms=response_time,
                    additional_info=additional_info
                )
            else:
                return ServiceStatus(
                    name="Langfuse",
                    host=host,
                    port=port,
                    status="unhealthy",
                    response_time_ms=response_time,
                    error_message=f"Health check failed: HTTP {response.status_code}"
                )
                
        except requests.RequestException as e:
            return ServiceStatus(
                name="Langfuse",
                host=host,
                port=port,
                status="unhealthy",
                error_message=f"HTTP request failed: {str(e)}"
            )


class InfrastructureValidator:
    """Main infrastructure validation orchestrator."""

    # Framework configurations
    FRAMEWORK_CONFIGS = {
        'dspy': {'qdrant_port': 6334, 'langfuse_port': 3001, 'postgres_port': 5433},
        'pocketflow': {'qdrant_port': 6335, 'langfuse_port': 3002, 'postgres_port': 5434},
        'crewai': {'qdrant_port': 6333, 'langfuse_port': 3000, 'postgres_port': 5432},
        'google_adk': {'qdrant_port': 6336, 'langfuse_port': 3003, 'postgres_port': 5435},
        'pydantic_ai': {'qdrant_port': 6337, 'langfuse_port': 3004, 'postgres_port': 5436},
    }

    def __init__(self, timeout: int = 10):
        """
        Initialize the infrastructure validator.

        Args:
            timeout: Timeout for service checks in seconds
        """
        self.timeout = timeout
        self.qdrant_validator = QdrantValidator(timeout)
        self.postgres_validator = PostgreSQLValidator(timeout)
        self.langfuse_validator = LangfuseValidator(timeout)

    def validate_framework_infrastructure(self, framework_name: str,
                                        host: str = "localhost",
                                        postgres_user: str = "langfuse_user",
                                        postgres_password: str = "langfuse_password") -> FrameworkHealthReport:
        """
        Validate complete infrastructure for a framework.

        Args:
            framework_name: Name of the framework to validate
            host: Host where services are running
            postgres_user: PostgreSQL username
            postgres_password: PostgreSQL password

        Returns:
            FrameworkHealthReport with validation results
        """
        if framework_name not in self.FRAMEWORK_CONFIGS:
            raise ValueError(f"Unknown framework: {framework_name}")

        config = self.FRAMEWORK_CONFIGS[framework_name]
        services = []

        logger.info(f"Validating infrastructure for {framework_name}")

        # Validate Qdrant
        logger.info(f"Checking Qdrant on port {config['qdrant_port']}")
        qdrant_status = self.qdrant_validator.validate_service(host, config['qdrant_port'])
        services.append(qdrant_status)

        # Validate PostgreSQL
        logger.info(f"Checking PostgreSQL on port {config['postgres_port']}")
        postgres_status = self.postgres_validator.validate_service(
            host, config['postgres_port'], "langfuse", postgres_user, postgres_password
        )
        services.append(postgres_status)

        # Validate Langfuse
        logger.info(f"Checking Langfuse on port {config['langfuse_port']}")
        langfuse_status = self.langfuse_validator.validate_service(host, config['langfuse_port'])
        services.append(langfuse_status)

        # Determine overall status
        healthy_count = sum(1 for s in services if s.status == "healthy")
        total_count = len(services)

        if healthy_count == total_count:
            overall_status = "healthy"
        elif healthy_count > 0:
            overall_status = "degraded"
        else:
            overall_status = "unhealthy"

        # Generate summary
        summary = {
            "total_services": total_count,
            "healthy_services": healthy_count,
            "unhealthy_services": sum(1 for s in services if s.status == "unhealthy"),
            "unreachable_services": sum(1 for s in services if s.status == "unreachable"),
            "average_response_time_ms": sum(s.response_time_ms for s in services if s.response_time_ms) / max(1, sum(1 for s in services if s.response_time_ms))
        }

        return FrameworkHealthReport(
            framework_name=framework_name,
            timestamp=datetime.now(),
            overall_status=overall_status,
            services=services,
            summary=summary
        )

    def validate_all_frameworks(self, host: str = "localhost") -> Dict[str, FrameworkHealthReport]:
        """
        Validate infrastructure for all frameworks.

        Args:
            host: Host where services are running

        Returns:
            Dictionary mapping framework names to health reports
        """
        results = {}

        for framework_name in self.FRAMEWORK_CONFIGS.keys():
            try:
                report = self.validate_framework_infrastructure(framework_name, host)
                results[framework_name] = report
            except Exception as e:
                logger.error(f"Failed to validate {framework_name}: {e}")
                # Create error report
                error_report = FrameworkHealthReport(
                    framework_name=framework_name,
                    timestamp=datetime.now(),
                    overall_status="unhealthy",
                    services=[],
                    summary={"error": str(e)}
                )
                results[framework_name] = error_report

        return results

    def generate_health_report(self, reports: Dict[str, FrameworkHealthReport],
                             output_path: Optional[Path] = None) -> str:
        """
        Generate a comprehensive health report.

        Args:
            reports: Dictionary of framework health reports
            output_path: Optional path to save the report

        Returns:
            Report content as string
        """
        report_lines = []
        report_lines.append("# Infrastructure Health Report")
        report_lines.append(f"Generated: {datetime.now().isoformat()}")
        report_lines.append("")

        # Overall summary
        total_frameworks = len(reports)
        healthy_frameworks = sum(1 for r in reports.values() if r.overall_status == "healthy")
        degraded_frameworks = sum(1 for r in reports.values() if r.overall_status == "degraded")
        unhealthy_frameworks = sum(1 for r in reports.values() if r.overall_status == "unhealthy")

        report_lines.append("## Overall Summary")
        report_lines.append(f"- Total Frameworks: {total_frameworks}")
        report_lines.append(f"- Healthy: {healthy_frameworks}")
        report_lines.append(f"- Degraded: {degraded_frameworks}")
        report_lines.append(f"- Unhealthy: {unhealthy_frameworks}")
        report_lines.append("")

        # Framework details
        for framework_name, report in reports.items():
            report_lines.append(f"## {framework_name.upper()} Framework")
            report_lines.append(f"**Status**: {report.overall_status.upper()}")
            report_lines.append("")

            if "error" in report.summary:
                report_lines.append(f"**Error**: {report.summary['error']}")
                report_lines.append("")
                continue

            # Service details
            report_lines.append("### Services")
            for service in report.services:
                status_emoji = "✅" if service.status == "healthy" else "❌" if service.status == "unhealthy" else "⚠️"
                report_lines.append(f"- {status_emoji} **{service.name}** ({service.host}:{service.port})")
                report_lines.append(f"  - Status: {service.status}")
                if service.response_time_ms:
                    report_lines.append(f"  - Response Time: {service.response_time_ms:.2f}ms")
                if service.error_message:
                    report_lines.append(f"  - Error: {service.error_message}")
                report_lines.append("")

            # Summary stats
            report_lines.append("### Summary")
            for key, value in report.summary.items():
                if key != "error":
                    report_lines.append(f"- {key.replace('_', ' ').title()}: {value}")
            report_lines.append("")

        report_content = "\n".join(report_lines)

        # Save to file if requested
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report_content)
            logger.info(f"Health report saved to: {output_path}")

        return report_content


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate AI agent framework infrastructure")
    parser.add_argument('--framework', '-f', help="Framework name to validate (default: all)")
    parser.add_argument('--host', default="localhost", help="Host where services are running")
    parser.add_argument('--timeout', '-t', type=int, default=10, help="Timeout for service checks")
    parser.add_argument('--output', '-o', help="Output file for health report")
    parser.add_argument('--json', action='store_true', help="Output results in JSON format")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        validator = InfrastructureValidator(timeout=args.timeout)

        if args.framework:
            # Validate specific framework
            if args.framework not in validator.FRAMEWORK_CONFIGS:
                print(f"Error: Unknown framework '{args.framework}'")
                print(f"Available frameworks: {', '.join(validator.FRAMEWORK_CONFIGS.keys())}")
                return 1

            report = validator.validate_framework_infrastructure(args.framework, args.host)
            reports = {args.framework: report}
        else:
            # Validate all frameworks
            reports = validator.validate_all_frameworks(args.host)

        if args.json:
            # Output JSON format
            json_data = {}
            for name, report in reports.items():
                json_data[name] = {
                    'framework_name': report.framework_name,
                    'timestamp': report.timestamp.isoformat(),
                    'overall_status': report.overall_status,
                    'services': [service.model_dump() for service in report.services],
                    'summary': report.summary
                }

            output_content = json.dumps(json_data, indent=2)
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_content)
            else:
                print(output_content)
        else:
            # Output markdown format
            output_path = Path(args.output) if args.output else None
            report_content = validator.generate_health_report(reports, output_path)
            if not args.output:
                print(report_content)

        # Return appropriate exit code
        all_healthy = all(r.overall_status == "healthy" for r in reports.values())
        return 0 if all_healthy else 1

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
