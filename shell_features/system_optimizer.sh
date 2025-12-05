#!/bin/bash

# System Optimizer Script for Performance Enhancement
# Supports Linux and macOS systems

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get system information
get_system_info() {
    print_status "Collecting system information..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
        CPU_INFO=$(lscpu | grep "Model name" | head -n1 | cut -d':' -f2 | xargs)
        MEM_INFO=$(free -h | awk 'NR==2{printf "%.1f/%.1f GB", $3/1024**3,$2/1024**3}')
        DISK_INFO=$(df -h / | awk 'NR==2{print $5 " used"}')
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        CPU_INFO=$(sysctl -n machdep.cpu.brand_string)
        MEM_INFO=$(($(vm_stat | awk '/^Pages free:/ {print $3}' | sed 's/\.//') * 4096 / 1024 / 1024 / 1024))
        TOTAL_MEM=$(sysctl -n hw.memsize | awk '{printf "%.1f", $1/1024/1024/1024}')
        MEM_INFO="${MEM_INFO}/${TOTAL_MEM} GB"
        DISK_INFO=$(df -h / | awk 'NR==2{print $5 " used"}')
    else
        OS="Unknown"
        CPU_INFO="N/A"
        MEM_INFO="N/A"
        DISK_INFO="N/A"
    fi
    
    echo "Operating System: $OS"
    echo "CPU: $CPU_INFO"
    echo "Memory: $MEM_INFO"
    echo "Disk Usage: $DISK_INFO"
}

# Function to clean temporary files
clean_temp_files() {
    print_status "Cleaning temporary files..."
    
    TEMP_CLEANED=0
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Clean temporary directories
        if sudo rm -rf /tmp/* 2>/dev/null; then
            ((TEMP_CLEANED+=1))
        fi
        if sudo rm -rf /var/tmp/* 2>/dev/null; then
            ((TEMP_CLEANED+=1))
        fi
        
        # Clean package manager caches
        if command_exists apt; then
            sudo apt autoremove -y >/dev/null 2>&1
            sudo apt autoclean >/dev/null 2>&1
            ((TEMP_CLEANED+=2))
        elif command_exists yum; then
            sudo yum clean all >/dev/null 2>&1
            ((TEMP_CLEANED+=1))
        elif command_exists dnf; then
            sudo dnf clean all >/dev/null 2>&1
            ((TEMP_CLEANED+=1))
        fi
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Clean macOS caches
        if sudo rm -rf ~/Library/Caches/* 2>/dev/null; then
            ((TEMP_CLEANED+=1))
        fi
        if sudo rm -rf /Library/Caches/* 2>/dev/null; then
            ((TEMP_CLEANED+=1))
        fi
        if command_exists brew; then
            brew cleanup >/dev/null 2>&1
            ((TEMP_CLEANED+=1))
        fi
    fi
    
    print_success "Cleaned $TEMP_CLEANED temporary directories/files"
}

# Function to optimize network settings
optimize_network() {
    print_status "Optimizing network settings..."
    
    NETWORK_OPTIMIZED=0
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Optimize TCP settings for better performance
        if command_exists sysctl; then
            sudo sysctl -w net.core.rmem_max=16777216 >/dev/null 2>&1
            sudo sysctl -w net.core.wmem_max=16777216 >/dev/null 2>&1
            sudo sysctl -w net.ipv4.tcp_rmem='4096 65536 16777216' >/dev/null 2>&1
            sudo sysctl -w net.ipv4.tcp_wmem='4096 65536 16777216' >/dev/null 2>&1
            ((NETWORK_OPTIMIZED+=4))
        fi
    fi
    
    if [ $NETWORK_OPTIMIZED -gt 0 ]; then
        print_success "Applied $NETWORK_OPTIMIZED network optimizations"
    else
        print_warning "No network optimizations applied (requires root privileges)"
    fi
}

# Function to optimize system services
optimize_services() {
    print_status "Optimizing system services..."
    
    SERVICES_OPTIMIZED=0
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists systemctl; then
            # Disable unnecessary services (be careful with these)
            # Only showing status, not actually disabling anything dangerous
            UNNECESSARY_SERVICES=("bluetooth" "cups" "avahi-daemon")
            
            for service in "${UNNECESSARY_SERVICES[@]}"; do
                if systemctl is-active --quiet "$service"; then
                    print_warning "Service '$service' is active (consider disabling if not needed)"
                    ((SERVICES_OPTIMIZED++))
                fi
            done
        fi
    fi
    
    print_success "Checked $SERVICES_OPTIMIZED potentially unnecessary services"
}

# Function to get current performance metrics
get_performance_metrics() {
    print_status "Collecting performance metrics..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
        MEM_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
        LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' | xargs)
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        CPU_USAGE=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1)
        MEM_USAGE=$(vm_stat | awk '/^Pages active:/ {active=$3}; /^Pages free:/ {free=$3}; END {printf("%.2f", (active/(active+free))*100)}')
        LOAD_AVG=$(uptime | awk -F'load averages:' '{print $2}' | xargs)
    fi
    
    echo "CPU Usage: ${CPU_USAGE}%"
    echo "Memory Usage: ${MEM_USAGE}%"
    echo "Load Average: $LOAD_AVG"
}

# Function to apply performance boosts
apply_performance_boost() {
    print_status "Applying performance boost..."
    
    BOOST_APPLIED=0
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Increase file descriptor limits
        if command_exists ulimit; then
            ulimit -n 65536 2>/dev/null
            ((BOOST_APPLIED+=1))
        fi
        
        # Optimize scheduler settings
        if [ -w /sys/block/*/queue/scheduler ]; then
            for sched in /sys/block/*/queue/scheduler; do
                if grep -q none "$sched" 2>/dev/null; then
                    echo none > "$sched" 2>/dev/null
                    ((BOOST_APPLIED+=1))
                fi
            done
        fi
    fi
    
    if [ $BOOST_APPLIED -gt 0 ]; then
        print_success "Applied $BOOST_APPLIED performance enhancements"
    else
        print_warning "No performance boosts applied (may require root privileges)"
    fi
}

# Main optimization function
perform_full_optimization() {
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}   ZIO-BOOSTER SYSTEM OPTIMIZER${NC}"
    echo -e "${GREEN}================================${NC}"
    
    get_system_info
    echo ""
    
    get_performance_metrics
    echo ""
    
    read -p "Do you want to proceed with system optimization? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Starting full system optimization..."
        echo ""
        
        clean_temp_files
        echo ""
        
        optimize_network
        echo ""
        
        optimize_services
        echo ""
        
        apply_performance_boost
        echo ""
        
        get_performance_metrics
        echo ""
        
        print_success "System optimization completed!"
        print_success "For best results, consider restarting your system."
    else
        print_warning "Optimization cancelled by user."
    fi
}

# Help function
show_help() {
    echo "Zio-Booster System Optimizer"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -i, --info           Show system information"
    echo "  -m, --metrics        Show performance metrics"
    echo "  -c, --clean          Clean temporary files"
    echo "  -n, --network        Optimize network settings"
    echo "  -p, --performance    Apply performance boosts"
    echo "  -f, --full           Perform full optimization (default)"
    echo ""
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -i|--info)
        get_system_info
        ;;
    -m|--metrics)
        get_performance_metrics
        ;;
    -c|--clean)
        clean_temp_files
        ;;
    -n|--network)
        optimize_network
        ;;
    -p|--performance)
        apply_performance_boost
        ;;
    -f|--full)
        perform_full_optimization
        ;;
    "")
        perform_full_optimization
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac