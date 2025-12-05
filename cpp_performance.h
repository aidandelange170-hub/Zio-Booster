#ifndef CPP_PERFORMANCE_H
#define CPP_PERFORMANCE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct PerformanceOptimizer PerformanceOptimizer;

PerformanceOptimizer* create_optimizer();
void destroy_optimizer(PerformanceOptimizer* opt);
double get_system_memory_usage(PerformanceOptimizer* opt);
double get_system_load(PerformanceOptimizer* opt);
double get_cpu_temperature(PerformanceOptimizer* opt);
void optimize_for_gaming(PerformanceOptimizer* opt);
void restore_normal_settings(PerformanceOptimizer* opt);
void clear_system_caches(PerformanceOptimizer* opt);
double get_available_memory(PerformanceOptimizer* opt);
double get_total_memory(PerformanceOptimizer* opt);
double get_cpu_usage(PerformanceOptimizer* opt);
double get_system_uptime(PerformanceOptimizer* opt);

#ifdef __cplusplus
}
#endif

#endif