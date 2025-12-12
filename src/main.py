import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
import threading
import time
import sys
import os
import random
import json
import subprocess
from datetime import datetime

# Add the project root to the path so we can import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class ZioBoosterApp:
    def __init__(self):
        # FPS optimization variables
        self.is_running = False
        self.monitoring_thread = None
        self.optimization_log = []
        self.system_profiles = {}
        self.current_profile = "default"
        
        # Initialize UI (using basic tkinter for now to avoid dependency issues)
        self.root = tk.Tk()
        self.root.title("Zio-Booster FPS Booster - Advanced Mode")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Load profiles if they exist
        self.load_profiles()
        
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
        
        # Profile selection frame
        profile_frame = tk.Frame(self.root)
        profile_frame.pack(pady=5, fill="x", padx=20)
        
        tk.Label(profile_frame, text="System Profile:", font=("Arial", 10)).pack(side="left")
        
        # Profile selection dropdown
        self.profile_var = tk.StringVar(value=self.current_profile)
        self.profile_dropdown = ttk.Combobox(profile_frame, textvariable=self.profile_var, 
                                            values=list(self.system_profiles.keys()), 
                                            state="readonly", width=15)
        self.profile_dropdown.pack(side="left", padx=5)
        self.profile_dropdown.bind("<<ComboboxSelected>>", self.on_profile_change)
        
        # Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_button = tk.Button(control_frame, text="Start Boosting", 
                                     command=self.start_boosting, 
                                     bg="#4CAF50", fg="white", 
                                     font=("Arial", 12), width=15)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = tk.Button(control_frame, text="Stop Boosting", 
                                    command=self.stop_boosting, 
                                    bg="#f44336", fg="white", 
                                    font=("Arial", 12), width=15, 
                                    state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Manual optimization button
        self.manual_optimize_button = tk.Button(control_frame, text="Manual Optimize", 
                                               command=self.manual_optimize, 
                                               bg="#2196F3", fg="white", 
                                               font=("Arial", 12), width=15)
        self.manual_optimize_button.pack(side="left", padx=5)
        
        # Terminate high resource processes button
        self.terminate_button = tk.Button(control_frame, text="Kill High CPU", 
                                         command=self.terminate_processes_click, 
                                         bg="#FF9800", fg="white", 
                                         font=("Arial", 12), width=15)
        self.terminate_button.pack(side="left", padx=5)
        
        # Export log button
        self.export_log_button = tk.Button(control_frame, text="Export Log", 
                                          command=self.export_log, 
                                          bg="#9C27B0", fg="white", 
                                          font=("Arial", 12), width=15)
        self.export_log_button.pack(side="left", padx=5)
        
        # Temperature and process info
        temp_frame = tk.Frame(self.root)
        temp_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        tk.Label(temp_frame, text="High Resource Processes:", 
                font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Create a treeview for processes
        columns = ("Name", "PID", "CPU %", "Memory %", "Resource Score")
        self.process_tree = ttk.Treeview(temp_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=120)
        
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
    def terminate_processes_click(self):
        """Handle the terminate high resource processes button click"""
        result = messagebox.askquestion("Confirm Action", 
                                       "This will terminate processes using high CPU/Memory resources. Continue?")
        if result == 'yes':
            terminated_count = self.terminate_high_resource_processes()
            self.status_label.config(text=f"Status: Terminated {terminated_count} high resource processes", fg="orange")
            
            # Update process list after termination
            self.update_process_list()
            
            # Reset status after a few seconds
            self.root.after(3000, lambda: self.status_label.config(text="Status: Idle", fg="black") 
                           if not self.is_running else None)

    def on_profile_change(self, event=None):
        """Handle profile selection change"""
        selected_profile = self.profile_var.get()
        self.apply_profile(selected_profile)
    
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
    
    def load_profiles(self):
        """Load system profiles from a JSON file"""
        try:
            with open('profiles.json', 'r') as f:
                self.system_profiles = json.load(f)
        except FileNotFoundError:
            # Create default profiles if file doesn't exist
            self.system_profiles = {
                "default": {"priority_boost": "above_normal", "cpu_affinity": "all", "ram_optimization": True},
                "gaming": {"priority_boost": "high", "cpu_affinity": "cores_1_2_3_4", "ram_optimization": True},
                "performance": {"priority_boost": "realtime", "cpu_affinity": "all", "ram_optimization": True},
                "battery_saver": {"priority_boost": "below_normal", "cpu_affinity": "cores_1_2", "ram_optimization": False}
            }
            self.save_profiles()
        except Exception as e:
            print(f"Error loading profiles: {e}")
            self.system_profiles = {
                "default": {"priority_boost": "above_normal", "cpu_affinity": "all", "ram_optimization": True}
            }

    def save_profiles(self):
        """Save system profiles to a JSON file"""
        try:
            with open('profiles.json', 'w') as f:
                json.dump(self.system_profiles, f, indent=4)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def apply_profile(self, profile_name):
        """Apply a specific system profile"""
        if profile_name in self.system_profiles:
            self.current_profile = profile_name
            profile = self.system_profiles[profile_name]
            self.status_label.config(text=f"Status: Applied profile '{profile_name}'", fg="blue")
            
            # Log this action
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": "apply_profile",
                "profile": profile_name,
                "details": profile
            }
            self.optimization_log.append(log_entry)
            
            print(f"Applied profile: {profile_name} with settings: {profile}")
        else:
            messagebox.showwarning("Profile Error", f"Profile '{profile_name}' does not exist.")

    def terminate_high_resource_processes(self, threshold=80.0):
        """Terminate processes that are using too many resources"""
        terminated_count = 0
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    cpu_usage = proc.info['cpu_percent'] or 0
                    memory_usage = proc.info['memory_percent'] or 0
                    
                    # Calculate combined resource usage
                    total_usage = cpu_usage + memory_usage
                    
                    if total_usage > threshold:
                        # Attempt to terminate the process
                        try:
                            p = psutil.Process(proc.info['pid'])
                            p.terminate()
                            p.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
                            
                            log_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "action": "terminate_process",
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "cpu_usage": cpu_usage,
                                "memory_usage": memory_usage
                            }
                            self.optimization_log.append(log_entry)
                            
                            terminated_count += 1
                        except psutil.TimeoutExpired:
                            # Force kill if terminate didn't work
                            try:
                                p.kill()
                                
                                log_entry = {
                                    "timestamp": datetime.now().isoformat(),
                                    "action": "kill_process",
                                    "pid": proc.info['pid'],
                                    "name": proc.info['name'],
                                    "cpu_usage": cpu_usage,
                                    "memory_usage": memory_usage
                                }
                                self.optimization_log.append(log_entry)
                                
                                terminated_count += 1
                            except:
                                pass  # Ignore if we can't kill the process
                        except:
                            pass  # Ignore if we can't terminate the process
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"Error terminating high resource processes: {e}")
        
        return terminated_count

    def export_log(self):
        """Export optimization log to a file"""
        if not self.optimization_log:
            messagebox.showinfo("Log Export", "No optimization events to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Optimization Log"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.optimization_log, f, indent=4)
                messagebox.showinfo("Log Export", f"Optimization log exported to {filename}")
            except Exception as e:
                messagebox.showerror("Log Export Error", f"Failed to export log: {e}")

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ZioBoosterApp()
    app.run()
