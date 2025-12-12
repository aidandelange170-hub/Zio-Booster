# ZioBooster Installation and Usage Guide

## Overview
ZioBooster is an advanced FPS boosting application that optimizes your system for better gaming performance. This application includes features like system monitoring, resource optimization, process management, and customizable performance profiles.

## New Features Added

### 1. System Profiles
- **Gaming Profile**: Optimizes system for maximum gaming performance
- **Performance Profile**: Sets system to highest performance mode
- **Battery Saver**: Reduces resource usage for better battery life
- **Default Profile**: Balanced optimization

### 2. Enhanced UI Controls
- Profile selection dropdown
- "Kill High CPU" button to terminate resource-heavy processes
- "Export Log" button to save optimization history
- Improved process monitoring with resource scores

### 3. Process Management
- Automatic termination of high-resource processes
- Process monitoring with detailed metrics
- Optimization logging with timestamps

### 4. Windows Installation Scripts
- PowerShell script (`install_and_run.ps1`) for easy installation and execution
- Batch script (`install_and_run.bat`) as alternative for Windows users

## Installation and Execution

### Using PowerShell (Recommended)
1. Double-click the `install_and_run.ps1` file, or
2. Open PowerShell as Administrator and run:
   ```powershell
   cd path\to\zio-booster
   .\install_and_run.ps1
   ```

### Using Batch File
1. Double-click the `install_and_run.bat` file, or
2. Open Command Prompt and run:
   ```cmd
   cd path\to\zio-booster
   install_and_run.bat
   ```

### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python src/main.py
   ```

## How to Use

### Basic Operation
1. **Start Boosting**: Click "Start Boosting" to begin automatic optimization
2. **Manual Optimization**: Click "Manual Optimize" for on-demand optimization
3. **Stop Boosting**: Click "Stop Boosting" to end optimization

### Advanced Features
1. **System Profiles**: Select a profile from the dropdown to apply predefined optimization settings
2. **Kill High CPU Processes**: Click "Kill High CPU" to terminate processes using excessive resources
3. **Export Logs**: Click "Export Log" to save your optimization history to a file
4. **Monitor Processes**: View real-time process information in the process list

### Process Information
The application displays:
- Process Name
- Process ID (PID)
- CPU Usage Percentage
- Memory Usage Percentage
- Resource Score (combined CPU and memory usage)

## Safety Features
- Confirmation dialogs before terminating processes
- Logging of all optimization actions
- Safe process termination with fallback to force kill if needed

## Requirements
- Python 3.8 or higher
- Windows OS (for PowerShell/Batch scripts)
- Administrator privileges recommended for full functionality

## Troubleshooting

### Common Issues
1. **Python not found**: Ensure Python is installed and added to PATH
2. **Permission errors**: Run as Administrator or with elevated privileges
3. **Missing dependencies**: The installation scripts will install all required packages

### Performance Issues
- If the application runs slowly, try using the "Battery Saver" profile
- High CPU usage during monitoring is normal when scanning all processes

## Files Included
- `install_and_run.ps1`: PowerShell installation and execution script
- `install_and_run.bat`: Windows batch installation and execution script
- `src/main.py`: Main application file with enhanced features
- `profiles.json`: System profiles configuration (auto-generated)