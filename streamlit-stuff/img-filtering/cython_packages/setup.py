from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    ext_modules = cythonize("filter1.pyx")
)
setup(
    name = 'medianfilter',
    ext_modules = cythonize("medianfilter.pyx"),
    include_dirs=[np.get_include()]
)
setup(
    name="smooth",
    ext_modules=cythonize("smooth.pyx")
)