# Backup Scripts for AI Agent Framework Infrastructure

This directory contains automated backup scripts for the infrastructure components of each AI agent framework.

## 📁 Available Scripts

### `backup_database.sh`
Automated PostgreSQL database backup script for Langfuse data.

**Features:**
- Framework-specific database backups
- Automatic compression and integrity verification
- Configurable retention policies
- Metadata generation for each backup
- Support for both individual and bulk framework backups

**Usage:**
```bash
# Backup all frameworks
./backup_database.sh backup

# Backup specific framework
./backup_database.sh backup dspy

# List available backups
./backup_database.sh list

# Custom retention period
./backup_database.sh --retention 14 backup
```

### `backup_qdrant.sh`
Automated Qdrant vector database backup script.

**Features:**
- Collection-level backup using Qdrant snapshots
- Automatic snapshot creation and download
- Framework isolation maintained
- Configurable retention policies
- Metadata tracking for each backup

**Usage:**
```bash
# Backup all frameworks
./backup_qdrant.sh backup

# Backup specific framework
./backup_qdrant.sh backup pocketflow

# List available backups
./backup_qdrant.sh list

# Custom backup directory
./backup_qdrant.sh --backup-dir /custom/path backup
```

## 🔧 Configuration

### Environment Variables

Both scripts support the following environment variables:

```bash
# Backup configuration
BACKUP_DIR="/path/to/backups"          # Custom backup directory
RETENTION_DAYS="7"                     # Backup retention in days

# Database configuration (backup_database.sh)
DB_NAME="langfuse"                     # Database name
DB_USER="langfuse_user"                # Database username
DB_PASSWORD="langfuse_password"        # Database password
DB_HOST="localhost"                    # Database host

# Qdrant configuration (backup_qdrant.sh)
QDRANT_HOST="localhost"                # Qdrant host
```

### Framework Port Mapping

The scripts automatically use the correct ports for each framework:

| Framework   | PostgreSQL Port | Qdrant Port |
|-------------|----------------|-------------|
| DSPy        | 5433           | 6334        |
| PocketFlow  | 5434           | 6335        |
| CrewAI      | 5432           | 6333        |
| Google ADK  | 5435           | 6336        |
| Pydantic AI | 5436           | 6337        |

## 📋 Prerequisites

### System Dependencies

**For database backups:**
- `pg_dump` (PostgreSQL client tools)
- `gzip` (compression)
- `docker` (container management)

**For Qdrant backups:**
- `curl` (HTTP requests)
- `docker` (container management)
- `jq` (JSON parsing, optional but recommended)

### Installation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql-client gzip curl jq docker.io
```

**macOS:**
```bash
brew install postgresql gzip curl jq docker
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql gzip curl jq docker
```

## 🚀 Quick Start

### 1. Set Up Backup Directory

```bash
# Create backup directory structure
mkdir -p /path/to/backups/{database,qdrant}

# Set permissions
chmod 755 /path/to/backups
```

### 2. Configure Environment

```bash
# Create environment file
cat > backup.env << EOF
BACKUP_DIR="/path/to/backups"
RETENTION_DAYS="14"
DB_PASSWORD="your_secure_password"
EOF

# Source environment
source backup.env
```

### 3. Run Initial Backup

```bash
# Test with single framework
./backup_database.sh backup dspy
./backup_qdrant.sh backup dspy

# Backup all frameworks
./backup_database.sh backup
./backup_qdrant.sh backup
```

### 4. Verify Backups

```bash
# List all backups
./backup_database.sh list
./backup_qdrant.sh list

# Check backup directory
ls -la /path/to/backups/
```

## ⏰ Automated Scheduling

### Using Cron

Add to your crontab for automated backups:

```bash
# Edit crontab
crontab -e

# Add backup jobs (daily at 2 AM)
0 2 * * * /path/to/shared_infrastructure/backup_scripts/backup_database.sh backup
15 2 * * * /path/to/shared_infrastructure/backup_scripts/backup_qdrant.sh backup
```

### Using Systemd Timers

Create systemd service and timer files:

```bash
# Create service file
sudo tee /etc/systemd/system/ai-framework-backup.service << EOF
[Unit]
Description=AI Framework Infrastructure Backup
After=docker.service

[Service]
Type=oneshot
User=your_user
WorkingDirectory=/path/to/shared_infrastructure/backup_scripts
ExecStart=/bin/bash -c './backup_database.sh backup && ./backup_qdrant.sh backup'
EOF

# Create timer file
sudo tee /etc/systemd/system/ai-framework-backup.timer << EOF
[Unit]
Description=Run AI Framework Backup Daily
Requires=ai-framework-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start timer
sudo systemctl enable ai-framework-backup.timer
sudo systemctl start ai-framework-backup.timer
```

## 🔍 Monitoring and Alerting

### Log Monitoring

Both scripts log to stderr with timestamps. Redirect logs for monitoring:

```bash
# Run with logging
./backup_database.sh backup 2>&1 | tee backup.log

# Monitor logs in real-time
tail -f backup.log
```

### Health Checks

Create a health check script:

```bash
#!/bin/bash
# backup_health_check.sh

BACKUP_DIR="/path/to/backups"
MAX_AGE_HOURS=25  # Alert if no backup in 25 hours

for framework in dspy pocketflow crewai google_adk pydantic_ai; do
    # Check database backup
    db_backup=$(find "$BACKUP_DIR/database/$framework" -name "*.sql.gz" -mtime -1 2>/dev/null | head -1)
    if [[ -z "$db_backup" ]]; then
        echo "ALERT: No recent database backup for $framework"
    fi
    
    # Check Qdrant backup
    qdrant_backup=$(find "$BACKUP_DIR/qdrant/$framework" -name "${framework}_*" -mtime -1 2>/dev/null | head -1)
    if [[ -z "$qdrant_backup" ]]; then
        echo "ALERT: No recent Qdrant backup for $framework"
    fi
done
```

## 🔄 Disaster Recovery

### Database Restoration

```bash
# Restore database from backup
gunzip -c backup_file.sql.gz | psql -h localhost -p 5433 -U langfuse_user -d langfuse
```

### Qdrant Restoration

```bash
# Stop Qdrant service
docker-compose stop qdrant

# Copy backup to Qdrant data directory
cp backup_file /path/to/qdrant/data/

# Restart Qdrant service
docker-compose start qdrant

# Restore collection from snapshot via API
curl -X PUT "http://localhost:6334/collections/collection_name/snapshots/snapshot_name/recover"
```

## 🛠️ Troubleshooting

### Common Issues

**Permission Denied:**
```bash
# Fix script permissions
chmod +x backup_*.sh

# Fix backup directory permissions
sudo chown -R $USER:$USER /path/to/backups
```

**PostgreSQL Connection Failed:**
```bash
# Check if container is running
docker ps | grep postgres

# Verify connection
pg_isready -h localhost -p 5433 -U langfuse_user
```

**Qdrant API Errors:**
```bash
# Check Qdrant health
curl http://localhost:6334/health

# Verify collections
curl http://localhost:6334/collections
```

**Disk Space Issues:**
```bash
# Check available space
df -h /path/to/backups

# Clean old backups manually
find /path/to/backups -name "*.sql.gz" -mtime +30 -delete
```

### Debug Mode

Run scripts with verbose output:

```bash
# Enable debug mode
set -x

# Run backup with debug
./backup_database.sh backup dspy

# Disable debug mode
set +x
```

## 📊 Backup Verification

### Integrity Checks

Both scripts generate checksums for verification:

```bash
# Verify database backup integrity
gunzip -t backup_file.sql.gz

# Verify checksum
sha256sum -c backup_file.metadata.json
```

### Test Restoration

Regularly test backup restoration in a test environment:

```bash
# Create test database
createdb -h localhost -p 5433 -U langfuse_user test_restore

# Restore backup
gunzip -c backup_file.sql.gz | psql -h localhost -p 5433 -U langfuse_user -d test_restore

# Verify data
psql -h localhost -p 5433 -U langfuse_user -d test_restore -c "SELECT COUNT(*) FROM traces;"

# Clean up
dropdb -h localhost -p 5433 -U langfuse_user test_restore
```

## 🔒 Security Considerations

### Backup Encryption

For sensitive data, consider encrypting backups:

```bash
# Encrypt backup
gpg --symmetric --cipher-algo AES256 backup_file.sql.gz

# Decrypt backup
gpg --decrypt backup_file.sql.gz.gpg > backup_file.sql.gz
```

### Access Controls

- Store backups in secure locations with appropriate permissions
- Use dedicated backup user accounts with minimal privileges
- Implement backup retention policies to comply with data regulations
- Regular audit backup access and procedures

### Network Security

- Use secure connections for remote backups
- Implement firewall rules for backup traffic
- Consider VPN for backup transfers over public networks
