#!/usr/bin/env python3
"""
Test script for auto-update functionality
"""

import sys
import os

# Add the project root to the path so we can import utilities
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.update_manager import check_for_updates_now, get_current_version
from utils.update_scheduler import configure_update_schedule

def test_manual_update():
    """Test manual update check"""
    print(f"Current version: {get_current_version()}")
    print("Testing manual update check...")
    
    updated = check_for_updates_now()
    if updated:
        print("Update was installed!")
        print(f"New version: {get_current_version()}")
    else:
        print("No updates available or update failed.")

def test_scheduled_updates():
    """Test scheduled update functionality"""
    print("\nSetting up scheduled update checks (every 1 hour)...")
    configure_update_schedule(hours_interval=1)
    print("Scheduled update checks configured.")

if __name__ == "__main__":
    print("Zio-Booster Auto-Update Test")
    print("=" * 40)
    
    # Test manual update
    test_manual_update()
    
    # Test scheduled updates
    test_scheduled_updates()
    
    print("\nTest completed. The application will continue checking for updates in the background.")
    print("Press Ctrl+C to exit.")
    
    try:
        # Keep the script running to allow scheduled updates to work
        import time
        while True:
            time.sleep(60)  # Sleep for 1 minute
    except KeyboardInterrupt:
        print("\nExiting...")