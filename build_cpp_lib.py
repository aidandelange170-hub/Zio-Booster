import os
import subprocess
import platform

def build_cpp_library():
    """Build the C++ performance library as a shared object"""
    
    # Determine the appropriate compiler flags based on the platform
    if platform.system() == "Linux":
        compile_cmd = [
            "g++", "-O3", "-fPIC", "-shared",
            "-o", "libcpp_performance.so",
            "cpp_performance_impl.cpp"
        ]
    elif platform.system() == "Darwin":  # macOS
        compile_cmd = [
            "g++", "-O3", "-fPIC", "-shared",
            "-o", "libcpp_performance.dylib",
            "cpp_performance_impl.cpp"
        ]
    else:
        print(f"Unsupported platform: {platform.system()}")
        return False
    
    try:
        result = subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        print("C++ library built successfully!")
        print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building C++ library: {e}")
        print("Error output:", e.stderr)
        return False

if __name__ == "__main__":
    build_cpp_library()