from setuptools import find_packages
from skbuild import setup

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=find_packages(include=['latex2sympy', 'latex2sympy.*']),
    cmake_install_dir='latex2sympy'
)
