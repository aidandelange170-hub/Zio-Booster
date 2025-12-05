use pyo3::prelude::*;
use std::collections::HashMap;

/// A function that calculates optimized process priorities based on system load
#[pyfunction]
fn calculate_process_priority(cpu_load: f64, memory_usage: f64, base_priority: i32) -> PyResult<i32> {
    let mut priority = base_priority;
    
    // Adjust priority based on CPU load
    if cpu_load > 80.0 {
        priority += 2;
    } else if cpu_load > 60.0 {
        priority += 1;
    }
    
    // Adjust priority based on memory usage
    if memory_usage > 85.0 {
        priority += 2;
    } else if memory_usage > 70.0 {
        priority += 1;
    }
    
    // Ensure priority stays within reasonable bounds
    priority = priority.clamp(-10, 10);
    
    Ok(priority)
}

/// A function that optimizes system resources using Rust's speed
#[pyfunction]
fn optimize_system_resources(processes: Vec<String>, cpu_threshold: f64) -> PyResult<Vec<String>> {
    let mut optimized_processes = Vec::new();
    
    for process in processes {
        // Simulate fast optimization logic in Rust
        if process.contains("idle") || process.contains("background") {
            optimized_processes.push(format!("optimized_{}", process));
        } else if cpu_threshold > 75.0 && process.len() > 5 {
            optimized_processes.push(format!("boosted_{}", process));
        } else {
            optimized_processes.push(process);
        }
    }
    
    Ok(optimized_processes)
}

/// A function that performs fast mathematical calculations for performance metrics
#[pyfunction]
fn calculate_performance_score(metrics: HashMap<String, f64>) -> PyResult<f64> {
    let mut score = 0.0;
    
    if let Some(cpu) = metrics.get("cpu_usage") {
        score += 100.0 - cpu;
    }
    
    if let Some(ram) = metrics.get("memory_usage") {
        score += 100.0 - ram;
    }
    
    if let Some(disk) = metrics.get("disk_usage") {
        score += 100.0 - disk;
    }
    
    if let Some(net) = metrics.get("network_usage") {
        score += 100.0 - net * 0.5; // Network usage has less impact
    }
    
    // Normalize the score to 0-100 range
    score = score / 4.0;
    score = score.clamp(0.0, 100.0);
    
    Ok(score)
}

/// A struct to represent a system optimizer
#[pyclass]
struct SystemOptimizer {
    #[pyo3(get, set)]
    efficiency_level: f64,
    #[pyo3(get, set)]
    optimization_count: u32,
}

#[pymethods]
impl SystemOptimizer {
    #[new]
    fn new() -> Self {
        SystemOptimizer {
            efficiency_level: 0.0,
            optimization_count: 0,
        }
    }
    
    fn boost_performance(&mut self, boost_factor: f64) -> PyResult<f64> {
        self.efficiency_level = (self.efficiency_level + boost_factor).min(100.0);
        self.optimization_count += 1;
        
        Ok(self.efficiency_level)
    }
    
    fn reset_optimizer(&mut self) {
        self.efficiency_level = 0.0;
        self.optimization_count = 0;
    }
    
    fn get_status(&self) -> PyResult<String> {
        Ok(format!(
            "Efficiency: {:.2}%, Optimizations: {}",
            self.efficiency_level, self.optimization_count
        ))
    }
}

/// This function registers the Python module
#[pymodule]
fn performance_features(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_process_priority, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_system_resources, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_performance_score, m)?)?;
    m.add_class::<SystemOptimizer>()?;
    Ok(())
}