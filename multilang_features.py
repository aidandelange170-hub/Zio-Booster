"""
Multi-Language Features Integration Module
This module integrates features implemented in different programming languages:
- Rust for performance-critical operations
- Go for concurrent processing
- JavaScript/TypeScript for web UI
- Shell for system-level operations
"""

import os
import subprocess
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    # Try to import the Rust extension if available
    from rust_features.performance_features import (
        calculate_process_priority,
        optimize_system_resources,
        calculate_performance_score,
        SystemOptimizer
    )
    RUST_AVAILABLE = True
except ImportError:
    print("Rust extension not available. Install with: cargo build --release in /workspace/rust_features")
    RUST_AVAILABLE = False


@dataclass
class SystemMetrics:
    """Data class to hold system metrics"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float
    timestamp: float
    process_count: int = 0
    temperature: Optional[float] = None


class MultiLanguageFeatures:
    """Main class to manage features implemented in different languages"""
    
    def __init__(self):
        self.rust_available = RUST_AVAILABLE
        self.system_optimizer = None
        
        # Initialize Rust optimizer if available
        if self.rust_available:
            self.system_optimizer = SystemOptimizer()
    
    def get_rust_performance_features(self) -> Dict[str, Any]:
        """Get performance features implemented in Rust"""
        if not self.rust_available:
            return {"error": "Rust extension not available"}
        
        # Example usage of Rust functions
        priority = calculate_process_priority(75.0, 80.0, 0)
        processes = ["idle_process", "background_service", "main_application"]
        optimized_processes = optimize_system_resources(processes, 75.0)
        
        metrics = {
            "cpu_usage": 75.0,
            "memory_usage": 80.0,
            "disk_usage": 60.0,
            "network_usage": 30.0
        }
        score = calculate_performance_score(metrics)
        
        return {
            "calculated_priority": priority,
            "optimized_processes": optimized_processes,
            "performance_score": score,
            "rust_available": True
        }
    
    def run_go_concurrent_monitor(self) -> Dict[str, Any]:
        """Run Go concurrent monitor and get results"""
        go_file = Path("/workspace/go_features/concurrent_monitor.go")
        
        if not go_file.exists():
            return {"error": "Go concurrent monitor file not found"}
        
        try:
            # Run the Go program and capture output
            result = subprocess.run(
                ["go", "run", str(go_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Simple parsing of Go output
                lines = result.stdout.strip().split('\n')
                go_output = lines[-1] if lines else "No output"
                
                return {
                    "success": True,
                    "output": go_output,
                    "language": "Go",
                    "feature": "concurrent system monitoring"
                }
            else:
                return {
                    "error": f"Go program failed: {result.stderr}",
                    "return_code": result.returncode
                }
        except subprocess.TimeoutExpired:
            return {"error": "Go program timed out"}
        except FileNotFoundError:
            return {"error": "Go executable not found. Install Go to use this feature."}
    
    def get_js_web_features(self) -> Dict[str, str]:
        """Get information about JavaScript web features"""
        ts_file = Path("/workspace/js_features/system-monitor.ts")
        
        if not ts_file.exists():
            return {"error": "JavaScript features file not found"}
        
        return {
            "file": str(ts_file),
            "language": "TypeScript/JavaScript",
            "feature": "Web-based system monitoring UI component",
            "description": "Custom web component for real-time system monitoring with performance metrics visualization"
        }
    
    def run_shell_optimization(self, mode: str = "info") -> Dict[str, Any]:
        """Run shell optimization script"""
        shell_script = Path("/workspace/shell_features/system_optimizer.sh")
        
        if not shell_script.exists():
            return {"error": "Shell optimization script not found"}
        
        try:
            # Make sure the script is executable
            shell_script.chmod(0o755)
            
            cmd = [str(shell_script), f"--{mode}"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "language": "Shell/Bash",
                "feature": "System optimization and cleaning"
            }
        except subprocess.TimeoutExpired:
            return {"error": "Shell script timed out"}
        except Exception as e:
            return {"error": f"Error running shell script: {str(e)}"}
    
    def integrated_performance_analysis(self) -> Dict[str, Any]:
        """Perform integrated analysis using features from all languages"""
        analysis = {
            "timestamp": time.time(),
            "features_evaluated": {},
            "summary": {}
        }
        
        # Evaluate Rust features
        if self.rust_available:
            analysis["features_evaluated"]["rust"] = self.get_rust_performance_features()
        else:
            analysis["features_evaluated"]["rust"] = {"status": "not available"}
        
        # Evaluate Go features
        analysis["features_evaluated"]["go"] = self.run_go_concurrent_monitor()
        
        # Evaluate JavaScript features
        analysis["features_evaluated"]["javascript"] = self.get_js_web_features()
        
        # Evaluate Shell features
        analysis["features_evaluated"]["shell"] = self.run_shell_optimization(mode="info")
        
        # Create summary
        successful_features = 0
        for lang, result in analysis["features_evaluated"].items():
            if result.get("success") or result.get("performance_score") or "error" not in result:
                successful_features += 1
        
        analysis["summary"] = {
            "total_languages_integrated": len(analysis["features_evaluated"]),
            "successful_features": successful_features,
            "languages_available": [
                lang for lang, result in analysis["features_evaluated"].items()
                if not result.get("error")
            ]
        }
        
        return analysis
    
    def boost_system_performance(self) -> Dict[str, Any]:
        """Use all available language features to boost system performance"""
        if not self.rust_available:
            return {"error": "Cannot boost performance: Rust features unavailable"}
        
        results = {}
        
        # Use Rust optimizer
        if self.system_optimizer:
            boost_result = self.system_optimizer.boost_performance(15.0)
            results["rust_optimizer"] = {
                "efficiency_level": boost_result,
                "status": self.system_optimizer.get_status()
            }
        
        # Get updated Rust performance features
        results["updated_features"] = self.get_rust_performance_features()
        
        # Run shell optimization (non-destructive info mode)
        results["shell_analysis"] = self.run_shell_optimization(mode="info")
        
        return {
            "action": "system_performance_boost",
            "timestamp": time.time(),
            "results": results,
            "message": "Performance boost applied using multi-language features"
        }


def main():
    """Example usage of multi-language features"""
    print("Initializing Multi-Language Features...")
    features = MultiLanguageFeatures()
    
    print("\n1. Integrated Performance Analysis:")
    analysis = features.integrated_performance_analysis()
    print(json.dumps(analysis, indent=2))
    
    print("\n2. Rust Performance Features:")
    if features.rust_available:
        rust_features = features.get_rust_performance_features()
        print(json.dumps(rust_features, indent=2))
    else:
        print("Rust features not available")
    
    print("\n3. Running System Performance Boost:")
    boost_result = features.boost_system_performance()
    print(json.dumps(boost_result, indent=2))


if __name__ == "__main__":
    main()