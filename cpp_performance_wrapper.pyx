# cython: language_level=3
import numpy as np
cimport numpy as cnp
from libc.stdint cimport int32_t, int64_t
from libcpp.vector cimport vector
from libcpp.pair cimport pair

cdef extern from "cpp_performance.h":
    cdef struct PerformanceOptimizer:
        pass  # Opaque structure

    cdef PerformanceOptimizer* create_optimizer()
    cdef void destroy_optimizer(PerformanceOptimizer* opt)
    cdef double get_system_memory_usage(PerformanceOptimizer* opt)
    cdef double get_system_load(PerformanceOptimizer* opt)
    cdef double get_cpu_temperature(PerformanceOptimizer* opt)
    cdef void optimize_for_gaming(PerformanceOptimizer* opt)
    cdef void restore_normal_settings(PerformanceOptimizer* opt)
    cdef void clear_system_caches(PerformanceOptimizer* opt)
    cdef double get_available_memory(PerformanceOptimizer* opt)
    cdef double get_total_memory(PerformanceOptimizer* opt)
    cdef double get_cpu_usage(PerformanceOptimizer* opt)
    cdef double get_system_uptime(PerformanceOptimizer* opt)

cdef class PyPerformanceOptimizer:
    cdef PerformanceOptimizer* thisptr
    
    def __cinit__(self):
        self.thisptr = create_optimizer()
    
    def __dealloc__(self):
        if self.thisptr:
            destroy_optimizer(self.thisptr)
    
    def get_system_memory_usage(self):
        return get_system_memory_usage(self.thisptr)
    
    def get_system_load(self):
        return get_system_load(self.thisptr)
    
    def get_cpu_temperature(self):
        return get_cpu_temperature(self.thisptr)
    
    def optimize_for_gaming(self):
        optimize_for_gaming(self.thisptr)
    
    def restore_normal_settings(self):
        restore_normal_settings(self.thisptr)
    
    def clear_system_caches(self):
        clear_system_caches(self.thisptr)
    
    def get_available_memory(self):
        return get_available_memory(self.thisptr)
    
    def get_total_memory(self):
        return get_total_memory(self.thisptr)
    
    def get_cpu_usage(self):
        return get_cpu_usage(self.thisptr)
    
    def get_system_uptime(self):
        return get_system_uptime(self.thisptr)