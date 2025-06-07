#!/bin/bash
# Database Backup Script Template for AI Agent Framework Infrastructure
# This script creates backups of PostgreSQL databases for each framework

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups/database}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Framework configurations
declare -A FRAMEWORKS=(
    ["dspy"]="5433"
    ["pocketflow"]="5434"
    ["crewai"]="5432"
    ["google_adk"]="5435"
    ["pydantic_ai"]="5436"
)

# Database configuration
DB_NAME="${DB_NAME:-langfuse}"
DB_USER="${DB_USER:-langfuse_user}"
DB_PASSWORD="${DB_PASSWORD:-langfuse_password}"
DB_HOST="${DB_HOST:-localhost}"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

error() {
    log "ERROR: $1"
    exit 1
}

# Check dependencies
check_dependencies() {
    if ! command -v pg_dump &> /dev/null; then
        error "pg_dump is not installed. Please install PostgreSQL client tools."
    fi
    
    if ! command -v docker &> /dev/null; then
        error "docker is not installed. Please install Docker."
    fi
}

# Create backup directory
create_backup_dir() {
    local framework=$1
    local backup_path="$BACKUP_DIR/$framework"
    
    mkdir -p "$backup_path"
    echo "$backup_path"
}

# Check if framework services are running
check_framework_running() {
    local framework=$1
    local container_name="${framework}_postgres"
    
    if ! docker ps --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        log "WARNING: PostgreSQL container for $framework is not running"
        return 1
    fi
    
    return 0
}

# Backup database for a specific framework
backup_framework_database() {
    local framework=$1
    local port=${FRAMEWORKS[$framework]}
    local backup_path=$(create_backup_dir "$framework")
    local backup_file="$backup_path/${framework}_${DB_NAME}_${TIMESTAMP}.sql"
    local backup_file_compressed="${backup_file}.gz"
    
    log "Starting backup for $framework (port: $port)"
    
    # Check if framework is running
    if ! check_framework_running "$framework"; then
        log "Skipping backup for $framework - services not running"
        return 0
    fi
    
    # Set password for pg_dump
    export PGPASSWORD="$DB_PASSWORD"
    
    # Create database backup
    if pg_dump \
        --host="$DB_HOST" \
        --port="$port" \
        --username="$DB_USER" \
        --dbname="$DB_NAME" \
        --verbose \
        --clean \
        --if-exists \
        --create \
        --format=plain \
        --file="$backup_file"; then
        
        log "Database backup created: $backup_file"
        
        # Compress backup
        if gzip "$backup_file"; then
            log "Backup compressed: $backup_file_compressed"
            
            # Verify backup integrity
            if gunzip -t "$backup_file_compressed" 2>/dev/null; then
                log "Backup integrity verified for $framework"
                
                # Create metadata file
                create_backup_metadata "$framework" "$backup_file_compressed"
                
                return 0
            else
                error "Backup integrity check failed for $framework"
            fi
        else
            error "Failed to compress backup for $framework"
        fi
    else
        error "Failed to create database backup for $framework"
    fi
    
    # Clean up password
    unset PGPASSWORD
}

# Create backup metadata
create_backup_metadata() {
    local framework=$1
    local backup_file=$2
    local metadata_file="${backup_file%.sql.gz}.metadata.json"
    
    cat > "$metadata_file" << EOF
{
    "framework": "$framework",
    "database": "$DB_NAME",
    "timestamp": "$TIMESTAMP",
    "backup_file": "$(basename "$backup_file")",
    "file_size": $(stat -c%s "$backup_file" 2>/dev/null || echo "0"),
    "checksum": "$(sha256sum "$backup_file" | cut -d' ' -f1)",
    "created_by": "$(whoami)",
    "host": "$(hostname)",
    "pg_dump_version": "$(pg_dump --version | head -n1)"
}
EOF
    
    log "Metadata created: $metadata_file"
}

# Clean up old backups
cleanup_old_backups() {
    local framework=$1
    local backup_path="$BACKUP_DIR/$framework"
    
    if [[ -d "$backup_path" ]]; then
        log "Cleaning up backups older than $RETENTION_DAYS days for $framework"
        
        find "$backup_path" -name "*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete
        find "$backup_path" -name "*.metadata.json" -type f -mtime +$RETENTION_DAYS -delete
        
        # Remove empty directories
        find "$backup_path" -type d -empty -delete 2>/dev/null || true
    fi
}

# Backup all frameworks
backup_all_frameworks() {
    local success_count=0
    local total_count=${#FRAMEWORKS[@]}
    
    log "Starting backup process for all frameworks"
    
    for framework in "${!FRAMEWORKS[@]}"; do
        log "Processing framework: $framework"
        
        if backup_framework_database "$framework"; then
            cleanup_old_backups "$framework"
            ((success_count++))
        else
            log "Failed to backup $framework"
        fi
    done
    
    log "Backup process completed: $success_count/$total_count frameworks backed up successfully"
    
    if [[ $success_count -eq $total_count ]]; then
        return 0
    else
        return 1
    fi
}

# Backup specific framework
backup_specific_framework() {
    local framework=$1
    
    if [[ ! ${FRAMEWORKS[$framework]+_} ]]; then
        error "Unknown framework: $framework. Available frameworks: ${!FRAMEWORKS[*]}"
    fi
    
    log "Starting backup process for framework: $framework"
    
    if backup_framework_database "$framework"; then
        cleanup_old_backups "$framework"
        log "Backup completed successfully for $framework"
        return 0
    else
        error "Backup failed for $framework"
    fi
}

# List available backups
list_backups() {
    local framework=${1:-}
    
    if [[ -n "$framework" ]]; then
        if [[ ! ${FRAMEWORKS[$framework]+_} ]]; then
            error "Unknown framework: $framework"
        fi
        
        local backup_path="$BACKUP_DIR/$framework"
        if [[ -d "$backup_path" ]]; then
            log "Backups for $framework:"
            find "$backup_path" -name "*.sql.gz" -type f -exec ls -lh {} \; | sort -k9
        else
            log "No backups found for $framework"
        fi
    else
        log "All available backups:"
        for fw in "${!FRAMEWORKS[@]}"; do
            local backup_path="$BACKUP_DIR/$fw"
            if [[ -d "$backup_path" ]] && [[ -n "$(find "$backup_path" -name "*.sql.gz" -type f)" ]]; then
                echo "Framework: $fw"
                find "$backup_path" -name "*.sql.gz" -type f -exec ls -lh {} \; | sort -k9
                echo
            fi
        done
    fi
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [COMMAND] [FRAMEWORK]

Commands:
    backup [FRAMEWORK]  Create backup for specific framework or all frameworks
    list [FRAMEWORK]    List available backups for specific framework or all frameworks
    help               Show this help message

Options:
    --backup-dir DIR   Set backup directory (default: $PROJECT_ROOT/backups/database)
    --retention DAYS   Set retention period in days (default: 7)
    --db-name NAME     Set database name (default: langfuse)
    --db-user USER     Set database user (default: langfuse_user)
    --db-password PASS Set database password (default: langfuse_password)
    --db-host HOST     Set database host (default: localhost)

Examples:
    $0 backup                    # Backup all frameworks
    $0 backup dspy              # Backup only DSPy framework
    $0 list                     # List all backups
    $0 list crewai              # List backups for CrewAI framework
    $0 --retention 14 backup    # Backup with 14-day retention

Available frameworks: ${!FRAMEWORKS[*]}
EOF
}

# Main function
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backup-dir)
                BACKUP_DIR="$2"
                shift 2
                ;;
            --retention)
                RETENTION_DAYS="$2"
                shift 2
                ;;
            --db-name)
                DB_NAME="$2"
                shift 2
                ;;
            --db-user)
                DB_USER="$2"
                shift 2
                ;;
            --db-password)
                DB_PASSWORD="$2"
                shift 2
                ;;
            --db-host)
                DB_HOST="$2"
                shift 2
                ;;
            backup)
                COMMAND="backup"
                if [[ $# -gt 1 ]] && [[ ! $2 =~ ^-- ]]; then
                    FRAMEWORK="$2"
                    shift
                fi
                shift
                ;;
            list)
                COMMAND="list"
                if [[ $# -gt 1 ]] && [[ ! $2 =~ ^-- ]]; then
                    FRAMEWORK="$2"
                    shift
                fi
                shift
                ;;
            help|--help|-h)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
    
    # Set default command
    COMMAND=${COMMAND:-backup}
    
    # Check dependencies
    check_dependencies
    
    # Execute command
    case $COMMAND in
        backup)
            if [[ -n "${FRAMEWORK:-}" ]]; then
                backup_specific_framework "$FRAMEWORK"
            else
                backup_all_frameworks
            fi
            ;;
        list)
            list_backups "${FRAMEWORK:-}"
            ;;
        *)
            error "Unknown command: $COMMAND"
            ;;
    esac
}

# Run main function
main "$@"
