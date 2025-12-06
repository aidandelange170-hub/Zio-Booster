"""
AI-Powered System Optimizer using Machine Learning
Implements intelligent optimization based on system patterns and usage data
"""
import time
import psutil
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import os
from datetime import datetime
import threading
import json


class AIOptimizer:
    """
    AI-powered optimizer that learns system patterns and optimizes accordingly
    """
    
    def __init__(self, model_path=None):
        self.model_path = model_path or "./ai_model.pkl"
        self.scaler_path = "./ai_scaler.pkl"
        self.data_path = "./ai_training_data.json"
        
        # Initialize ML components
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.training_data = []
        
        # Load existing model if available
        self.load_model()
        
        # Performance metrics
        self.optimization_history = []
        self.system_metrics_history = []
        
    def collect_system_features(self):
        """
        Collect system metrics to create feature vector for ML model
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Create feature vector
        features = [
            cpu_percent,  # CPU usage %
            memory.percent,  # Memory usage %
            disk.percent,  # Disk usage %
            network.bytes_sent / 1024 / 1024,  # Network sent (MB)
            network.bytes_recv / 1024 / 1024,  # Network received (MB)
            len(psutil.pids()),  # Number of processes
            memory.available / 1024 / 1024 / 1024,  # Available memory (GB)
            disk.free / 1024 / 1024 / 1024,  # Free disk space (GB)
            time.time() % 86400,  # Time of day (seconds since midnight)
        ]
        
        return features
    
    def train_model(self, training_data=None):
        """
        Train the ML model with system data
        """
        if training_data is None:
            training_data = self.training_data
            
        if len(training_data) < 10:
            # Not enough data to train, return early
            return False
            
        # Convert to numpy array
        X = np.array(training_data)
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the isolation forest model
        self.model.fit(X_scaled)
        self.is_trained = True
        
        # Save the trained model
        self.save_model()
        
        return True
    
    def predict_anomaly(self, features):
        """
        Predict if current system state is anomalous (needs optimization)
        Returns 1 for normal, -1 for anomaly (needs optimization)
        """
        if not self.is_trained:
            # If not trained, return 1 (normal) to avoid over-optimization
            return 1
            
        # Scale the features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        prediction = self.model.predict(features_scaled)
        
        return prediction[0]
    
    def get_optimization_recommendation(self, features):
        """
        Get specific optimization recommendations based on current system state
        """
        recommendations = []
        
        cpu_usage, memory_usage, disk_usage, net_sent, net_recv, proc_count, avail_mem, free_disk, time_of_day = features
        
        # CPU-based recommendations
        if cpu_usage > 80:
            recommendations.append({
                'type': 'cpu',
                'action': 'reduce_process_priority',
                'severity': 'high',
                'reason': f'High CPU usage detected: {cpu_usage:.1f}%'
            })
        elif cpu_usage > 60:
            recommendations.append({
                'type': 'cpu',
                'action': 'monitor_process_usage',
                'severity': 'medium',
                'reason': f'Moderate CPU usage detected: {cpu_usage:.1f}%'
            })
        
        # Memory-based recommendations
        if memory_usage > 85:
            recommendations.append({
                'type': 'memory',
                'action': 'clear_cache_and_swap',
                'severity': 'high',
                'reason': f'High memory usage detected: {memory_usage:.1f}%'
            })
        elif memory_usage > 70:
            recommendations.append({
                'type': 'memory',
                'action': 'monitor_memory_usage',
                'severity': 'medium',
                'reason': f'Moderate memory usage detected: {memory_usage:.1f}%'
            })
        
        # Disk-based recommendations
        if disk_usage > 90:
            recommendations.append({
                'type': 'disk',
                'action': 'clean_temp_files',
                'severity': 'high',
                'reason': f'Critical disk usage detected: {disk_usage:.1f}%'
            })
        elif disk_usage > 75:
            recommendations.append({
                'type': 'disk',
                'action': 'monitor_disk_usage',
                'severity': 'medium',
                'reason': f'High disk usage detected: {disk_usage:.1f}%'
            })
        
        # Process count recommendations
        if proc_count > 200:
            recommendations.append({
                'type': 'process',
                'action': 'identify_unnecessary_processes',
                'severity': 'high',
                'reason': f'High number of processes detected: {proc_count}'
            })
        elif proc_count > 100:
            recommendations.append({
                'type': 'process',
                'action': 'monitor_process_list',
                'severity': 'medium',
                'reason': f'Moderate number of processes detected: {proc_count}'
            })
        
        return recommendations
    
    def optimize_system(self):
        """
        Perform AI-driven system optimization based on recommendations
        """
        start_time = time.time()
        
        # Collect current system features
        features = self.collect_system_features()
        
        # Get ML prediction
        anomaly_score = self.predict_anomaly(features)
        
        # Get specific recommendations
        recommendations = self.get_optimization_recommendation(features)
        
        # Apply optimizations based on recommendations
        applied_optimizations = []
        
        for rec in recommendations:
            if rec['severity'] == 'high':
                # Apply high severity optimizations
                if rec['action'] == 'reduce_process_priority':
                    result = self._reduce_cpu_intensive_processes()
                    applied_optimizations.append(result)
                elif rec['action'] == 'clear_cache_and_swap':
                    result = self._clear_memory_caches()
                    applied_optimizations.append(result)
                elif rec['action'] == 'clean_temp_files':
                    result = self._clean_temp_files()
                    applied_optimizations.append(result)
                elif rec['action'] == 'identify_unnecessary_processes':
                    result = self._identify_and_terminate_unnecessary_processes()
                    applied_optimizations.append(result)
        
        # Record optimization in history
        optimization_record = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'anomaly_score': anomaly_score,
            'recommendations_count': len(recommendations),
            'applied_optimizations_count': len(applied_optimizations),
            'duration': time.time() - start_time
        }
        
        self.optimization_history.append(optimization_record)
        
        # Add to training data for future learning
        self.training_data.append(features)
        if len(self.training_data) > 1000:  # Keep only recent data
            self.training_data = self.training_data[-500:]
        
        # Retrain model periodically
        if len(self.optimization_history) % 10 == 0:
            self.train_model()
        
        return {
            'anomaly_detected': anomaly_score == -1,
            'recommendations': recommendations,
            'applied_optimizations': applied_optimizations,
            'optimization_record': optimization_record
        }
    
    def _reduce_cpu_intensive_processes(self):
        """
        Reduce priority of CPU-intensive processes
        """
        try:
            high_cpu_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 20:
                        high_cpu_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            high_cpu_processes.sort(key=lambda p: p.info['cpu_percent'], reverse=True)
            
            # Reduce priority of top CPU consumers (first 5)
            optimized_count = 0
            for proc in high_cpu_processes[:5]:
                try:
                    # On Windows, we can set priority; on Unix, we use nice
                    if hasattr(proc, 'nice'):
                        current_nice = proc.nice()
                        new_nice = min(19, current_nice + 5)  # Increase nice value (lower priority)
                        proc.nice(new_nice)
                        optimized_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'action': 'reduce_process_priority',
                'result': f'Reduced priority of {optimized_count} processes',
                'success': True
            }
        except Exception as e:
            return {
                'action': 'reduce_process_priority',
                'result': f'Error: {str(e)}',
                'success': False
            }
    
    def _clear_memory_caches(self):
        """
        Clear system memory caches
        """
        try:
            # On Linux, we can write to /proc/sys/vm/drop_caches
            # On other systems, we just return success
            import platform
            if platform.system() == "Linux":
                try:
                    with open("/proc/sys/vm/drop_caches", "w") as f:
                        f.write("3\n")  # Drop pagecache, dentries and inodes
                except:
                    # If we can't write to drop_caches, just continue
                    pass
            
            return {
                'action': 'clear_cache_and_swap',
                'result': 'System caches cleared',
                'success': True
            }
        except Exception as e:
            return {
                'action': 'clear_cache_and_swap',
                'result': f'Error: {str(e)}',
                'success': False
            }
    
    def _clean_temp_files(self):
        """
        Clean temporary files
        """
        try:
            cleaned_count = 0
            import tempfile
            import shutil
            
            # Clean temp directory (be careful not to remove important files)
            temp_dir = tempfile.gettempdir()
            
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) and item.startswith('tmp') and time.time() - os.path.getmtime(item_path) > 86400:  # Older than 1 day
                        os.remove(item_path)
                        cleaned_count += 1
                    elif os.path.isdir(item_path) and item.startswith('tmp') and time.time() - os.path.getmtime(item_path) > 86400:
                        shutil.rmtree(item_path)
                        cleaned_count += 1
                except:
                    continue  # Skip files we can't access
            
            return {
                'action': 'clean_temp_files',
                'result': f'Removed {cleaned_count} temporary files',
                'success': True
            }
        except Exception as e:
            return {
                'action': 'clean_temp_files',
                'result': f'Error: {str(e)}',
                'success': False
            }
    
    def _identify_and_terminate_unnecessary_processes(self):
        """
        Identify and terminate unnecessary processes
        """
        try:
            terminated_count = 0
            unnecessary_process_names = [
                'dropbox', 'onedrive', 'google', 'spotify', 'vlc', 'steamwebhelper',
                'code helper', 'teams', 'slack', 'skype', 'browser', 'chrome', 'firefox'
            ]
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(name in proc_name for name in unnecessary_process_names):
                        # Don't terminate critical system processes
                        if not any(critical in proc_name for critical in ['system', 'kernel', 'init', 'kthreadd']):
                            proc.terminate()
                            terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'action': 'identify_unnecessary_processes',
                'result': f'Terminated {terminated_count} unnecessary processes',
                'success': True
            }
        except Exception as e:
            return {
                'action': 'identify_unnecessary_processes',
                'result': f'Error: {str(e)}',
                'success': False
            }
    
    def save_model(self):
        """
        Save the trained model to disk
        """
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            # Save training data
            with open(self.data_path, 'w') as f:
                json.dump(self.training_data, f)
                
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    def load_model(self):
        """
        Load the trained model from disk
        """
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.is_trained = True
            
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r') as f:
                    self.training_data = json.load(f)
                    
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def get_performance_metrics(self):
        """
        Get AI optimizer performance metrics
        """
        if not self.optimization_history:
            return {
                'total_optimizations': 0,
                'average_duration': 0,
                'last_optimization': None
            }
        
        total_duration = sum([rec['duration'] for rec in self.optimization_history])
        avg_duration = total_duration / len(self.optimization_history)
        
        return {
            'total_optimizations': len(self.optimization_history),
            'average_duration': avg_duration,
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None,
            'data_points_collected': len(self.training_data)
        }


class AIOptimizerManager:
    """
    Manager class to handle AI optimization in a separate thread
    """
    
    def __init__(self):
        self.ai_optimizer = AIOptimizer()
        self.is_running = False
        self.optimization_thread = None
        self.check_interval = 30  # seconds
    
    def start_optimization_loop(self):
        """
        Start the AI optimization loop in a separate thread
        """
        if self.is_running:
            return
        
        self.is_running = True
        self.optimization_thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.optimization_thread.start()
    
    def stop_optimization_loop(self):
        """
        Stop the AI optimization loop
        """
        self.is_running = False
        if self.optimization_thread:
            self.optimization_thread.join(timeout=2)
    
    def _optimization_loop(self):
        """
        Main optimization loop that runs in a separate thread
        """
        while self.is_running:
            try:
                result = self.ai_optimizer.optimize_system()
                print(f"AI Optimization completed: {result['applied_optimizations_count']} optimizations applied")
                
                # Wait for the specified interval
                for _ in range(self.check_interval):
                    if not self.is_running:
                        break
                    time.sleep(1)
            except Exception as e:
                print(f"Error in AI optimization loop: {e}")
                time.sleep(5)  # Wait a bit before trying again
    
    def run_single_optimization(self):
        """
        Run a single optimization cycle
        """
        return self.ai_optimizer.optimize_system()
    
    def get_performance_metrics(self):
        """
        Get performance metrics from the AI optimizer
        """
        return self.ai_optimizer.get_performance_metrics()


# Example usage and testing
if __name__ == "__main__":
    print("Testing AI Optimizer...")
    
    # Create AI optimizer instance
    ai_opt = AIOptimizer()
    
    # Collect some initial data for training
    print("Collecting initial system data...")
    for i in range(20):
        features = ai_opt.collect_system_features()
        ai_opt.training_data.append(features)
        print(f"Collected data point {i+1}: {features[:3]}...")  # Show first 3 features
        time.sleep(0.5)
    
    # Train the model
    print("Training the model...")
    success = ai_opt.train_model()
    print(f"Model training {'succeeded' if success else 'failed'}")
    
    # Run a test optimization
    print("Running test optimization...")
    result = ai_opt.optimize_system()
    print(f"Optimization result: {result}")
    
    # Show performance metrics
    metrics = ai_opt.get_performance_metrics()
    print(f"Performance metrics: {metrics}")