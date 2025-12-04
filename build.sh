#!/bin/bash

echo "Building NIO Emulator..."
echo "High performance Android emulator with zero lag guarantee!"

# Compile the emulator
g++ -std=c++11 -o nio_emulator nio_emulator.cpp

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Run './nio_emulator' to start the emulator"
    echo "Press 'f' during emulation to activate PC fan"
    echo "Press 'q' to quit the emulator"
else
    echo "Build failed!"
    exit 1
fi