from setuptools import find_packages
from skbuild import setup

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=find_packages(include=['latex2sympy', 'latex2sympy.*']),
    package_dir={'': 'src'},
    cmake_install_dir='src/latex2sympy'
)
