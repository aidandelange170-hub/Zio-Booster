#!/usr/bin/env python3
"""
Build script for Rust performance features
"""
import subprocess
import sys
import os
from pathlib import Path

def build_rust_extension():
    """Build the Rust extension using maturin or cargo"""
    try:
        # Check if we have cargo installed
        result = subprocess.run(['cargo', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Cargo is not installed. Please install Rust first.")
            return False
        
        # Change to the rust_features directory
        original_dir = os.getcwd()
        os.chdir('/workspace/rust_features')
        
        # Build the Rust library
        print("Building Rust extension...")
        result = subprocess.run([
            'cargo', 'build', '--release'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Build failed: {result.stderr}")
            return False
        
        print("Rust extension built successfully!")
        return True
    except FileNotFoundError:
        print("Cargo not found. Please install Rust and Cargo.")
        return False
    except Exception as e:
        print(f"Error building Rust extension: {e}")
        return False
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    success = build_rust_extension()
    sys.exit(0 if success else 1)