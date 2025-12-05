package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
	"sync"
	"runtime"
)

// SystemMetrics holds system performance metrics
type SystemMetrics struct {
	CPUUsage     float64   `json:"cpu_usage"`
	MemoryUsage  float64   `json:"memory_usage"`
	DiskUsage    float64   `json:"disk_usage"`
	NetworkUsage float64   `json:"network_usage"`
	Timestamp    time.Time `json:"timestamp"`
	ProcessCount int       `json:"process_count"`
}

// MonitorResult holds the result of a monitoring operation
type MonitorResult struct {
	Metrics SystemMetrics `json:"metrics"`
	Error   string        `json:"error,omitempty"`
}

// ConcurrentMonitor performs concurrent system monitoring
type ConcurrentMonitor struct {
	mu       sync.Mutex
	metrics  []SystemMetrics
}

// NewConcurrentMonitor creates a new instance of ConcurrentMonitor
func NewConcurrentMonitor() *ConcurrentMonitor {
	return &ConcurrentMonitor{
		metrics: make([]SystemMetrics, 0),
	}
}

// MonitorSystem simulates concurrent system monitoring
func (cm *ConcurrentMonitor) MonitorSystem() SystemMetrics {
	// In a real implementation, this would collect actual system metrics
	// For this example, we'll simulate metrics collection
	cpuUsage := float64(runtime.NumGoroutine()) * 5.0
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	memoryUsage := float64(m.Alloc) / 1000000.0 * 0.1
	diskUsage := 30.0 + float64(time.Now().UnixNano()%20)
	networkUsage := 10.0 + float64(time.Now().UnixNano()%15)
	
	return SystemMetrics{
		CPUUsage:     cpuUsage,
		MemoryUsage:  memoryUsage,
		DiskUsage:    diskUsage,
		NetworkUsage: networkUsage,
		Timestamp:    time.Now(),
		ProcessCount: runtime.NumGoroutine() * 2,
	}
}

// CollectMetrics concurrently collects metrics from multiple sources
func (cm *ConcurrentMonitor) CollectMetrics(concurrencyLevel int) []MonitorResult {
	var wg sync.WaitGroup
	results := make(chan MonitorResult, concurrencyLevel)
	
	for i := 0; i < concurrencyLevel; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			
			// Simulate collecting metrics with potential errors
			if id%10 == 0 { // Simulate occasional errors
				results <- MonitorResult{
					Error: "Simulated collection error",
				}
			} else {
				metrics := cm.MonitorSystem()
				results <- MonitorResult{
					Metrics: metrics,
				}
			}
		}(i)
	}
	
	// Close the results channel when all goroutines are done
	go func() {
		wg.Wait()
		close(results)
	}()
	
	// Collect results
	var monitorResults []MonitorResult
	for result := range results {
		monitorResults = append(monitorResults, result)
	}
	
	return monitorResults
}

// CalculateAverageMetrics calculates average metrics from collected results
func (cm *ConcurrentMonitor) CalculateAverageMetrics(results []MonitorResult) SystemMetrics {
	var totalCPU, totalMemory, totalDisk, totalNetwork float64
	var validCount int
	
	for _, result := range results {
		if result.Error == "" {
			totalCPU += result.Metrics.CPUUsage
			totalMemory += result.Metrics.MemoryUsage
			totalDisk += result.Metrics.DiskUsage
			totalNetwork += result.Metrics.NetworkUsage
			validCount++
		}
	}
	
	if validCount == 0 {
		return SystemMetrics{}
	}
	
	return SystemMetrics{
		CPUUsage:     totalCPU / float64(validCount),
		MemoryUsage:  totalMemory / float64(validCount),
		DiskUsage:    totalDisk / float64(validCount),
		NetworkUsage: totalNetwork / float64(validCount),
		Timestamp:    time.Now(),
		ProcessCount: 0, // Not averaged
	}
}

// StartHTTPServer starts an HTTP server to expose metrics
func (cm *ConcurrentMonitor) StartHTTPServer(port string) {
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		metrics := cm.MonitorSystem()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(metrics)
	})
	
	http.HandleFunc("/concurrent-metrics", func(w http.ResponseWriter, r *http.Request) {
		concurrencyLevel := 10
		if r.URL.Query().Get("concurrency") != "" {
			// In a real app, parse the query parameter properly
		}
		
		results := cm.CollectMetrics(concurrencyLevel)
		avgMetrics := cm.CalculateAverageMetrics(results)
		
		response := map[string]interface{}{
			"average_metrics": avgMetrics,
			"total_results":   len(results),
			"timestamp":       time.Now(),
		}
		
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})
	
	fmt.Printf("Starting HTTP server on :%s\n", port)
	http.ListenAndServe(":"+port, nil)
}

func main() {
	monitor := NewConcurrentMonitor()
	
	// Example usage
	fmt.Println("Collecting metrics concurrently...")
	results := monitor.CollectMetrics(5)
	avgMetrics := monitor.CalculateAverageMetrics(results)
	
	fmt.Printf("Average metrics: %+v\n", avgMetrics)
	
	// Start HTTP server (uncomment to run)
	// monitor.StartHTTPServer("8080")
}