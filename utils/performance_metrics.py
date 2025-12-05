"""
Advanced Performance Metrics for Zio-Booster FPS Booster
"""
import time
import psutil
import platform
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics

@dataclass
class PerformanceSnapshot:
    """A snapshot of system performance metrics at a specific time"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    cpu_temp: Optional[float]
    disk_io_read: float
    disk_io_write: float
    network_sent: float
    network_recv: float
    processes_count: int
    active_optimizations: int

class PerformanceMetrics:
    """Manages collection and analysis of performance metrics"""
    
    def __init__(self):
        self.snapshots: List[PerformanceSnapshot] = []
        self.network_baseline = psutil.net_io_counters()
        self.disk_baseline = psutil.disk_io_counters()
        
    def capture_snapshot(self) -> PerformanceSnapshot:
        """Capture a snapshot of current system performance"""
        # Get network I/O since last baseline
        network_current = psutil.net_io_counters()
        network_sent = network_current.bytes_sent - self.network_baseline.bytes_sent
        network_recv = network_current.bytes_recv - self.network_baseline.bytes_recv
        
        # Get disk I/O since last baseline
        disk_current = psutil.disk_io_counters()
        if disk_current:
            disk_read = disk_current.read_bytes - self.disk_baseline.read_bytes
            disk_write = disk_current.write_bytes - self.disk_baseline.write_bytes
        else:
            disk_read = 0
            disk_write = 0
        
        # Update baselines
        self.network_baseline = network_current
        if disk_current:
            self.disk_baseline = disk_current
        
        # Get CPU temperature if available
        cpu_temp = self._get_cpu_temperature()
        
        snapshot = PerformanceSnapshot(
            timestamp=time.time(),
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            cpu_temp=cpu_temp,
            disk_io_read=disk_read,
            disk_io_write=disk_write,
            network_sent=network_sent,
            network_recv=network_recv,
            processes_count=len(psutil.pids()),
            active_optimizations=0  # This would be updated by the optimizer
        )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature if available"""
        try:
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
        
        return None
    
    def get_cpu_trend(self, minutes: int = 5) -> List[Tuple[float, float]]:
        """Get CPU usage trend over the last specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        return [(s.timestamp, s.cpu_percent) for s in recent_snapshots]
    
    def get_memory_trend(self, minutes: int = 5) -> List[Tuple[float, float]]:
        """Get memory usage trend over the last specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        return [(s.timestamp, s.memory_percent) for s in recent_snapshots]
    
    def get_temperature_trend(self, minutes: int = 5) -> List[Tuple[float, Optional[float]]]:
        """Get temperature trend over the last specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        return [(s.timestamp, s.cpu_temp) for s in recent_snapshots if s.cpu_temp is not None]
    
    def get_average_metrics(self, minutes: int = 5) -> Dict[str, float]:
        """Get average metrics over the last specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        if not recent_snapshots:
            return {}
        
        avg_cpu = statistics.mean([s.cpu_percent for s in recent_snapshots])
        avg_memory = statistics.mean([s.memory_percent for s in recent_snapshots])
        
        # Only include temperature if available
        temp_snapshots = [s for s in recent_snapshots if s.cpu_temp is not None]
        avg_temp = statistics.mean([s.cpu_temp for s in temp_snapshots]) if temp_snapshots else None
        
        return {
            'avg_cpu_percent': avg_cpu,
            'avg_memory_percent': avg_memory,
            'avg_temperature': avg_temp,
            'snapshot_count': len(recent_snapshots)
        }
    
    def get_optimization_impact(self) -> Dict[str, float]:
        """Calculate the impact of optimizations"""
        if len(self.snapshots) < 2:
            return {}
        
        # Compare metrics before and after optimizations
        # This is a simplified version - in a real implementation, we'd track
        # when optimizations were applied
        before = self.snapshots[0]
        after = self.snapshots[-1]
        
        return {
            'cpu_improvement': before.cpu_percent - after.cpu_percent,
            'memory_improvement': before.memory_percent - after.memory_percent,
            'time_span': after.timestamp - before.timestamp
        }
    
    def get_peak_metrics(self, minutes: int = 5) -> Dict[str, float]:
        """Get peak metrics over the last specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        if not recent_snapshots:
            return {}
        
        peak_cpu = max([s.cpu_percent for s in recent_snapshots])
        peak_memory = max([s.memory_percent for s in recent_snapshots])
        
        # Only include temperature if available
        temp_snapshots = [s for s in recent_snapshots if s.cpu_temp is not None]
        peak_temp = max([s.cpu_temp for s in temp_snapshots]) if temp_snapshots else None
        
        return {
            'peak_cpu_percent': peak_cpu,
            'peak_memory_percent': peak_memory,
            'peak_temperature': peak_temp
        }
    
    def clear_old_snapshots(self, minutes: int = 60):
        """Clear snapshots older than specified minutes"""
        cutoff_time = time.time() - (minutes * 60)
        self.snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]

# Example usage
if __name__ == "__main__":
    metrics = PerformanceMetrics()
    
    # Capture a few snapshots
    for i in range(3):
        snapshot = metrics.capture_snapshot()
        print(f"Snapshot {i+1}: CPU={snapshot.cpu_percent}%, Memory={snapshot.memory_percent}%")
        time.sleep(2)
    
    # Get average metrics
    avg_metrics = metrics.get_average_metrics(minutes=1)
    print(f"Average metrics: {avg_metrics}")
    
    # Get peak metrics
    peak_metrics = metrics.get_peak_metrics(minutes=1)
    print(f"Peak metrics: {peak_metrics}")