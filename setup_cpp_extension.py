from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

# Define the extension module
cpp_extension = Extension(
    name="cpp_performance",
    sources=[
        "cpp_performance_wrapper.pyx",
        "cpp_performance_impl.cpp"  # Renamed to avoid conflicts
    ],
    include_dirs=["."],  # Include current directory for header files
    language="c++",
    extra_compile_args=["-std=c++11", "-O3"],
    extra_link_args=["-std=c++11"],
)

setup(
    ext_modules=cythonize([cpp_extension]),
    include_dirs=[numpy.get_include()]
)