/**
 * System Monitor UI Component for Web-based Performance Monitoring
 */

interface SystemMetrics {
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  networkUsage: number;
  timestamp: Date;
  processCount: number;
  temperature?: number;
}

interface OptimizationResult {
  status: 'success' | 'error' | 'warning';
  message: string;
  performanceBoost: number;
}

class WebSystemMonitor {
  private metricsHistory: SystemMetrics[] = [];
  private isMonitoring: boolean = false;
  private updateInterval: number | null = null;
  private readonly maxHistory: number = 100;

  /**
   * Start monitoring system metrics
   */
  startMonitoring(): void {
    if (this.isMonitoring) return;
    
    this.isMonitoring = true;
    console.log('Starting system monitoring...');
    
    this.updateInterval = window.setInterval(() => {
      const metrics = this.collectMetrics();
      this.metricsHistory.push(metrics);
      
      // Keep history within limits
      if (this.metricsHistory.length > this.maxHistory) {
        this.metricsHistory.shift();
      }
      
      this.updateUI(metrics);
    }, 1000); // Update every second
  }

  /**
   * Stop monitoring system metrics
   */
  stopMonitoring(): void {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
      this.updateInterval = null;
    }
    this.isMonitoring = false;
    console.log('Stopped system monitoring');
  }

  /**
   * Collect simulated system metrics
   * In a real implementation, this would call an API
   */
  private collectMetrics(): SystemMetrics {
    // Simulate metrics collection
    const cpuUsage = Math.min(100, Math.max(0, 20 + Math.random() * 60));
    const memoryUsage = Math.min(100, Math.max(0, 30 + Math.random() * 50));
    const diskUsage = Math.min(100, Math.max(0, 40 + Math.random() * 40));
    const networkUsage = Math.min(100, Math.max(0, 10 + Math.random() * 30));
    const processCount = Math.floor(50 + Math.random() * 100);
    const temperature = Math.min(100, Math.max(30, 40 + Math.random() * 40));

    return {
      cpuUsage: parseFloat(cpuUsage.toFixed(2)),
      memoryUsage: parseFloat(memoryUsage.toFixed(2)),
      diskUsage: parseFloat(diskUsage.toFixed(2)),
      networkUsage: parseFloat(networkUsage.toFixed(2)),
      timestamp: new Date(),
      processCount,
      temperature
    };
  }

  /**
   * Update the UI with current metrics
   */
  private updateUI(metrics: SystemMetrics): void {
    // Update DOM elements with metrics
    const cpuElement = document.getElementById('cpu-usage');
    const memoryElement = document.getElementById('memory-usage');
    const diskElement = document.getElementById('disk-usage');
    const networkElement = document.getElementById('network-usage');
    const tempElement = document.getElementById('temperature');
    const processElement = document.getElementById('process-count');
    
    if (cpuElement) cpuElement.textContent = `${metrics.cpuUsage}%`;
    if (memoryElement) memoryElement.textContent = `${metrics.memoryUsage}%`;
    if (diskElement) diskElement.textContent = `${metrics.diskUsage}%`;
    if (networkElement) networkElement.textContent = `${metrics.networkUsage}%`;
    if (tempElement) tempElement.textContent = `${metrics.temperature}°C`;
    if (processElement) processElement.textContent = metrics.processCount.toString();
    
    // Update progress bars
    this.updateProgressBar('cpu-bar', metrics.cpuUsage);
    this.updateProgressBar('memory-bar', metrics.memoryUsage);
    this.updateProgressBar('disk-bar', metrics.diskUsage);
    this.updateProgressBar('network-bar', metrics.networkUsage);
  }

  /**
   * Update progress bar with value
   */
  private updateProgressBar(barId: string, value: number): void {
    const bar = document.getElementById(barId);
    if (bar) {
      bar.style.width = `${value}%`;
      
      // Change color based on value
      if (value > 80) {
        bar.className = 'progress-bar progress-danger';
      } else if (value > 60) {
        bar.className = 'progress-bar progress-warning';
      } else {
        bar.className = 'progress-bar progress-success';
      }
    }
  }

  /**
   * Perform system optimization
   */
  async optimizeSystem(): Promise<OptimizationResult> {
    console.log('Optimizing system...');
    
    // Simulate optimization process
    return new Promise((resolve) => {
      setTimeout(() => {
        const boost = Math.floor(5 + Math.random() * 15);
        resolve({
          status: 'success',
          message: `System optimized! Performance boost: ${boost}%`,
          performanceBoost: boost
        });
      }, 1500);
    });
  }

  /**
   * Get historical metrics
   */
  getHistoricalMetrics(): SystemMetrics[] {
    return [...this.metricsHistory];
  }

  /**
   * Calculate average metrics from history
   */
  getAverageMetrics(): SystemMetrics {
    if (this.metricsHistory.length === 0) {
      return this.getDefaultMetrics();
    }

    const sum = this.metricsHistory.reduce((acc, curr) => ({
      cpuUsage: acc.cpuUsage + curr.cpuUsage,
      memoryUsage: acc.memoryUsage + curr.memoryUsage,
      diskUsage: acc.diskUsage + curr.diskUsage,
      networkUsage: acc.networkUsage + curr.networkUsage,
      processCount: acc.processCount + curr.processCount,
      temperature: (acc.temperature || 0) + (curr.temperature || 0)
    }), {
      cpuUsage: 0,
      memoryUsage: 0,
      diskUsage: 0,
      networkUsage: 0,
      processCount: 0,
      temperature: 0
    });

    const count = this.metricsHistory.length;
    return {
      cpuUsage: parseFloat((sum.cpuUsage / count).toFixed(2)),
      memoryUsage: parseFloat((sum.memoryUsage / count).toFixed(2)),
      diskUsage: parseFloat((sum.diskUsage / count).toFixed(2)),
      networkUsage: parseFloat((sum.networkUsage / count).toFixed(2)),
      timestamp: new Date(),
      processCount: Math.floor(sum.processCount / count),
      temperature: parseFloat((sum.temperature / count).toFixed(2))
    };
  }

  private getDefaultMetrics(): SystemMetrics {
    return {
      cpuUsage: 0,
      memoryUsage: 0,
      diskUsage: 0,
      networkUsage: 0,
      timestamp: new Date(),
      processCount: 0,
      temperature: 0
    };
  }
}

// Web Component for the system monitor
class SystemMonitorElement extends HTMLElement {
  private monitor: WebSystemMonitor;

  constructor() {
    super();
    this.monitor = new WebSystemMonitor();
    this.init();
  }

  private init(): void {
    this.innerHTML = `
      <div class="system-monitor">
        <h3>System Monitor</h3>
        <div class="metrics-grid">
          <div class="metric-card">
            <h4>CPU Usage</h4>
            <div class="value" id="cpu-usage">0%</div>
            <div class="progress">
              <div class="progress-bar" id="cpu-bar" style="width: 0%"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <h4>Memory Usage</h4>
            <div class="value" id="memory-usage">0%</div>
            <div class="progress">
              <div class="progress-bar" id="memory-bar" style="width: 0%"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <h4>Disk Usage</h4>
            <div class="value" id="disk-usage">0%</div>
            <div class="progress">
              <div class="progress-bar" id="disk-bar" style="width: 0%"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <h4>Network Usage</h4>
            <div class="value" id="network-usage">0%</div>
            <div class="progress">
              <div class="progress-bar" id="network-bar" style="width: 0%"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <h4>Temperature</h4>
            <div class="value" id="temperature">0°C</div>
          </div>
          
          <div class="metric-card">
            <h4>Processes</h4>
            <div class="value" id="process-count">0</div>
          </div>
        </div>
        
        <div class="controls">
          <button id="start-btn">Start Monitoring</button>
          <button id="stop-btn">Stop Monitoring</button>
          <button id="optimize-btn">Optimize System</button>
        </div>
        
        <div class="status" id="status-message"></div>
      </div>
      
      <style>
        .system-monitor {
          font-family: Arial, sans-serif;
          padding: 20px;
          border: 1px solid #ddd;
          border-radius: 8px;
          background-color: #f9f9f9;
        }
        
        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          margin: 20px 0;
        }
        
        .metric-card {
          background: white;
          padding: 15px;
          border-radius: 5px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .value {
          font-size: 24px;
          font-weight: bold;
          margin: 10px 0;
        }
        
        .progress {
          height: 20px;
          background-color: #eee;
          border-radius: 10px;
          overflow: hidden;
        }
        
        .progress-bar {
          height: 100%;
          transition: width 0.3s ease;
        }
        
        .progress-success {
          background-color: #4CAF50;
        }
        
        .progress-warning {
          background-color: #FF9800;
        }
        
        .progress-danger {
          background-color: #F44336;
        }
        
        .controls {
          margin: 20px 0;
        }
        
        button {
          margin-right: 10px;
          padding: 10px 15px;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        
        button:hover {
          background-color: #0056b3;
        }
        
        .status {
          margin-top: 15px;
          padding: 10px;
          border-radius: 4px;
          background-color: #e9ecef;
        }
      </style>
    `;
    
    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    const startBtn = this.querySelector('#start-btn');
    const stopBtn = this.querySelector('#stop-btn');
    const optimizeBtn = this.querySelector('#optimize-btn');
    
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        this.monitor.startMonitoring();
        this.updateStatus('Monitoring started');
      });
    }
    
    if (stopBtn) {
      stopBtn.addEventListener('click', () => {
        this.monitor.stopMonitoring();
        this.updateStatus('Monitoring stopped');
      });
    }
    
    if (optimizeBtn) {
      optimizeBtn.addEventListener('click', async () => {
        const result = await this.monitor.optimizeSystem();
        this.updateStatus(result.message);
      });
    }
  }

  private updateStatus(message: string): void {
    const statusElement = this.querySelector('#status-message');
    if (statusElement) {
      statusElement.textContent = message;
    }
  }
}

// Register the custom element
customElements.define('system-monitor', SystemMonitorElement);

// Export for use in other modules
export { WebSystemMonitor, SystemMetrics, OptimizationResult };