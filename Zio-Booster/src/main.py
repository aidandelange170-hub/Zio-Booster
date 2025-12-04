
import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
import sys
import os

# Add the project root to the path so we can import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.temperature_monitor import TemperatureMonitor
from utils.optimizer import SystemOptimizer

class ZioBoosterApp:
    def __init__(self):
        # Initialize temperature monitor and optimizer
        self.temp_monitor = TemperatureMonitor()
        self.optimizer = SystemOptimizer()
        
        # FPS optimization variables
        self.is_running = False
        self.monitoring_thread = None
        
        # Initialize UI (using basic tkinter for now to avoid dependency issues)
        self.root = tk.Tk()
        self.root.title("Zio-Booster FPS Booster")
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
        result = self.optimizer.run_optimization_cycle()
        self.status_label.config(text="Status: Manual Optimization Complete", fg="green")
        print(f"Manual optimization result: {result}")
        
        # Update process list after optimization
        self.update_process_list()
        
        # Reset status after a few seconds
        self.root.after(3000, lambda: self.status_label.config(text="Status: Idle", fg="black") if not self.is_running else None)
    
    def monitor_system(self):
        """Monitor system and optimize in the background"""
        while self.is_running:
            # Update process list
            self.update_process_list()
            # Run optimization cycle periodically
            if self.is_running:  # Check again in case it was stopped during process update
                self.optimizer.run_optimization_cycle()
            time.sleep(5)  # Update every 5 seconds

    def update_system_info(self):
        """Update system information labels"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        self.cpu_label.config(text=f"{cpu_percent}%")
        self.memory_label.config(text=f"{memory_percent}%")
        
        # Update temperature
        cpu_temp = self.temp_monitor.get_cpu_temperature()
        if cpu_temp is not None:
            self.temp_label.config(text=f"{cpu_temp:.1f}°C")
        else:
            self.temp_label.config(text="N/A")
        
        # Schedule next update
        self.root.after(2000, self.update_system_info)

    def update_process_list(self):
        """Update the list of processes, highlighting high-temperature ones"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Get all processes using our temperature monitor
        processes = self.temp_monitor.get_process_temperatures()
        
        # Add top processes to the treeview
        for i, proc in enumerate(processes[:20]):  # Show top 20 processes
            self.process_tree.insert("", "end", values=(
                proc['name'],
                proc['pid'],
                f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else "0.0",
                f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else "0.0",
                f"{proc['temperature_score']:.1f}"
            ))
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ZioBoosterApp()
    app.run()
