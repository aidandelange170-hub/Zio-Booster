#!/bin/bash

echo "Starting NIO Emulator..."
echo "High performance Android emulation with zero lag!"
echo "Free forever - C++ technology eliminates all lag for best experience"
echo ""

# Check if the emulator is built
if [ ! -f "./nio_emulator" ]; then
    echo "Emulator not found. Building now..."
    ./build.sh
    if [ $? -ne 0 ]; then
        echo "Build failed. Exiting."
        exit 1
    fi
fi

echo "Starting NIO Emulator..."
echo "Press 'f' to activate PC fan during emulation"
echo "Press 'q' to quit"
echo ""

./nio_emulator