from setuptools import setup, find_packages

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=find_packages(include=['latex2sympy', 'latex2sympy.*']),
    install_requires=[
        'sympy==1.10.1',
        'antlr4-python3-runtime==4.11.1'
    ],
    package_data={
        '': ['latex2antlrJson.so']
    }
)
