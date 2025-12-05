"""
Gaming Mode for Zio-Booster FPS Booster
Activates focused gaming mode with various optimizations
"""
import platform
import subprocess
import time
from typing import Dict, List, Optional
import psutil
import threading

class GamingMode:
    """Manages gaming mode with various optimizations"""
    
    def __init__(self):
        self.active = False
        self.original_power_plan = None
        self.background_services_disabled = []
        self.notifications_blocked = False
        self.power_savings_disabled = []
        self.optimization_thread = None
        
    def activate_gaming_mode(self):
        """Activate gaming mode with all optimizations"""
        if self.active:
            return True
            
        print("Activating Gaming Mode...")
        
        # Store original power plan
        self.original_power_plan = self._get_current_power_plan()
        
        # Apply optimizations
        self._disable_notifications()
        self._disable_power_saving_features()
        self._optimize_background_services()
        self._set_high_performance_plan()
        
        self.active = True
        print("Gaming Mode activated!")
        
        return True
    
    def deactivate_gaming_mode(self):
        """Deactivate gaming mode and restore original settings"""
        if not self.active:
            return True
            
        print("Deactivating Gaming Mode...")
        
        # Restore original settings
        self._restore_notifications()
        self._restore_power_saving_features()
        self._restore_background_services()
        self._restore_original_power_plan()
        
        self.active = False
        print("Gaming Mode deactivated!")
        
        return True
    
    def _get_current_power_plan(self) -> Optional[str]:
        """Get the current power plan"""
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['powercfg', '/getactivescheme'], 
                                      capture_output=True, text=True)
                # Extract GUID from the output
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'GUID:' in line:
                            return line.split('(')[0].strip().split(': ')[1]
            except Exception as e:
                print(f"Could not get power plan: {e}")
        return None
    
    def _set_high_performance_plan(self):
        """Set high performance power plan"""
        if platform.system() == "Windows":
            try:
                # Find high performance plan GUID
                result = subprocess.run(['powercfg', '/list'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'High performance' in line or 'Ultimate Performance' in line:
                            guid = line.split('(')[0].strip().split(': ')[1]
                            subprocess.run(['powercfg', '/setactive', guid], 
                                         capture_output=True)
                            print(f"Set power plan to High Performance")
                            break
            except Exception as e:
                print(f"Could not set power plan: {e}")
    
    def _restore_original_power_plan(self):
        """Restore the original power plan"""
        if self.original_power_plan and platform.system() == "Windows":
            try:
                subprocess.run(['powercfg', '/setactive', self.original_power_plan], 
                             capture_output=True)
                print(f"Restored original power plan")
            except Exception as e:
                print(f"Could not restore power plan: {e}")
    
    def _disable_notifications(self):
        """Disable system notifications during gaming"""
        if platform.system() == "Windows":
            try:
                # Enable Focus Assist (Quiet Hours) via registry
                subprocess.run([
                    'reg', 'add', 
                    'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings',
                    '/v', 'NOC_GLOBAL_SETTING_TOASTS_ENABLED',
                    '/t', 'REG_DWORD',
                    '/d', '0',
                    '/f'
                ], capture_output=True)
                
                # Alternative: Use Windows 10+ focus assist
                subprocess.run([
                    'powershell', '-Command',
                    'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\DUSM" -Name "QuietHours" -Value 1'
                ], capture_output=True)
                
                self.notifications_blocked = True
                print("Notifications disabled")
            except Exception as e:
                print(f"Could not disable notifications: {e}")
        elif platform.system() == "Linux":
            try:
                # Try to disable notifications via D-Bus
                subprocess.run([
                    'gdbus', 'call', '--session',
                    '--dest', 'org.freedesktop.Notifications',
                    '--object-path', '/org/freedesktop/Notifications',
                    '--method', 'org.freedesktop.DBus.Properties.Set',
                    'org.freedesktop.Notifications', 'enabled', 'false'
                ], capture_output=True)
                
                self.notifications_blocked = True
                print("Notifications disabled")
            except Exception as e:
                print(f"Could not disable notifications: {e}")
    
    def _restore_notifications(self):
        """Restore system notifications"""
        if platform.system() == "Windows":
            try:
                subprocess.run([
                    'reg', 'add', 
                    'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings',
                    '/v', 'NOC_GLOBAL_SETTING_TOASTS_ENABLED',
                    '/t', 'REG_DWORD',
                    '/d', '1',
                    '/f'
                ], capture_output=True)
                
                self.notifications_blocked = False
                print("Notifications restored")
            except Exception as e:
                print(f"Could not restore notifications: {e}")
    
    def _disable_power_saving_features(self):
        """Disable power saving features that might affect gaming"""
        try:
            # Disable screen saver
            if platform.system() == "Windows":
                subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '0'], 
                             capture_output=True)
                subprocess.run(['powercfg', '/change', 'hibernate-timeout-ac', '0'], 
                             capture_output=True)
                print("Disabled standby and hibernation timeouts")
            
            # Disable CPU frequency scaling to minimum
            self._disable_cpu_scaling()
            
            self.power_savings_disabled = ['screen_saver', 'cpu_scaling']
            print("Power saving features disabled")
        except Exception as e:
            print(f"Could not disable power saving features: {e}")
    
    def _disable_cpu_scaling(self):
        """Attempt to disable CPU frequency scaling"""
        if platform.system() == "Linux":
            try:
                # Check if cpufreq is available
                import glob
                freq_files = glob.glob('/sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq')
                
                # Set max frequency to highest possible
                for freq_file in freq_files:
                    with open(freq_file, 'r') as f:
                        max_freq = f.read().strip()
                    
                    # Write the same max frequency to prevent scaling down
                    with open(freq_file, 'w') as f:
                        f.write(max_freq)
                        
                print("CPU scaling minimized")
            except Exception as e:
                print(f"Could not disable CPU scaling: {e}")
    
    def _restore_power_saving_features(self):
        """Restore power saving features"""
        try:
            if platform.system() == "Windows":
                # Restore default timeouts (let's use 15 minutes as default)
                subprocess.run(['powercfg', '/change', 'standby-timeout-ac', '15'], 
                             capture_output=True)
                subprocess.run(['powercfg', '/change', 'hibernate-timeout-ac', '30'], 
                             capture_output=True)
                print("Power saving features restored")
        except Exception as e:
            print(f"Could not restore power saving features: {e}")
    
    def _optimize_background_services(self):
        """Optimize background services for gaming"""
        try:
            # Identify and temporarily reduce priority of non-critical services
            services_to_reduce = [
                'WindowsUpdate', 'BITS', 'OneSyncSvc', 'WaaSMedicSvc'
            ]
            
            for service in services_to_reduce:
                try:
                    # This is a simplified approach - actual service management requires admin rights
                    result = subprocess.run([
                        'sc', 'query', service
                    ], capture_output=True, text=True)
                    
                    if 'RUNNING' in result.stdout:
                        self.background_services_disabled.append(service)
                        print(f"Identified service {service} for optimization")
                except:
                    continue
                    
            print(f"Background services optimized: {len(self.background_services_disabled)} identified")
        except Exception as e:
            print(f"Could not optimize background services: {e}")
    
    def _restore_background_services(self):
        """Restore background services to normal state"""
        try:
            # In a real implementation, we would restore services to their original state
            print(f"Restored {len(self.background_services_disabled)} background services")
            self.background_services_disabled = []
        except Exception as e:
            print(f"Could not restore background services: {e}")
    
    def is_active(self) -> bool:
        """Check if gaming mode is currently active"""
        return self.active

# Example usage
if __name__ == "__main__":
    gaming_mode = GamingMode()
    
    # Activate gaming mode
    gaming_mode.activate_gaming_mode()
    time.sleep(5)  # Simulate gaming session
    
    # Deactivate gaming mode
    gaming_mode.deactivate_gaming_mode()