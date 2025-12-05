"""
Fast Optimizer module using C++ backend for improved performance.
Provides high-speed system optimization functions for the FPS booster.
"""

from .cpp_performance_wrapper import CppPerformanceOptimizer
import time
import threading
from typing import Dict, List, Tuple, Optional


class FastPerformanceOptimizer:
    """
    High-performance system optimizer using C++ backend for faster execution.
    """
    
    def __init__(self):
        self.cpp_optimizer = CppPerformanceOptimizer()
        self.is_gaming_mode = False
        self.optimization_count = 0
        self.last_optimization_time = 0
        
    def get_system_info_fast(self) -> Dict[str, float]:
        """
        Get system information using fast C++ implementation.
        Returns dict with CPU usage, memory info, temperature, etc.
        """
        return {
            'cpu_usage': self.cpp_optimizer.get_cpu_usage(),
            'available_memory': self.cpp_optimizer.get_available_memory(),
            'total_memory': self.cpp_optimizer.get_total_memory(),
            'memory_used': self.cpp_optimizer.get_total_memory() - self.cpp_optimizer.get_available_memory(),
            'system_load': self.cpp_optimizer.get_system_load(),
            'cpu_temp': self.cpp_optimizer.get_cpu_temperature(),
            'uptime': self.cpp_optimizer.get_system_uptime()
        }
    
    def optimize_system_fast(self, aggressive: bool = False) -> bool:
        """
        Perform fast system optimization using C++ backend.
        """
        try:
            # Clear system caches for immediate memory boost
            self.cpp_optimizer.clear_system_caches()
            
            # If in gaming mode, apply gaming-specific optimizations
            if self.is_gaming_mode:
                self.cpp_optimizer.optimize_for_gaming()
            
            self.optimization_count += 1
            self.last_optimization_time = time.time()
            
            return True
        except Exception as e:
            print(f"Error during fast optimization: {e}")
            return False
    
    def enable_gaming_mode(self) -> bool:
        """Enable high-performance gaming mode."""
        try:
            self.cpp_optimizer.optimize_for_gaming()
            self.is_gaming_mode = True
            return True
        except Exception as e:
            print(f"Error enabling gaming mode: {e}")
            return False
    
    def disable_gaming_mode(self) -> bool:
        """Disable gaming mode and restore normal settings."""
        try:
            self.cpp_optimizer.restore_normal_settings()
            self.is_gaming_mode = False
            return True
        except Exception as e:
            print(f"Error disabling gaming mode: {e}")
            return False
    
    def get_optimization_stats(self) -> Dict[str, int]:
        """Get statistics about optimizations performed."""
        return {
            'optimizations_performed': self.optimization_count,
            'last_optimization_time': self.last_optimization_time
        }
    
    def batch_optimize(self, iterations: int = 5) -> Dict[str, any]:
        """
        Perform multiple optimization passes for maximum performance gain.
        """
        start_time = time.time()
        
        for _ in range(iterations):
            self.optimize_system_fast()
            time.sleep(0.01)  # Small delay to allow system to respond
        
        end_time = time.time()
        
        return {
            'duration': end_time - start_time,
            'iterations': iterations,
            'average_iteration_time': (end_time - start_time) / iterations,
            'final_stats': self.get_optimization_stats()
        }


# Global instance for shared use
fast_optimizer_instance = FastPerformanceOptimizer()


def get_fast_optimizer():
    """Get the global fast optimizer instance."""
    return fast_optimizer_instance