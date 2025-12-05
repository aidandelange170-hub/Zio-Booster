"""
Modern UI components for Zio-Booster
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk  # We'll use this for modern styling

class ModernZioBoosterUI:
    """A modern UI for the Zio-Booster application"""
    
    def __init__(self, root):
        self.root = root
        self.setup_modern_ui()
    
    def setup_modern_ui(self):
        """Setup the modern UI with customtkinter"""
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
        
        # Configure the main window
        self.root.title("Zio-Booster FPS Booster")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Zio-Booster FPS Booster", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))
        
        # Status frame
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Status: Idle", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=10)
        
        # System info frame
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", padx=20, pady=10)
        
        # Create info grid
        self.cpu_label = ctk.CTkLabel(self.info_frame, text="CPU Usage: 0%", font=ctk.CTkFont(size=12))
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.memory_label = ctk.CTkLabel(self.info_frame, text="Memory Usage: 0%", font=ctk.CTkFont(size=12))
        self.memory_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.temp_label = ctk.CTkLabel(self.info_frame, text="CPU Temp: N/A", font=ctk.CTkFont(size=12))
        self.temp_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        # Additional metrics
        self.optimization_count_label = ctk.CTkLabel(self.info_frame, text="Optimizations: 0", font=ctk.CTkFont(size=12))
        self.optimization_count_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.gaming_mode_label = ctk.CTkLabel(self.info_frame, text="Gaming Mode: Off", font=ctk.CTkFont(size=12))
        self.gaming_mode_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Control buttons frame
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=20, pady=10)
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="Start Boosting",
            command=self.start_boosting_callback,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_button.pack(side="left", padx=5, pady=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="Stop Boosting",
            command=self.stop_boosting_callback,
            fg_color="#f44336",
            hover_color="#D32F2F",
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5, pady=10)
        
        # Manual optimize button
        self.manual_optimize_button = ctk.CTkButton(
            self.control_frame,
            text="Manual Optimize",
            command=self.manual_optimize_callback,
            fg_color="#2196F3",
            hover_color="#1976D2",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.manual_optimize_button.pack(side="left", padx=5, pady=10)
        
        # Gaming Mode button
        self.gaming_mode_button = ctk.CTkButton(
            self.control_frame,
            text="Enable Gaming Mode",
            command=self.gaming_mode_callback,
            fg_color="#FF9800",
            hover_color="#F57C00",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.gaming_mode_button.pack(side="left", padx=5, pady=10)
        
        # Profile selection frame
        self.profile_frame = ctk.CTkFrame(self.main_frame)
        self.profile_frame.pack(fill="x", padx=20, pady=10)
        
        # Profile selection
        profile_label = ctk.CTkLabel(self.profile_frame, text="Game Profile:", font=ctk.CTkFont(size=12, weight="bold"))
        profile_label.pack(side="left", padx=10, pady=10)
        
        self.profile_var = ctk.StringVar(value="Default")
        self.profile_dropdown = ctk.CTkComboBox(
            self.profile_frame,
            values=["Default", "Cyberpunk 2077", "Fortnite", "CS:GO", "Valorant"],
            variable=self.profile_var,
            width=150
        )
        self.profile_dropdown.pack(side="left", padx=10, pady=10)
        
        self.apply_profile_button = ctk.CTkButton(
            self.profile_frame,
            text="Apply Profile",
            command=self.apply_profile_callback,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            font=ctk.CTkFont(size=12)
        )
        self.apply_profile_button.pack(side="left", padx=10, pady=10)
        
        # Process list frame
        self.process_frame = ctk.CTkFrame(self.main_frame)
        self.process_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Process list title
        process_title = ctk.CTkLabel(
            self.process_frame,
            text="High Temperature Processes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        process_title.pack(pady=(10, 5))
        
        # Create treeview for processes using standard tkinter (since customtkinter doesn't have a treeview)
        tree_frame = ctk.CTkFrame(self.process_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Name", "PID", "CPU %", "Memory %", "Temp Score")
        self.process_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.process_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def start_boosting_callback(self):
        """Callback for start boosting button"""
        pass  # This will be implemented by the main app
    
    def stop_boosting_callback(self):
        """Callback for stop boosting button"""
        pass  # This will be implemented by the main app
    
    def manual_optimize_callback(self):
        """Callback for manual optimize button"""
        pass  # This will be implemented by the main app
    
    def gaming_mode_callback(self):
        """Callback for gaming mode button"""
        pass  # This will be implemented by the main app
    
    def apply_profile_callback(self):
        """Callback for apply profile button"""
        pass  # This will be implemented by the main app