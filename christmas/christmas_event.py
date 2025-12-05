"""
Christmas Event Module for Zio-Booster FPS Booster
This module adds Christmas-themed features to the application
"""

import datetime
import random
import os
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk


class ChristmasEvent:
    """
    Manages the Christmas event features for Zio-Booster
    """
    
    def __init__(self):
        self.is_christmas_season = self._is_christmas_season()
        self.christmas_themes = self._load_christmas_themes()
        self.active_theme = None
        self.snowflakes = []
        self.christmas_decorations = []
        
    def _is_christmas_season(self) -> bool:
        """
        Check if we're currently in the Christmas season (December 1 - January 5)
        """
        now = datetime.datetime.now()
        month = now.month
        day = now.day
        
        # Christmas season is from December 1 to January 5
        if month == 12 and day >= 1:
            return True
        elif month == 1 and day <= 5:
            return True
        return False
    
    def _load_christmas_themes(self) -> Dict:
        """
        Load available Christmas themes
        """
        return {
            "classic": {
                "name": "Classic Christmas",
                "colors": {
                    "background": "#0a3d1f",  # Dark green
                    "foreground": "#ffffff",  # White
                    "accent": "#c62828",      # Christmas red
                    "highlight": "#fdd835"    # Gold
                },
                "snow_enabled": True,
                "icons": "christmas"
            },
            "frosty": {
                "name": "Frosty Winter",
                "colors": {
                    "background": "#1a237e",  # Deep blue
                    "foreground": "#ffffff",  # White
                    "accent": "#4fc3f7",      # Light blue
                    "highlight": "#e1f5fe"    # Very light blue
                },
                "snow_enabled": True,
                "icons": "winter"
            },
            "cozy": {
                "name": "Cozy Fireplace",
                "colors": {
                    "background": "#4e342e",  # Brown
                    "foreground": "#ffffff",  # White
                    "accent": "#ff8f00",      # Orange
                    "highlight": "#ffecb3"    # Light yellow
                },
                "snow_enabled": False,
                "icons": "cozy"
            }
        }
    
    def activate_christmas_mode(self) -> bool:
        """
        Activate Christmas mode if it's Christmas season
        """
        if not self.is_christmas_season:
            return False
            
        # Randomly select a theme if none is active
        if self.active_theme is None:
            theme_names = list(self.christmas_themes.keys())
            self.active_theme = random.choice(theme_names)
        
        return True
    
    def get_active_theme(self) -> Dict:
        """
        Get the currently active Christmas theme
        """
        if self.active_theme and self.active_theme in self.christmas_themes:
            return self.christmas_themes[self.active_theme]
        return None
    
    def apply_theme_to_window(self, window: tk.Tk) -> None:
        """
        Apply the current Christmas theme to a tkinter window
        """
        if not self.active_theme:
            return
            
        theme = self.get_active_theme()
        if theme:
            # Apply background color to the window
            window.configure(bg=theme['colors']['background'])
            
            # Set up styles for ttk widgets
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configure styles for various widgets
            style.configure('TFrame', background=theme['colors']['background'])
            style.configure('TLabel', 
                           background=theme['colors']['background'],
                           foreground=theme['colors']['foreground'])
            style.configure('TButton', 
                           background=theme['colors']['accent'],
                           foreground=theme['colors']['foreground'])
            style.configure('Treeview', 
                           background=theme['colors']['background'],
                           foreground=theme['colors']['foreground'],
                           fieldbackground=theme['colors']['background'])
            style.configure('Treeview.Heading', 
                           background=theme['colors']['accent'],
                           foreground=theme['colors']['foreground'])
    
    def add_christmas_decorations(self, parent_frame: tk.Frame) -> None:
        """
        Add Christmas decorations to the parent frame
        """
        if not self.is_christmas_season:
            return
            
        # Add a Christmas banner
        banner_frame = tk.Frame(parent_frame, bg=self.get_active_theme()['colors']['accent'])
        banner_frame.pack(fill='x', pady=(0, 10))
        
        banner_label = tk.Label(
            banner_frame,
            text="🎄 CHRISTMAS EVENT ACTIVE! 🎄",
            font=("Arial", 14, "bold"),
            fg=self.get_active_theme()['colors']['foreground'],
            bg=self.get_active_theme()['colors']['accent']
        )
        banner_label.pack(pady=5)
        
        # Add Christmas messages
        messages = [
            "Ho Ho Ho! Your system is getting optimized for Christmas gaming!",
            "Christmas elves are optimizing your FPS!",
            "Merry Christmas! Your system is running in festive mode!",
            "Jingle bells, FPS spells - your system is optimized!"
        ]
        
        message_label = tk.Label(
            parent_frame,
            text=random.choice(messages),
            font=("Arial", 10, "italic"),
            fg=self.get_active_theme()['colors']['highlight'],
            bg=self.get_active_theme()['colors']['background']
        )
        message_label.pack(pady=5)
    
    def get_christmas_process_names(self) -> List[str]:
        """
        Get a list of Christmas-themed process names for decoration
        """
        return [
            "Santa's Sleigh.exe",
            "ReindeerManager.exe", 
            "ElfOptimizer.exe",
            "SnowflakeGenerator.exe",
            "ChristmasLights.exe",
            "GiftWrapper.exe",
            "Mistletoe.exe",
            "CandyCane.exe",
            "HotChocolate.exe",
            "NorthPole.exe"
        ]
    
    def get_christmas_status_messages(self) -> List[str]:
        """
        Get Christmas-themed status messages
        """
        return [
            "Ho Ho Ho! Optimizing for Christmas gaming!",
            "Christmas elves are boosting your FPS!",
            "Jingle bells, FPS spells!",
            "Merry Christmas! System optimized!",
            "Santa's elves are working hard!",
            "Festive optimization in progress!",
            "Christmas magic boosting your FPS!",
            "System running in Christmas mode!"
        ]


def is_christmas_time() -> bool:
    """
    Simple function to check if it's Christmas time
    """
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    
    # Christmas season is from December 1 to January 5
    if month == 12 and day >= 1:
        return True
    elif month == 1 and day <= 5:
        return True
    return False


def get_christmas_greeting() -> str:
    """
    Get a Christmas greeting based on the time of day
    """
    hour = datetime.datetime.now().hour
    
    if 5 <= hour < 12:
        time_greeting = "Morning"
    elif 12 <= hour < 17:
        time_greeting = "Afternoon" 
    elif 17 <= hour < 21:
        time_greeting = "Evening"
    else:
        time_greeting = "Night"
    
    greetings = [
        f"Good {time_greeting}! Merry Christmas! 🎄",
        f"Happy {time_greeting}! Christmas FPS boosting! ⛄",
        f"Season's Greetings! Optimizing for Christmas {time_greeting}! 🎅",
        f"Merry Christmas {time_greeting}! Your system is jolly fast! 🎁"
    ]
    
    return random.choice(greetings)


def get_christmas_motivational_message() -> str:
    """
    Get a Christmas-themed motivational message
    """
    messages = [
        "Christmas magic is boosting your FPS!",
        "Santa's elves are optimizing your system!",
        "Your FPS is more jolly now!",
        "Christmas cheer increases performance!",
        "Ho Ho Ho! Your system is running faster!",
        "Christmas spirit powers your performance!",
        "Festive optimization brings joy and speed!",
        "Merry Christmas! Your FPS is merry and bright!"
    ]
    
    return random.choice(messages)