import time
import threading
from datetime import datetime
import logging
from .update_manager import update_manager

class UpdateScheduler:
    """
    A scheduler that handles timing of update checks with autosave functionality
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.check_interval = 3600  # Default to 1 hour (3600 seconds)
        self.thread = None
        self.running = False
        self.last_check_time = None
        
    def set_check_interval(self, hours):
        """Set the interval between update checks in hours"""
        self.check_interval = hours * 3600  # Convert hours to seconds
        
    def run_scheduler(self):
        """Main scheduler loop that runs in a separate thread"""
        self.logger.info("Update scheduler started")
        while self.running:
            try:
                # Check if it's time for an update
                if self.should_check_now():
                    self.logger.info("Running scheduled update check")
                    update_manager.check_for_updates()
                    self.last_check_time = time.time()
                
                # Sleep for 1 minute before checking again
                for _ in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in update scheduler: {e}")
                time.sleep(60)  # Wait before retrying
        
        self.logger.info("Update scheduler stopped")
    
    def should_check_now(self):
        """Determine if we should run an update check now"""
        if self.last_check_time is None:
            return True
            
        elapsed_time = time.time() - self.last_check_time
        return elapsed_time >= self.check_interval
    
    def start(self):
        """Start the update scheduler"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.thread.start()
        self.logger.info("Update scheduler thread started")
    
    def stop(self):
        """Stop the update scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
        self.logger.info("Update scheduler stopped")

# Global scheduler instance
scheduler = UpdateScheduler()

def start_update_scheduler():
    """Start the update scheduler"""
    scheduler.start()

def stop_update_scheduler():
    """Stop the update scheduler"""
    scheduler.stop()

def configure_update_schedule(hours_interval=24):
    """Configure and start the update scheduler with specified interval"""
    scheduler.set_check_interval(hours_interval)
    start_update_scheduler()