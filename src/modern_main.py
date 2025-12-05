"""
Modern Zio-Booster FPS Booster with CustomTkinter UI
"""

import threading
import time
import sys
import os

# Add the project root to the path so we can import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import customtkinter as ctk
    from ui.modern_ui import ModernZioBoosterUI
    CUSTOM_TK_AVAILABLE = True
except ImportError:
    CUSTOM_TK_AVAILABLE = False
    import tkinter as tk
    from tkinter import ttk

from utils.temperature_monitor import TemperatureMonitor
from utils.optimizer import SystemOptimizer
from utils.performance_metrics import PerformanceMetrics

class ZioBoosterApp:
    def __init__(self):
        # Initialize temperature monitor and optimizer
        self.temp_monitor = TemperatureMonitor()
        self.optimizer = SystemOptimizer()
        self.performance_metrics = PerformanceMetrics()
        
        # FPS optimization variables
        self.is_running = False
        self.monitoring_thread = None
        self.gaming_mode_active = False
        
        if CUSTOM_TK_AVAILABLE:
            # Use modern UI
            self.root = ctk.CTk()
            self.ui = ModernZioBoosterUI(self.root)
            
            # Connect UI callbacks to app methods
            self.ui.start_boosting_callback = self.start_boosting
            self.ui.stop_boosting_callback = self.stop_boosting
            self.ui.manual_optimize_callback = self.manual_optimize
            self.ui.gaming_mode_callback = self.toggle_gaming_mode
            self.ui.apply_profile_callback = self.apply_profile
        else:
            # Fallback to basic tkinter UI
            self.root = tk.Tk()
            self.root.title("Zio-Booster FPS Booster")
            self.root.geometry("700x600")
            self.root.resizable(True, True)
            
            # Create UI elements
            self.create_basic_ui()
        
        # Update system info periodically
        self.update_system_info()
    
    def create_basic_ui(self):
        """Create basic UI when customtkinter is not available"""
        import tkinter as tk
        from tkinter import ttk
        
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
    
    def start_boosting(self):
        """Start the FPS boosting process"""
        self.is_running = True
        
        if CUSTOM_TK_AVAILABLE:
            self.ui.status_label.configure(text="Status: Active - Optimizing System")
            self.ui.start_button.configure(state="disabled")
            self.ui.stop_button.configure(state="normal")
        else:
            self.status_label.config(text="Status: Active - Optimizing System", fg="green")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
        
        # Start monitoring in a separate thread
        self.monitoring_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitoring_thread.start()

    def stop_boosting(self):
        """Stop the FPS boosting process"""
        self.is_running = False
        
        if CUSTOM_TK_AVAILABLE:
            self.ui.status_label.configure(text="Status: Stopped")
            self.ui.start_button.configure(state="normal")
            self.ui.stop_button.configure(state="disabled")
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def manual_optimize(self):
        """Manually run an optimization cycle"""
        if CUSTOM_TK_AVAILABLE:
            self.ui.status_label.configure(text="Status: Manual Optimization Running")
        else:
            self.status_label.config(text="Status: Manual Optimization Running", fg="orange")
        
        result = self.optimizer.run_optimization_cycle()
        
        if CUSTOM_TK_AVAILABLE:
            self.ui.status_label.configure(text="Status: Manual Optimization Complete")
        else:
            self.status_label.config(text="Status: Manual Optimization Complete", fg="green")
        
        print(f"Manual optimization result: {result}")
        
        # Update process list after optimization
        self.update_process_list()
        
        # Reset status after a few seconds if not running
        def reset_status():
            if not self.is_running:
                if CUSTOM_TK_AVAILABLE:
                    self.ui.status_label.configure(text="Status: Idle")
                else:
                    self.status_label.config(text="Status: Idle", fg="black")
        
        self.root.after(3000, reset_status)
    
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
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        if CUSTOM_TK_AVAILABLE:
            self.ui.cpu_label.configure(text=f"CPU Usage: {cpu_percent}%")
            self.ui.memory_label.configure(text=f"Memory Usage: {memory_percent}%")
        else:
            self.cpu_label.config(text=f"{cpu_percent}%")
            self.memory_label.config(text=f"{memory_percent}%")
        
        # Update temperature
        cpu_temp = self.temp_monitor.get_cpu_temperature()
        if cpu_temp is not None:
            if CUSTOM_TK_AVAILABLE:
                self.ui.temp_label.configure(text=f"CPU Temp: {cpu_temp:.1f}°C")
            else:
                self.temp_label.config(text=f"{cpu_temp:.1f}°C")
        else:
            if CUSTOM_TK_AVAILABLE:
                self.ui.temp_label.configure(text="CPU Temp: N/A")
            else:
                self.temp_label.config(text="N/A")
        
        # Schedule next update
        self.root.after(2000, self.update_system_info)
    
    def toggle_gaming_mode(self):
        """Toggle gaming mode on/off"""
        if self.gaming_mode_active:
            # Disable gaming mode
            self.optimizer.disable_gaming_mode()
            self.gaming_mode_active = False
            if CUSTOM_TK_AVAILABLE:
                self.ui.gaming_mode_label.configure(text="Gaming Mode: Off")
                self.ui.gaming_mode_button.configure(text="Enable Gaming Mode", fg_color="#FF9800")
            else:
                # For basic UI, we would need to implement this
                pass
            print("Gaming mode disabled")
        else:
            # Enable gaming mode
            self.optimizer.enable_gaming_mode()
            self.gaming_mode_active = True
            if CUSTOM_TK_AVAILABLE:
                self.ui.gaming_mode_label.configure(text="Gaming Mode: Active")
                self.ui.gaming_mode_button.configure(text="Disable Gaming Mode", fg_color="#795548")
            else:
                # For basic UI, we would need to implement this
                pass
            print("Gaming mode enabled")
    
    def apply_profile(self):
        """Apply selected game profile"""
        if CUSTOM_TK_AVAILABLE:
            profile_name = self.ui.profile_var.get()
            if profile_name and profile_name != "Default":
                success = self.optimizer.apply_profile(profile_name)
                if success:
                    print(f"Applied profile: {profile_name}")
                    # Update status to indicate profile is active
                    if self.is_running:
                        if CUSTOM_TK_AVAILABLE:
                            self.ui.status_label.configure(text=f"Status: Active - Profile: {profile_name}")
                    else:
                        if CUSTOM_TK_AVAILABLE:
                            self.ui.status_label.configure(text=f"Status: Profile Applied - {profile_name}")
                else:
                    print(f"Failed to apply profile: {profile_name}")
            else:
                print("No profile selected")
        else:
            print("Profile selection not available in basic UI")

    def update_process_list(self):
        """Update the list of processes, highlighting high-temperature ones"""
        # Get all processes using our temperature monitor
        processes = self.temp_monitor.get_process_temperatures()
        
        if CUSTOM_TK_AVAILABLE:
            # For customtkinter, we use the standard tkinter treeview
            tree = self.ui.process_tree
        else:
            tree = self.process_tree
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Add top processes to the treeview
        for i, proc in enumerate(processes[:20]):  # Show top 20 processes
            tree.insert("", "end", values=(
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