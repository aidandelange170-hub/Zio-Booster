import json
import os
import time
from datetime import datetime, timedelta
import threading
import logging
from .auto_updater import AutoUpdater

class UpdateManager:
    def __init__(self, config_path="/workspace/config/version.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.logger = logging.getLogger(__name__)
        self.update_thread = None
        self.running = False
        
    def load_config(self):
        """Load the configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Create default config if it doesn't exist
            default_config = {
                "current_version": "1.0.0",
                "last_update_check": "2023-06-01T00:00:00Z",
                "auto_update_enabled": True,
                "check_interval_hours": 24
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Save the configuration to file"""
        if config is None:
            config = self.config
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_time_since_last_check(self):
        """Get the time elapsed since the last update check"""
        last_check_str = self.config.get('last_update_check', '2023-06-01T00:00:00Z')
        last_check = datetime.fromisoformat(last_check_str.replace('Z', '+00:00'))
        return datetime.now() - last_check.replace(tzinfo=None)
    
    def should_check_for_updates(self):
        """Determine if it's time to check for updates"""
        if not self.config.get('auto_update_enabled', True):
            return False
            
        time_since_check = self.get_time_since_last_check()
        check_interval = timedelta(hours=self.config.get('check_interval_hours', 24))
        
        return time_since_check >= check_interval
    
    def update_last_check_time(self):
        """Update the last check time to now"""
        self.config['last_update_check'] = datetime.now().isoformat()
        self.save_config()
    
    def check_for_updates(self):
        """Check for updates and install if available"""
        if not self.should_check_for_updates():
            return False
            
        self.logger.info("Checking for updates...")
        
        updater = AutoUpdater(
            repo_owner="aidandelange170-hub",
            repo_name="Zio-Booster",
            current_version=self.config.get('current_version', '1.0.0'),
            install_path=os.getcwd()
        )
        
        is_updated = updater.run_update_check()
        
        if is_updated:
            # Update the version in config after successful update
            latest_release = updater.get_latest_release()
            if latest_release:
                self.config['current_version'] = latest_release['version']
                self.logger.info(f"Updated to version {latest_release['version']}")
        
        self.update_last_check_time()
        return is_updated
    
    def start_periodic_checks(self):
        """Start periodic update checks in a separate thread"""
        if self.running:
            self.logger.warning("Update manager is already running")
            return
            
        self.running = True
        self.update_thread = threading.Thread(target=self._periodic_check_loop, daemon=True)
        self.update_thread.start()
        self.logger.info("Started periodic update checks")
    
    def stop_periodic_checks(self):
        """Stop periodic update checks"""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)  # Wait up to 2 seconds for thread to finish
        self.logger.info("Stopped periodic update checks")
    
    def _periodic_check_loop(self):
        """Internal method that runs periodic checks"""
        while self.running:
            try:
                self.check_for_updates()
                # Sleep for 1 hour before checking again (instead of busy waiting)
                for _ in range(60 * 60):  # 1 hour in seconds
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in periodic update check: {e}")
                # Wait a bit before retrying
                time.sleep(60)  # Wait 1 minute before retrying
    
    def manual_update_check(self):
        """Manually trigger an update check"""
        self.logger.info("Manual update check triggered")
        self.update_last_check_time()  # Update the timestamp to prevent immediate re-check
        return self.check_for_updates()

# Global instance to be used throughout the application
update_manager = UpdateManager()

def initialize_auto_updates():
    """Initialize and start the auto-update system"""
    update_manager.start_periodic_checks()

def check_for_updates_now():
    """Manually check for updates now"""
    return update_manager.manual_update_check()

def get_current_version():
    """Get the current application version"""
    return update_manager.config.get('current_version', '1.0.0')

def set_auto_update_enabled(enabled):
    """Enable or disable auto updates"""
    update_manager.config['auto_update_enabled'] = enabled
    update_manager.save_config()