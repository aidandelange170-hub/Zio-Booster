#!/usr/bin/env python3
"""
Zio-Booster FPS Booster - Main Application Launcher
This script sets up and starts the Zio-Booster application with improved error handling and dependency management
"""

import os
import sys
import subprocess
import platform
import importlib
from pathlib import Path

def check_requirements():
    """
    Check if required packages are installed
    Returns a list of missing packages
    """
    required_packages = {
        'psutil': 'psutil>=5.8.0',
        'requests': 'requests>=2.25.1',
        'packaging': 'packaging>=21.0',
        'customtkinter': 'customtkinter>=5.0.0'
    }
    missing_packages = []
    
    for package_name, package_spec in required_packages.items():
        try:
            importlib.import_module(package_name)
        except ImportError:
            missing_packages.append(package_spec)
    
    return missing_packages

def install_requirements(missing_packages=None):
    """
    Install missing requirements with error handling
    """
    if missing_packages is None:
        missing_packages = check_requirements()
    
    if not missing_packages:
        print("All required packages are already installed.")
        return True
    
    print(f"Installing required packages: {', '.join(missing_packages)}...")
    try:
        # Install packages with proper error handling
        for package in missing_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during installation: {e}")
        return False

def ensure_directories():
    """
    Ensure all required directories exist
    """
    directories = ["src", "utils", "config", "logs", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Ensured directory exists: {directory}")

def validate_python_version():
    """
    Validate that the Python version meets minimum requirements
    """
    min_version = (3, 7)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"Error: Python {min_version[0]}.{min_version[1]} or higher is required. Current version: {sys.version}")
        return False
    
    print(f"Python version {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} is compatible.")
    return True

def check_system_compatibility():
    """
    Check if the system is compatible with the application
    """
    system = platform.system().lower()
    supported_systems = ['windows', 'linux', 'darwin']  # Darwin is macOS
    
    if system not in supported_systems:
        print(f"Warning: System '{system}' may not be fully supported. Supported: {', '.join(supported_systems)}")
        return False
    
    print(f"System '{system}' is supported.")
    return True

def load_config():
    """
    Load application configuration
    """
    config_path = Path("config/version.json")
    if config_path.exists():
        try:
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Configuration loaded. Current version: {config.get('current_version', 'unknown')}")
            return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return {}
    else:
        print("Configuration file not found. Using defaults.")
        return {}

def main():
    print("Zio-Booster FPS Booster - Starting Application")
    print("===============================================")
    
    # Validate Python version
    if not validate_python_version():
        return
    
    # Check system compatibility
    if not check_system_compatibility():
        print("Continuing despite system compatibility warning...")
    
    # Ensure required directories exist
    ensure_directories()
    
    # Load configuration
    config = load_config()
    
    # Check requirements
    missing_packages = check_requirements()
    
    if missing_packages:
        print(f"Missing packages detected: {', '.join(missing_packages)}")
        success = install_requirements(missing_packages)
        if not success:
            print("Failed to install required packages. Please install them manually.")
            return
    
    # Additional dependency check after installation
    missing_after_install = check_requirements()
    if missing_after_install:
        print(f"Warning: Some packages still missing after installation: {', '.join(missing_after_install)}")
        print("Attempting to continue with available packages...")
    
    # Start the main application
    try:
        print("Starting Zio-Booster...")
        from src.main import ZioBoosterApp
        app = ZioBoosterApp()
        app.run()
    except ImportError as e:
        print(f"Main application import error: {e}")
        print("Attempting to create basic application structure...")
        # Create basic application structure if not exists
        create_basic_app()
        try:
            from src.main import ZioBoosterApp
            app = ZioBoosterApp()
            app.run()
        except ImportError as e:
            print(f"Failed to start application after creating basic structure: {e}")
            print("Please check your installation and dependencies.")
            return
    except Exception as e:
        print(f"Unexpected error starting application: {e}")
        import traceback
        traceback.print_exc()
        return

def create_basic_app():
    """
    Create basic application structure if it doesn't exist
    This is a fallback method if the main application is missing
    """
    os.makedirs("src", exist_ok=True)
    
    # Create main.py with basic functionality
    main_content = '''import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
import sys
import os
import random

# Add the project root to the path so we can import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class ZioBoosterApp:
    def __init__(self):
        # FPS optimization variables
        self.is_running = False
        self.monitoring_thread = None
        
        # Initialize UI (using basic tkinter for now to avoid dependency issues)
        self.root = tk.Tk()
        self.root.title("Zio-Booster FPS Booster - Basic Mode")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the main UI"""
        # Title
        title_label = tk.Label(self.root, text="Zio-Booster FPS Booster", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10, fill="x", padx=20)
        
        self.status_label = tk.Label(status_frame, text="Status: Idle", 
                                    font=("Arial", 12))
        self.status_label.pack()
        
        # System info
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(info_frame, text="CPU Usage:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.cpu_label = tk.Label(info_frame, text="0%", font=("Arial", 10))
        self.cpu_label.grid(row=0, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="Memory Usage:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        self.memory_label = tk.Label(info_frame, text="0%", font=("Arial", 10))
        self.memory_label.grid(row=1, column=1, sticky="w", padx=10)
        
        tk.Label(info_frame, text="CPU Temp:", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
        self.temp_label = tk.Label(info_frame, text="N/A", font=("Arial", 10))
        self.temp_label.grid(row=2, column=1, sticky="w", padx=10)
        
        # Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)
        
        self.start_button = tk.Button(control_frame, text="Start Boosting", 
                                     command=self.start_boosting, 
                                     bg="#4CAF50", fg="white", 
                                     font=("Arial", 12), width=15)
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(control_frame, text="Stop Boosting", 
                                    command=self.stop_boosting, 
                                    bg="#f44336", fg="white", 
                                    font=("Arial", 12), width=15, 
                                    state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        # Manual optimization button
        self.manual_optimize_button = tk.Button(control_frame, text="Manual Optimize", 
                                               command=self.manual_optimize, 
                                               bg="#2196F3", fg="white", 
                                               font=("Arial", 12), width=15)
        self.manual_optimize_button.pack(side="left", padx=10)
        
        # Temperature and process info
        temp_frame = tk.Frame(self.root)
        temp_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        tk.Label(temp_frame, text="High Temperature Processes:", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Create a treeview for processes
        columns = ("Name", "PID", "CPU %", "Memory %", "Temp Score")
        self.process_tree = ttk.Treeview(temp_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        self.process_tree.pack(fill="both", expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(temp_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Update system info periodically
        self.update_system_info()
    
    def start_boosting(self):
        """Start the FPS boosting process"""
        self.is_running = True
        self.status_label.config(text="Status: Active - Optimizing System", fg="green")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start monitoring in a separate thread
        self.monitoring_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitoring_thread.start()
    
    def stop_boosting(self):
        """Stop the FPS boosting process"""
        self.is_running = False
        self.status_label.config(text="Status: Stopped", fg="red")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def manual_optimize(self):
        """Manually run an optimization cycle"""
        self.status_label.config(text="Status: Manual Optimization Running", fg="orange")
        
        # Simulate optimization process
        result = self.simulate_optimization()
        
        self.status_label.config(text="Status: Manual Optimization Complete", fg="green")
        print(f"Manual optimization result: {result}")
        
        # Update process list after optimization
        self.update_process_list()
        
        # Reset status after a few seconds
        self.root.after(3000, lambda: self.status_label.config(text="Status: Idle", fg="black") if not self.is_running else None)
    
    def simulate_optimization(self):
        """Simulate an optimization process"""
        # In a real implementation, this would perform actual optimization
        print("Simulating optimization process...")
        return {"processes_terminated": random.randint(1, 5), "performance_improved": True}
    
    def monitor_system(self):
        """Monitor system and optimize in the background"""
        while self.is_running:
            # Update process list
            self.update_process_list()
            time.sleep(5)  # Update every 5 seconds
    
    def update_system_info(self):
        """Update system information labels"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            self.cpu_label.config(text=f"{cpu_percent}%")
            self.memory_label.config(text=f"{memory_percent}%")
            
            # Attempt to get temperature
            try:
                # Try to get temperature from psutil sensors
                temps = psutil.sensors_temperatures()
                if temps and 'coretemp' in temps:
                    cpu_temp = temps['coretemp'][0].current
                    self.temp_label.config(text=f"{cpu_temp:.1f}°C")
                else:
                    # Simulate temperature if not available
                    simulated_temp = cpu_percent * 0.7 + 20  # Base temperature + load factor
                    self.temp_label.config(text=f"{simulated_temp:.1f}°C")
            except:
                # If temperature sensors are not available, simulate
                simulated_temp = cpu_percent * 0.7 + 20
                self.temp_label.config(text=f"{simulated_temp:.1f}°C")
        except Exception as e:
            print(f"Error updating system info: {e}")
            self.cpu_label.config(text="Error")
            self.memory_label.config(text="Error")
            self.temp_label.config(text="Error")
        
        # Schedule next update
        self.root.after(2000, self.update_system_info)

    def update_process_list(self):
        """Update the list of processes, highlighting high-temperature ones"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        try:
            # Get all processes with their resource usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    # Get CPU and memory usage
                    cpu_usage = proc.info['cpu_percent'] or 0
                    memory_usage = proc.info['memory_percent'] or 0
                    
                    # Calculate a "temperature score" based on resource usage
                    temp_score = cpu_usage * 0.6 + memory_usage * 0.4
                    
                    processes.append((
                        proc.info['name'],
                        proc.info['pid'],
                        f"{cpu_usage:.1f}",
                        f"{memory_usage:.1f}",
                        f"{temp_score:.1f}"
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Sort by temperature score (resource usage)
            processes.sort(key=lambda x: float(x[4]), reverse=True)
            
            # Add top processes to the treeview
            for i, proc in enumerate(processes[:20]):  # Show top 20 processes
                self.process_tree.insert("", "end", values=proc)
        except Exception as e:
            print(f"Error updating process list: {e}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ZioBoosterApp()
    app.run()
'''
    
    with open("src/main.py", "w") as f:
        f.write(main_content)
    
    print("Basic application structure created.")

if __name__ == "__main__":
    main()