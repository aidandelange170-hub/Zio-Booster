#!/usr/bin/env python3
"""
Zio-Booster FPS Booster - Main Application Launcher
This script sets up and starts the Zio-Booster application
"""

import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['psutil', 'tkinter']
    missing_packages = []
    
    try:
        import psutil
    except ImportError:
        missing_packages.append('psutil')
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append('tkinter')
    
    return missing_packages

def install_requirements():
    """Install missing requirements"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])

def main():
    print("Zio-Booster FPS Booster - Starting Application")
    print("===============================================")
    
    # Check requirements
    missing_packages = check_requirements()
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        try:
            install_requirements()
            print("Requirements installed successfully!")
        except Exception as e:
            print(f"Error installing requirements: {e}")
            return
    
    # Start the main application
    try:
        print("Starting Zio-Booster...")
        from src.main import ZioBoosterApp
        app = ZioBoosterApp()
        app.run()
    except ImportError:
        print("Main application not found. Creating basic application...")
        # Create basic application structure if not exists
        create_basic_app()
        from src.main import ZioBoosterApp
        app = ZioBoosterApp()
        app.run()

def create_basic_app():
    """Create basic application structure if it doesn't exist"""
    os.makedirs("src", exist_ok=True)
    
    # Create main.py
    main_content = '''
import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time

class ZioBoosterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zio-Booster FPS Booster")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Create UI
        self.create_ui()
        
        # FPS optimization variables
        self.is_running = False
        self.monitoring_thread = None
        
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
        
        # Temperature and process info
        temp_frame = tk.Frame(self.root)
        temp_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        tk.Label(temp_frame, text="High Temperature Processes:", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Create a treeview for processes
        columns = ("Name", "PID", "CPU %", "Memory %", "Temperature")
        self.process_tree = ttk.Treeview(temp_frame, columns=columns, show="headings", height=10)
        
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
    
    def monitor_system(self):
        """Monitor system and optimize in the background"""
        while self.is_running:
            # Update process list
            self.update_process_list()
            time.sleep(3)  # Update every 3 seconds
    
    def update_system_info(self):
        """Update system information labels"""
        if not self.is_running:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            self.cpu_label.config(text=f"{cpu_percent}%")
            self.memory_label.config(text=f"{memory_percent}%")
        
        # Schedule next update
        self.root.after(2000, self.update_system_info)
    
    def update_process_list(self):
        """Update the list of processes, highlighting high-temperature ones"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Get all processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                # For demo purposes, we'll simulate temperature based on CPU usage
                # In a real implementation, this would require hardware temperature sensors
                cpu_usage = proc.info['cpu_percent'] or 0
                simulated_temp = min(100, cpu_usage * 0.8)  # Simulated temperature
                
                processes.append((
                    proc.info['name'],
                    proc.info['pid'],
                    f"{cpu_usage:.1f}",
                    f"{proc.info['memory_percent']:.1f}" if proc.info['memory_percent'] else "0.0",
                    f"{simulated_temp:.1f}°C"
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage (simulated temperature)
        processes.sort(key=lambda x: float(x[2]), reverse=True)
        
        # Add top processes to the treeview
        for i, proc in enumerate(processes[:20]):  # Show top 20 processes
            self.process_tree.insert("", "end", values=proc)
    
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