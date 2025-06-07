#!/bin/bash
# Qdrant Vector Database Backup Script Template
# This script creates backups of Qdrant vector databases for each framework

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups/qdrant}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Framework configurations
declare -A FRAMEWORKS=(
    ["dspy"]="6334"
    ["pocketflow"]="6335"
    ["crewai"]="6333"
    ["google_adk"]="6336"
    ["pydantic_ai"]="6337"
)

# Qdrant configuration
QDRANT_HOST="${QDRANT_HOST:-localhost}"

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
    if ! command -v curl &> /dev/null; then
        error "curl is not installed. Please install curl."
    fi
    
    if ! command -v docker &> /dev/null; then
        error "docker is not installed. Please install Docker."
    fi
    
    if ! command -v jq &> /dev/null; then
        log "WARNING: jq is not installed. JSON parsing will be limited."
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
    local container_name="${framework}_qdrant"
    
    if ! docker ps --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        log "WARNING: Qdrant container for $framework is not running"
        return 1
    fi
    
    return 0
}

# Check Qdrant health
check_qdrant_health() {
    local framework=$1
    local port=${FRAMEWORKS[$framework]}
    local health_url="http://$QDRANT_HOST:$port/health"
    
    if curl -s -f "$health_url" > /dev/null; then
        return 0
    else
        log "WARNING: Qdrant health check failed for $framework (port: $port)"
        return 1
    fi
}

# Get Qdrant collections
get_collections() {
    local framework=$1
    local port=${FRAMEWORKS[$framework]}
    local collections_url="http://$QDRANT_HOST:$port/collections"
    
    if command -v jq &> /dev/null; then
        curl -s "$collections_url" | jq -r '.result.collections[].name' 2>/dev/null || echo ""
    else
        # Fallback without jq
        curl -s "$collections_url" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 || echo ""
    fi
}

# Create Qdrant snapshot
create_qdrant_snapshot() {
    local framework=$1
    local collection=$2
    local port=${FRAMEWORKS[$framework]}
    local snapshot_url="http://$QDRANT_HOST:$port/collections/$collection/snapshots"
    
    log "Creating snapshot for collection '$collection' in $framework"
    
    # Create snapshot
    local response=$(curl -s -X POST "$snapshot_url" -H "Content-Type: application/json")
    
    if command -v jq &> /dev/null; then
        local snapshot_name=$(echo "$response" | jq -r '.result.name' 2>/dev/null)
    else
        # Fallback without jq
        local snapshot_name=$(echo "$response" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    fi
    
    if [[ -n "$snapshot_name" && "$snapshot_name" != "null" ]]; then
        log "Snapshot created: $snapshot_name"
        echo "$snapshot_name"
        return 0
    else
        log "Failed to create snapshot for collection '$collection'"
        return 1
    fi
}

# Download Qdrant snapshot
download_qdrant_snapshot() {
    local framework=$1
    local collection=$2
    local snapshot_name=$3
    local port=${FRAMEWORKS[$framework]}
    local backup_path=$4
    
    local download_url="http://$QDRANT_HOST:$port/collections/$collection/snapshots/$snapshot_name"
    local backup_file="$backup_path/${framework}_${collection}_${snapshot_name}"
    
    log "Downloading snapshot: $snapshot_name"
    
    if curl -s -o "$backup_file" "$download_url"; then
        log "Snapshot downloaded: $backup_file"
        
        # Verify file was downloaded and has content
        if [[ -f "$backup_file" && -s "$backup_file" ]]; then
            # Create metadata
            create_backup_metadata "$framework" "$collection" "$backup_file" "$snapshot_name"
            echo "$backup_file"
            return 0
        else
            log "Downloaded file is empty or missing"
            rm -f "$backup_file"
            return 1
        fi
    else
        log "Failed to download snapshot: $snapshot_name"
        return 1
    fi
}

# Delete Qdrant snapshot from server
delete_qdrant_snapshot() {
    local framework=$1
    local collection=$2
    local snapshot_name=$3
    local port=${FRAMEWORKS[$framework]}
    
    local delete_url="http://$QDRANT_HOST:$port/collections/$collection/snapshots/$snapshot_name"
    
    if curl -s -X DELETE "$delete_url" > /dev/null; then
        log "Snapshot deleted from server: $snapshot_name"
        return 0
    else
        log "WARNING: Failed to delete snapshot from server: $snapshot_name"
        return 1
    fi
}

# Create backup metadata
create_backup_metadata() {
    local framework=$1
    local collection=$2
    local backup_file=$3
    local snapshot_name=$4
    local metadata_file="${backup_file}.metadata.json"
    
    cat > "$metadata_file" << EOF
{
    "framework": "$framework",
    "collection": "$collection",
    "snapshot_name": "$snapshot_name",
    "timestamp": "$TIMESTAMP",
    "backup_file": "$(basename "$backup_file")",
    "file_size": $(stat -c%s "$backup_file" 2>/dev/null || echo "0"),
    "checksum": "$(sha256sum "$backup_file" | cut -d' ' -f1)",
    "created_by": "$(whoami)",
    "host": "$(hostname)",
    "qdrant_host": "$QDRANT_HOST",
    "qdrant_port": "${FRAMEWORKS[$framework]}"
}
EOF
    
    log "Metadata created: $metadata_file"
}

# Backup collections for a specific framework
backup_framework_collections() {
    local framework=$1
    local backup_path=$(create_backup_dir "$framework")
    local success_count=0
    local total_count=0
    
    log "Starting backup for $framework"
    
    # Check if framework is running
    if ! check_framework_running "$framework"; then
        log "Skipping backup for $framework - services not running"
        return 0
    fi
    
    # Check Qdrant health
    if ! check_qdrant_health "$framework"; then
        log "Skipping backup for $framework - Qdrant not healthy"
        return 0
    fi
    
    # Get collections
    local collections=$(get_collections "$framework")
    
    if [[ -z "$collections" ]]; then
        log "No collections found for $framework"
        return 0
    fi
    
    # Backup each collection
    while IFS= read -r collection; do
        if [[ -n "$collection" ]]; then
            ((total_count++))
            log "Backing up collection: $collection"
            
            # Create snapshot
            local snapshot_name=$(create_qdrant_snapshot "$framework" "$collection")
            
            if [[ -n "$snapshot_name" ]]; then
                # Download snapshot
                local backup_file=$(download_qdrant_snapshot "$framework" "$collection" "$snapshot_name" "$backup_path")
                
                if [[ -n "$backup_file" ]]; then
                    # Clean up snapshot from server
                    delete_qdrant_snapshot "$framework" "$collection" "$snapshot_name"
                    ((success_count++))
                    log "Successfully backed up collection: $collection"
                else
                    log "Failed to download backup for collection: $collection"
                fi
            else
                log "Failed to create snapshot for collection: $collection"
            fi
        fi
    done <<< "$collections"
    
    log "Backup completed for $framework: $success_count/$total_count collections backed up"
    
    if [[ $total_count -eq 0 ]]; then
        return 0
    elif [[ $success_count -eq $total_count ]]; then
        return 0
    else
        return 1
    fi
}

# Clean up old backups
cleanup_old_backups() {
    local framework=$1
    local backup_path="$BACKUP_DIR/$framework"
    
    if [[ -d "$backup_path" ]]; then
        log "Cleaning up backups older than $RETENTION_DAYS days for $framework"
        
        find "$backup_path" -name "${framework}_*" -type f -mtime +$RETENTION_DAYS -delete
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
        
        if backup_framework_collections "$framework"; then
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
    
    if backup_framework_collections "$framework"; then
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
            log "Qdrant backups for $framework:"
            find "$backup_path" -name "${framework}_*" -type f ! -name "*.metadata.json" -exec ls -lh {} \; | sort -k9
        else
            log "No Qdrant backups found for $framework"
        fi
    else
        log "All available Qdrant backups:"
        for fw in "${!FRAMEWORKS[@]}"; do
            local backup_path="$BACKUP_DIR/$fw"
            if [[ -d "$backup_path" ]] && [[ -n "$(find "$backup_path" -name "${fw}_*" -type f ! -name "*.metadata.json")" ]]; then
                echo "Framework: $fw"
                find "$backup_path" -name "${fw}_*" -type f ! -name "*.metadata.json" -exec ls -lh {} \; | sort -k9
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
    --backup-dir DIR   Set backup directory (default: $PROJECT_ROOT/backups/qdrant)
    --retention DAYS   Set retention period in days (default: 7)
    --host HOST        Set Qdrant host (default: localhost)

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
            --host)
                QDRANT_HOST="$2"
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
