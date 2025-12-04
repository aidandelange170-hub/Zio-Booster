# Zio-Booster FPS Booster - Features

## Overview
Zio-Booster is a modern FPS booster application that optimizes your system in the background to increase frame rates and reduce temperature by terminating high-temperature applications.

## Core Features

### 1. Temperature Monitoring
- Monitors CPU temperature when available on supported systems
- Calculates temperature scores for processes based on CPU and memory usage
- Identifies high-temperature processes that may impact performance

### 2. System Optimization
- Terminates high-temperature applications that may be affecting performance
- Cleans memory by terminating unnecessary processes
- Optimizes network settings for lower latency (placeholder)
- Sets high priority for game processes

### 3. Real-time Monitoring
- Continuous monitoring of system resources (CPU, memory, temperature)
- Real-time process list with temperature scores
- Automatic optimization cycles while active

### 4. Modern UI
- Clean, intuitive interface with status indicators
- Real-time system information display
- Process management with detailed metrics
- Responsive controls for start/stop/manual optimization

### 5. Process Management
- Displays top processes sorted by temperature scores
- Shows detailed information: Name, PID, CPU%, Memory%, Temp Score
- Safeguards critical system processes from termination
- Manual optimization button for on-demand optimization

## How It Works

### Background Optimization
1. The application runs optimization cycles every 5 seconds when active
2. Identifies processes with high temperature scores (based on resource usage)
3. Terminates non-critical high-temperature processes
4. Cleans memory by removing unnecessary processes
5. Monitors system temperature and adjusts optimization accordingly

### Temperature Scoring
The application uses a simulated temperature score based on:
- CPU usage percentage (higher usage = higher temperature)
- Memory usage (higher usage contributes to temperature score)
- Critical system processes are protected from termination

## Usage

### Starting the Application
1. Run `python start-application.py`
2. The application will install dependencies if needed
3. The main UI will appear with system information

### Controls
- **Start Boosting**: Begin automatic optimization
- **Stop Boosting**: End automatic optimization
- **Manual Optimize**: Run a single optimization cycle

## Architecture

### Project Structure
```
Zio-Booster/
├── README.md              # Project overview
├── FEATURES.md            # This file
├── requirements.txt       # Python dependencies
├── setup.py              # Installation script
├── start-application.py   # Main application launcher
├── src/
│   ├── main.py           # Basic tkinter UI application
│   └── modern_main.py    # CustomTkinter UI application
├── ui/
│   └── modern_ui.py      # Modern UI components
└── utils/
    ├── temperature_monitor.py  # Temperature monitoring utilities
    └── optimizer.py            # System optimization utilities
```

### Key Components
- **Temperature Monitor**: Handles temperature detection and process scoring
- **System Optimizer**: Performs optimization operations
- **UI Components**: Modern interface with real-time updates
- **Process Management**: Safely handles process termination

## Requirements
- Python 3.7+
- psutil library
- tkinter (for basic UI)
- customtkinter (for modern UI, optional)

## Installation
1. Clone the repository
2. Run `start-application.py` to install dependencies and start the application
3. The application will automatically detect available UI libraries and use the best available option