"""
System optimization utilities for Zio-Booster FPS Booster
"""

import psutil
import platform
import time
from typing import List, Dict
from .temperature_monitor import TemperatureMonitor
from .profile_manager import ProfileManager, GameProfile
from .performance_metrics import PerformanceMetrics
from .gaming_mode import GamingMode

class SystemOptimizer:
    """Class to optimize system performance for better FPS"""
    
    def __init__(self):
        self.temp_monitor = TemperatureMonitor()
        self.original_process_priorities = {}
        self.profile_manager = ProfileManager()
        self.performance_metrics = PerformanceMetrics()
        self.gaming_mode = GamingMode()
        self.active_profile = None
        self.optimization_count = 0
        
    def apply_profile(self, profile_name: str) -> bool:
        """Apply settings from a game profile"""
        profile = self.profile_manager.get_profile(profile_name)
        if profile:
            self.active_profile = profile
            # Apply profile-specific settings
            print(f"Applied profile: {profile_name}")
            return True
        return False
    
    def enable_gaming_mode(self) -> bool:
        """Enable focused gaming mode"""
        return self.gaming_mode.activate_gaming_mode()
    
    def disable_gaming_mode(self) -> bool:
        """Disable focused gaming mode"""
        return self.gaming_mode.deactivate_gaming_mode()
    
    def capture_performance_snapshot(self):
        """Capture a performance snapshot"""
        snapshot = self.performance_metrics.capture_snapshot()
        # Update the active optimizations count in the snapshot
        snapshot.active_optimizations = self.optimization_count
        return snapshot
    
    def boost_cpu_performance(self):
        """Optimize CPU scheduling for better performance"""
        # On Linux, we could adjust CPU governor to performance mode
        # For now, we'll focus on process management
        pass
    
    def terminate_high_temperature_processes(self, threshold: float = 70.0, count: int = 3) -> List[int]:
        """
        Terminate processes that have high temperature scores
        threshold: temperature score threshold above which processes are considered high-temperature
        count: maximum number of processes to terminate
        """
        high_temp_processes = self.temp_monitor.get_highest_temperature_processes(count * 2)  # Get more than we need
        terminated_pids = []
        
        for proc in high_temp_processes:
            if proc['temperature_score'] >= threshold and len(terminated_pids) < count:
                pid = proc['pid']
                name = proc['name']
                
                # Don't terminate critical system processes
                if self._is_system_critical_process(name):
                    continue
                
                print(f"Terminating high-temperature process: {name} (PID: {pid}, Temp Score: {proc['temperature_score']})")
                
                if self.temp_monitor.terminate_high_temperature_process(pid):
                    terminated_pids.append(pid)
        
        return terminated_pids
    
    def _is_system_critical_process(self, process_name: str) -> bool:
        """Check if a process is critical to system operation"""
        critical_names = [
            'systemd', 'kernel', 'kthreadd', 'init', 'explorer.exe', 'svchost.exe',
            'wininit.exe', 'csrss.exe', 'lsass.exe', 'services.exe', 'dwm.exe',
            'winlogon.exe', 'spoolsv.exe', 'taskhost.exe', 'smss.exe', 'csrss.exe'
        ]
        
        # Convert to lowercase for comparison
        process_name_lower = process_name.lower() if process_name else ""
        
        for critical in critical_names:
            if critical in process_name_lower:
                return True
        
        return False
    
    def clean_memory(self):
        """Free up system memory"""
        # This is a simplified approach - actual memory cleaning depends on OS
        # We'll focus on terminating unnecessary processes that consume memory
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_info', 'memory_percent'])
                if pinfo['memory_percent'] and pinfo['memory_percent'] > 5:  # More than 5% memory usage
                    processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by memory usage
        processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
        
        # Terminate some high memory processes (excluding critical ones)
        terminated = []
        for proc in processes[:5]:  # Check top 5 memory consumers
            if not self._is_system_critical_process(proc['name']):
                if self.temp_monitor.terminate_high_temperature_process(proc['pid']):
                    terminated.append(proc['pid'])
        
        return terminated
    
    def optimize_network_for_games(self):
        """Optimize network settings for lower latency"""
        # This would require OS-specific implementations
        # For now, we'll just return a success message
        print("Network optimization applied (placeholder)")
        return True
    
    def set_high_priority_for_game(self, game_process_name: str = None):
        """Set high priority for a specific game process"""
        if not game_process_name:
            return False
            
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if game_process_name.lower() in proc.name().lower():
                    # Store original priority to restore later
                    try:
                        original_priority = proc.nice()
                        self.original_process_priorities[proc.pid] = original_priority
                        # Set to high priority (on Unix-like systems, lower nice value = higher priority)
                        proc.nice(-10)  # High priority
                        print(f"Set high priority for process: {proc.name()} (PID: {proc.pid})")
                        return True
                    except psutil.AccessDenied:
                        print(f"Access denied setting priority for process: {proc.name()}")
                        return False
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    
    def restore_process_priorities(self):
        """Restore original process priorities"""
        for pid, original_priority in self.original_process_priorities.items():
            try:
                proc = psutil.Process(pid)
                proc.nice(original_priority)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        self.original_process_priorities.clear()
    
    def run_optimization_cycle(self, temp_threshold: float = 70.0):
        """Run a complete optimization cycle"""
        print("Running optimization cycle...")
        
        # Capture performance before optimization
        self.capture_performance_snapshot()
        
        # Use profile-specific threshold if available
        threshold = self.active_profile.temp_threshold if self.active_profile else temp_threshold
        
        # Clean memory
        memory_cleaned = self.clean_memory()
        print(f"Cleaned memory by terminating {len(memory_cleaned)} processes")
        
        # Terminate high-temperature processes
        terminated = self.terminate_high_temperature_processes(threshold=threshold)
        print(f"Terminated {len(terminated)} high-temperature processes")
        
        # Apply other optimizations based on profile settings
        if not self.active_profile or self.active_profile.optimize_network:
            self.optimize_network_for_games()
        
        if not self.active_profile or self.active_profile.high_priority:
            # Set high priority for gaming processes (if known)
            pass
        
        # Update optimization count
        self.optimization_count += 1
        
        # Capture performance after optimization
        self.capture_performance_snapshot()
        
        print("Optimization cycle completed")
        return {
            'memory_cleaned_count': len(memory_cleaned),
            'terminated_processes': terminated,
            'cycle_complete': True,
            'optimization_count': self.optimization_count
        }