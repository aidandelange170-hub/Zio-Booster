"""
Temperature monitoring utilities for Zio-Booster
"""

import psutil
import platform
import subprocess
import os
from typing import List, Dict, Optional

class TemperatureMonitor:
    """Class to monitor system temperatures and related metrics"""
    
    def __init__(self):
        self.system = platform.system()
    
    def get_cpu_temperature(self) -> Optional[float]:
        """
        Get CPU temperature if available
        Returns temperature in Celsius or None if not available
        """
        try:
            # Try psutil sensors (works on some systems)
            temps = psutil.sensors_temperatures()
            if temps:
                # Look for common temperature sensor names
                for name, entries in temps.items():
                    if name in ['coretemp', 'cpu_thermal', 'acpi', 'k10temp']:
                        if entries:
                            return entries[0].current
                # If no specific CPU sensor found, return first available
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
        except AttributeError:
            # sensors_temperatures not available on this platform
            pass
        except Exception:
            pass
        
        # On Linux, try other methods
        if self.system == "Linux":
            try:
                # Try to read from thermal zone
                for i in range(10):  # Check first 10 thermal zones
                    thermal_path = f"/sys/class/thermal/thermal_zone{i}/temp"
                    if os.path.exists(thermal_path):
                        with open(thermal_path, 'r') as f:
                            temp = float(f.read().strip()) / 1000.0  # Convert from millidegrees
                            return temp
            except Exception:
                pass
        
        # On Windows, we might need to use other tools
        elif self.system == "Windows":
            try:
                # This is a simplified approach - real implementation would need more
                # For now, we'll return None as Windows doesn't typically expose temp via psutil
                pass
            except Exception:
                pass
        
        # On macOS
        elif self.system == "Darwin":
            try:
                # Requires installation of osx-cpu-temp tool
                result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
                if result.returncode == 0:
                    temp_str = result.stdout.strip().replace('°C', '')
                    return float(temp_str)
            except Exception:
                pass
        
        return None
    
    def get_process_temperatures(self) -> List[Dict]:
        """
        Get temperature-related information for processes
        Since direct process temperature isn't available, we'll use CPU usage as a proxy
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info'])
                
                # Calculate a "temperature score" based on resource usage
                # Higher CPU usage = higher temperature
                cpu_usage = pinfo['cpu_percent'] or 0
                memory_usage = (pinfo['memory_info'].rss / 1024 / 1024) if pinfo['memory_info'] else 0  # MB
                
                # Create a simulated temperature based on resource usage
                temp_score = min(100, cpu_usage * 0.7 + (memory_usage / 100) * 0.3)
                
                pinfo['temperature_score'] = round(temp_score, 2)
                processes.append(pinfo)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by temperature score (highest first)
        processes.sort(key=lambda x: x['temperature_score'], reverse=True)
        return processes
    
    def get_highest_temperature_processes(self, limit: int = 10) -> List[Dict]:
        """Get the processes with the highest temperature scores"""
        all_processes = self.get_process_temperatures()
        return all_processes[:limit]
    
    def terminate_high_temperature_process(self, pid: int) -> bool:
        """Terminate a process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)  # Wait up to 3 seconds for process to terminate
            return True
        except psutil.NoSuchProcess:
            print(f"Process with PID {pid} does not exist")
            return False
        except psutil.AccessDenied:
            print(f"Access denied terminating process with PID {pid}")
            return False
        except Exception as e:
            print(f"Error terminating process with PID {pid}: {e}")
            return False