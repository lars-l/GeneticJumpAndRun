from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("cython_floor_gen.pyx"),
)

setup(
    ext_modules=cythonize("cython_agent.pyx"),
)

setup(
    ext_modules=cythonize("cython_neural_network.pyx"),
    include_dirs=[numpy.get_include()]
)
