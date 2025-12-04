#ifndef FAN_CONTROLLER_H
#define FAN_CONTROLLER_H

#include <iostream>
#include <thread>
#include <chrono>

class FanController {
private:
    bool fanActive;
    int fanSpeed;

public:
    FanController() : fanActive(false), fanSpeed(0) {}
    
    void activateFan() {
        std::cout << "PC Fan activation system engaged!" << std::endl;
        std::cout << "Cooling system activated for high-performance emulation!" << std::endl;
        
        // Simulate fan activation
        fanActive = true;
        fanSpeed = 75; // Set to high speed for performance cooling
        
        std::cout << "Fan speed set to " << fanSpeed << "%" << std::endl;
        std::cout << "Optimal cooling for lag-free experience!" << std::endl;
    }
    
    void setFanSpeed(int speed) {
        if(speed >= 0 && speed <= 100) {
            fanSpeed = speed;
            if(fanActive) {
                std::cout << "Fan speed adjusted to " << fanSpeed << "%" << std::endl;
            }
        }
    }
    
    bool isFanActive() const {
        return fanActive;
    }
    
    void deactivateFan() {
        fanActive = false;
        fanSpeed = 0;
        std::cout << "Fan deactivated" << std::endl;
    }
};

#endif // FAN_CONTROLLER_H