# Zio-Booster Auto-Update Feature

## Overview
The Zio-Booster application includes an automatic update system that checks for new releases from the GitHub repository and automatically installs them when available.

## How It Works

### 1. Update Detection
- The system periodically checks the GitHub releases page at `https://github.com/aidandelange170-hub/Zio-Booster/releases`
- Compares the current application version with the latest release using semantic versioning
- Only downloads and installs newer versions

### 2. Update Process
- Downloads the latest release as a ZIP archive from GitHub
- Creates a backup of the current installation
- Extracts and installs the new version
- Preserves important configuration files during the update

### 3. Configuration
The update system is configured via `config/version.json`:

```json
{
  "current_version": "1.0.0",
  "last_update_check": "2023-06-01T00:00:00Z",
  "auto_update_enabled": true,
  "check_interval_hours": 24
}
```

## Features

### Automatic Checks
- Runs in the background on a configurable schedule (default: every 24 hours)
- Non-blocking operation - doesn't interfere with application performance
- Logs all update activities for debugging

### Manual Checks
- Users can manually check for updates via the "Check for Updates" button
- Shows real-time status during the update process
- Provides feedback on update success or failure

### Safe Installation
- Creates backups before installing updates
- Preserves user configurations
- Maintains application data integrity

## Technical Implementation

### Core Components

#### `utils/auto_updater.py`
- Handles GitHub API communication
- Manages download and installation process
- Version comparison logic

#### `utils/update_manager.py`
- Coordinates update checks
- Manages configuration and state
- Provides global interface for update operations

#### `utils/update_scheduler.py`
- Handles timed update checks
- Runs in a separate thread
- Configurable intervals

## Integration Points

### With Main Application (`src/main.py`)
- Initializes auto-update system on startup
- Adds "Check for Updates" button to UI
- Updates window title with current version
- Shows update status in application status bar

### Requirements
- `requests` library for HTTP communication
- `packaging` library for version comparison
- Standard Python libraries for file operations

## Security Considerations
- Downloads are verified through GitHub's secure API
- Updates are installed only from the official repository
- Backup mechanism allows for rollback if needed

## Troubleshooting

### Common Issues
- Network connectivity problems preventing update checks
- Permission issues during installation
- Version parsing errors

### Logging
All update activities are logged for troubleshooting purposes.

## Configuration Options

### Adjusting Check Frequency
Updates can be checked more or less frequently by modifying the `check_interval_hours` in the configuration file or through the update scheduler API.

### Disabling Auto-Updates
Auto-updates can be disabled by setting `auto_update_enabled` to `false` in the configuration file.