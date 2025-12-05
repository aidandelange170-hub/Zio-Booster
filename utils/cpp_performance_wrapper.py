import ctypes
from ctypes import c_void_p, c_double, c_int, POINTER
import os
import platform

class CppPerformanceOptimizer:
    """
    Python wrapper for the C++ PerformanceOptimizer class using ctypes.
    Provides fast system optimization functions for the FPS booster application.
    """
    
    def __init__(self):
        # Load the compiled C++ library
        if platform.system() == "Linux":
            lib_path = "./libcpp_performance.so"
        elif platform.system() == "Darwin":
            lib_path = "./libcpp_performance.dylib"
        else:
            raise OSError(f"Unsupported platform: {platform.system()}")
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"C++ library not found at {lib_path}")
        
        self.lib = ctypes.CDLL(lib_path)
        
        # Define the types for the C functions
        self._setup_function_signatures()
        
        # Create an instance of the C++ PerformanceOptimizer
        self.optimizer_ptr = self.lib.create_optimizer()
    
    def _setup_function_signatures(self):
        """Define the argument and return types for the C functions."""
        # create_optimizer
        self.lib.create_optimizer.argtypes = []
        self.lib.create_optimizer.restype = c_void_p
        
        # destroy_optimizer
        self.lib.destroy_optimizer.argtypes = [c_void_p]
        self.lib.destroy_optimizer.restype = None
        
        # get_system_memory_usage
        self.lib.get_system_memory_usage.argtypes = [c_void_p]
        self.lib.get_system_memory_usage.restype = c_double
        
        # get_system_load
        self.lib.get_system_load.argtypes = [c_void_p]
        self.lib.get_system_load.restype = c_double
        
        # get_cpu_temperature
        self.lib.get_cpu_temperature.argtypes = [c_void_p]
        self.lib.get_cpu_temperature.restype = c_double
        
        # optimize_for_gaming
        self.lib.optimize_for_gaming.argtypes = [c_void_p]
        self.lib.optimize_for_gaming.restype = None
        
        # restore_normal_settings
        self.lib.restore_normal_settings.argtypes = [c_void_p]
        self.lib.restore_normal_settings.restype = None
        
        # clear_system_caches
        self.lib.clear_system_caches.argtypes = [c_void_p]
        self.lib.clear_system_caches.restype = None
        
        # get_available_memory
        self.lib.get_available_memory.argtypes = [c_void_p]
        self.lib.get_available_memory.restype = c_double
        
        # get_total_memory
        self.lib.get_total_memory.argtypes = [c_void_p]
        self.lib.get_total_memory.restype = c_double
        
        # get_cpu_usage
        self.lib.get_cpu_usage.argtypes = [c_void_p]
        self.lib.get_cpu_usage.restype = c_double
        
        # get_system_uptime
        self.lib.get_system_uptime.argtypes = [c_void_p]
        self.lib.get_system_uptime.restype = c_double
    
    def get_system_memory_usage(self):
        """Get system memory usage in MB."""
        return self.lib.get_system_memory_usage(self.optimizer_ptr)
    
    def get_system_load(self):
        """Get system load average."""
        return self.lib.get_system_load(self.optimizer_ptr)
    
    def get_cpu_temperature(self):
        """Get CPU temperature in Celsius."""
        return self.lib.get_cpu_temperature(self.optimizer_ptr)
    
    def optimize_for_gaming(self):
        """Optimize system settings for gaming performance."""
        self.lib.optimize_for_gaming(self.optimizer_ptr)
    
    def restore_normal_settings(self):
        """Restore normal system settings."""
        self.lib.restore_normal_settings(self.optimizer_ptr)
    
    def clear_system_caches(self):
        """Clear system caches to free up memory."""
        self.lib.clear_system_caches(self.optimizer_ptr)
    
    def get_available_memory(self):
        """Get available memory in MB."""
        return self.lib.get_available_memory(self.optimizer_ptr)
    
    def get_total_memory(self):
        """Get total memory in MB."""
        return self.lib.get_total_memory(self.optimizer_ptr)
    
    def get_cpu_usage(self):
        """Get current CPU usage percentage."""
        return self.lib.get_cpu_usage(self.optimizer_ptr)
    
    def get_system_uptime(self):
        """Get system uptime in seconds."""
        return self.lib.get_system_uptime(self.optimizer_ptr)
    
    def __del__(self):
        """Clean up the C++ optimizer instance when Python object is destroyed."""
        if hasattr(self, 'optimizer_ptr') and self.optimizer_ptr:
            self.lib.destroy_optimizer(self.optimizer_ptr)
            self.optimizer_ptr = None


# Test the wrapper
if __name__ == "__main__":
    try:
        optimizer = CppPerformanceOptimizer()
        
        print("Testing C++ Performance Optimizer Wrapper:")
        print(f"CPU Usage: {optimizer.get_cpu_usage():.2f}%")
        print(f"Available Memory: {optimizer.get_available_memory():.2f} MB")
        print(f"Total Memory: {optimizer.get_total_memory():.2f} MB")
        print(f"System Load: {optimizer.get_system_load():.2f}")
        print(f"CPU Temperature: {optimizer.get_cpu_temperature():.2f}°C")
        print(f"System Uptime: {optimizer.get_system_uptime():.2f} seconds")
        
        # Test optimization functions
        print("\nTesting optimization functions...")
        optimizer.optimize_for_gaming()
        print("Applied gaming optimizations")
        
        optimizer.clear_system_caches()
        print("Cleared system caches")
        
        optimizer.restore_normal_settings()
        print("Restored normal settings")
        
    except Exception as e:
        print(f"Error: {e}")