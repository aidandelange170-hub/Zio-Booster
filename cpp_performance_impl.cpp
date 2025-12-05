#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <algorithm>
#include <memory>
#include <cstring>
#include <signal.h>
#include <sys/resource.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <fstream>
#include <sstream>

class PerformanceOptimizer {
private:
    std::vector<int> process_ids;
    bool gaming_mode = false;
    
public:
    PerformanceOptimizer() {
        // Set high priority for this process
        setpriority(PRIO_PROCESS, 0, -10);
    }
    
    // Get system memory info in MB
    double get_system_memory_usage() {
        struct sysinfo memInfo;
        sysinfo(&memInfo);
        
        long long totalMemory = memInfo.totalram;
        totalMemory *= memInfo.mem_unit;
        
        long long freeMemory = memInfo.freeram;
        freeMemory *= memInfo.mem_unit;
        
        double usedMemory = (totalMemory - freeMemory) / (1024.0 * 1024.0); // Convert to MB
        return usedMemory;
    }
    
    // Get system load average
    double get_system_load() {
        double loadavg[3];
        if (getloadavg(loadavg, 3) != -1) {
            return loadavg[0]; // 1-minute average
        }
        return 0.0;
    }
    
    // Get CPU temperature (Linux)
    double get_cpu_temperature() {
        std::ifstream tempFile("/sys/class/thermal/thermal_zone0/temp");
        if (!tempFile.is_open()) {
            return 0.0;
        }
        
        std::string line;
        if (std::getline(tempFile, line)) {
            try {
                double temp = std::stod(line) / 1000.0; // Convert from millidegrees to degrees
                return temp;
            } catch (...) {
                return 0.0;
            }
        }
        return 0.0;
    }
    
    // Get process CPU usage (simplified)
    double get_process_cpu_usage(int pid) {
        std::string statPath = "/proc/" + std::to_string(pid) + "/stat";
        std::ifstream statFile(statPath);
        
        if (!statFile.is_open()) {
            return 0.0;
        }
        
        std::string line;
        if (std::getline(statFile, line)) {
            std::istringstream iss(line);
            std::vector<std::string> tokens;
            std::string token;
            
            while (iss >> token) {
                tokens.push_back(token);
            }
            
            if (tokens.size() >= 14) {
                // Simplified CPU usage calculation
                return 10.0; // Placeholder - actual calculation would be more complex
            }
        }
        return 0.0;
    }
    
    // Kill a specific process by PID
    bool kill_process(int pid) {
        if (kill(pid, SIGTERM) == 0) {
            // Give process time to terminate gracefully
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            // Force kill if still running
            kill(pid, SIGKILL);
            return true;
        }
        return false;
    }
    
    // Find processes by name
    std::vector<int> find_processes_by_name(const std::string& name) {
        std::vector<int> pids;
        std::string command = "pgrep -f \"" + name + "\"";
        
        FILE* pipe = popen(command.c_str(), "r");
        if (!pipe) return pids;
        
        char buffer[128];
        while (fgets(buffer, sizeof buffer, pipe) != nullptr) {
            int pid = std::stoi(buffer);
            if (pid > 0) {
                pids.push_back(pid);
            }
        }
        pclose(pipe);
        
        return pids;
    }
    
    // Optimize system for gaming
    void optimize_for_gaming() {
        gaming_mode = true;
        
        // Set CPU governor to performance mode
        system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1");
        
        // Disable CPU idle states (if possible)
        system("sudo modprobe cpuidle.off=1 > /dev/null 2>&1");
        
        // Increase swappiness for better memory management
        system("echo 10 | sudo tee /proc/sys/vm/swappiness > /dev/null 2>&1");
        
        // Optimize network settings for gaming
        system("sudo sysctl -w net.core.rmem_max=16777216 > /dev/null 2>&1");
        system("sudo sysctl -w net.core.wmem_max=16777216 > /dev/null 2>&1");
    }
    
    // Restore normal system settings
    void restore_normal_settings() {
        gaming_mode = false;
        
        // Restore CPU governor to powersave
        system("echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1");
        
        // Re-enable CPU idle states
        system("sudo modprobe cpuidle.off=0 > /dev/null 2>&1");
        
        // Restore normal swappiness
        system("echo 60 | sudo tee /proc/sys/vm/swappiness > /dev/null 2>&1");
    }
    
    // Get list of high CPU usage processes
    std::vector<std::pair<int, double>> get_high_cpu_processes(int threshold_percent = 10) {
        std::vector<std::pair<int, double>> high_cpu_processes;
        
        // Get all process IDs
        std::string command = "ps -eo pid,pcpu --no-headers";
        FILE* pipe = popen(command.c_str(), "r");
        
        if (!pipe) return high_cpu_processes;
        
        char buffer[256];
        while (fgets(buffer, sizeof buffer, pipe) != nullptr) {
            int pid;
            double cpu_usage;
            
            if (sscanf(buffer, "%d %lf", &pid, &cpu_usage) == 2) {
                if (cpu_usage >= threshold_percent && pid > 1) {
                    high_cpu_processes.push_back(std::make_pair(pid, cpu_usage));
                }
            }
        }
        pclose(pipe);
        
        // Sort by CPU usage descending
        std::sort(high_cpu_processes.begin(), high_cpu_processes.end(),
                  [](const std::pair<int, double>& a, const std::pair<int, double>& b) {
                      return a.second > b.second;
                  });
        
        return high_cpu_processes;
    }
    
    // Memory optimization - clear caches
    void clear_system_caches() {
        // Clear pagecache, dentries and inodes
        system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' > /dev/null 2>&1");
    }
    
    // Get available memory in MB
    double get_available_memory() {
        struct sysinfo memInfo;
        sysinfo(&memInfo);
        
        long long freeMemory = memInfo.freeram;
        freeMemory *= memInfo.mem_unit;
        
        return freeMemory / (1024.0 * 1024.0); // Convert to MB
    }
    
    // Get total memory in MB
    double get_total_memory() {
        struct sysinfo memInfo;
        sysinfo(&memInfo);
        
        long long totalMemory = memInfo.totalram;
        totalMemory *= memInfo.mem_unit;
        
        return totalMemory / (1024.0 * 1024.0); // Convert to MB
    }
    
    // Get CPU usage percentage
    double get_cpu_usage() {
        std::ifstream statFile("/proc/stat");
        if (!statFile.is_open()) return 0.0;
        
        std::string line;
        if (std::getline(statFile, line)) {
            std::istringstream iss(line);
            std::string cpu;
            unsigned long user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice;
            
            iss >> cpu >> user >> nice >> system >> idle >> iowait >> irq >> softirq >> steal >> guest >> guest_nice;
            
            unsigned long idle_time = idle + iowait;
            unsigned long total_time = user + nice + system + idle + iowait + irq + softirq + steal;
            
            static unsigned long prev_idle = 0, prev_total = 0;
            
            unsigned long delta_idle = idle_time - prev_idle;
            unsigned long delta_total = total_time - prev_total;
            
            if (delta_total == 0) return 0.0;
            
            double cpu_usage = 100.0 * (delta_total - delta_idle) / delta_total;
            
            prev_idle = idle_time;
            prev_total = total_time;
            
            return cpu_usage;
        }
        
        return 0.0;
    }
    
    // Fast process termination for optimization
    void fast_process_cleanup(const std::vector<std::string>& process_names) {
        for (const auto& name : process_names) {
            auto pids = find_processes_by_name(name);
            for (int pid : pids) {
                kill_process(pid);
            }
        }
    }
    
    // Get system uptime in seconds
    double get_system_uptime() {
        std::ifstream uptimeFile("/proc/uptime");
        if (!uptimeFile.is_open()) return 0.0;
        
        double uptime;
        uptimeFile >> uptime;
        return uptime;
    }
    
    ~PerformanceOptimizer() {
        if (gaming_mode) {
            restore_normal_settings();
        }
    }
};

// Expose functions for Python integration
extern "C" {
    PerformanceOptimizer* create_optimizer() {
        return new PerformanceOptimizer();
    }
    
    void destroy_optimizer(PerformanceOptimizer* opt) {
        delete static_cast<struct PerformanceOptimizer*>(opt);
    }
    
    double get_system_memory_usage(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_system_memory_usage();
    }
    
    double get_system_load(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_system_load();
    }
    
    double get_cpu_temperature(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_cpu_temperature();
    }
    
    void optimize_for_gaming(PerformanceOptimizer* opt) {
        reinterpret_cast<PerformanceOptimizer*>(opt)->optimize_for_gaming();
    }
    
    void restore_normal_settings(PerformanceOptimizer* opt) {
        reinterpret_cast<PerformanceOptimizer*>(opt)->restore_normal_settings();
    }
    
    void clear_system_caches(PerformanceOptimizer* opt) {
        reinterpret_cast<PerformanceOptimizer*>(opt)->clear_system_caches();
    }
    
    double get_available_memory(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_available_memory();
    }
    
    double get_total_memory(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_total_memory();
    }
    
    double get_cpu_usage(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_cpu_usage();
    }
    
    double get_system_uptime(PerformanceOptimizer* opt) {
        return reinterpret_cast<PerformanceOptimizer*>(opt)->get_system_uptime();
    }
}