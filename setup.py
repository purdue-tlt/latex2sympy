from setuptools import setup, find_packages

setup(
    version="1.5.4",
    name="latex2sympy",
    packages=find_packages(exclude=('tests')),
    py_modules=['asciimath_printer', 'latex2sympy'],
    install_requires=[
        'sympy>=1.4',
        'antlr4-python3-runtime>=4.7.2'
    ]
)
