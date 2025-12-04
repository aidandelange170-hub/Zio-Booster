#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib>
#include "emulator_core.h"
#include "performance_manager.h"
#include "fan_controller.h"

class NioEmulator {
private:
    EmulatorCore core;
    PerformanceManager perfMgr;
    FanController fanCtrl;
    bool isRunning;

public:
    NioEmulator() : isRunning(false) {}

    void initialize() {
        std::cout << "Initializing NIO Emulator..." << std::endl;
        std::cout << "High performance Android emulation system" << std::endl;
        std::cout << "Free forever - No lag guaranteed!" << std::endl;
        
        core.initialize();
        perfMgr.optimizeForPerformance();
        std::cout << "Fast installation and loading ready!" << std::endl;
    }

    void start() {
        isRunning = true;
        std::cout << "\nStarting NIO Emulator..." << std::endl;
        std::cout << "C++ technology eliminates all lag for best experience" << std::endl;
        
        // Start performance monitoring in background
        std::thread perfThread([this]() {
            while(isRunning) {
                perfMgr.monitorPerformance();
                std::this_thread::sleep_for(std::chrono::milliseconds(500));
            }
        });
        
        // Main emulation loop
        while(isRunning) {
            core.runEmulationCycle();
            std::this_thread::sleep_for(std::chrono::milliseconds(16)); // ~60 FPS
        }
        
        perfThread.join();
    }

    void activateFanControl() {
        std::cout << "\nActivating PC Fan Control..." << std::endl;
        fanCtrl.activateFan();
        std::cout << "Fan activated for optimal cooling during high-performance emulation!" << std::endl;
    }

    void stop() {
        isRunning = false;
        std::cout << "\nShutting down NIO Emulator..." << std::endl;
        std::cout << "Thanks for using our lag-free experience!" << std::endl;
    }
};

int main() {
    NioEmulator emulator;
    
    emulator.initialize();
    
    // Show fan activation option
    std::cout << "\nPress 'f' to activate PC fan for cooling (if available)" << std::endl;
    std::cout << "Press 'q' to quit emulator" << std::endl;
    
    char input;
    std::thread inputThread([&emulator, &input]() {
        while(true) {
            std::cin >> input;
            if(input == 'q' || input == 'Q') {
                emulator.stop();
                break;
            } else if(input == 'f' || input == 'F') {
                emulator.activateFanControl();
            }
        }
    });
    
    emulator.start();
    
    if(inputThread.joinable()) {
        inputThread.join();
    }
    
    return 0;
}