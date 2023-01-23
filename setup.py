from setuptools import setup, find_packages

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=find_packages(exclude=('tests')),
    py_modules=['asciimath_printer', 'latex2sympy'],
    install_requires=[
        'sympy==1.10.1',
        'antlr4-python3-runtime==4.11.1'
    ]
)
