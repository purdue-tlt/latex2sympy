from setuptools import setup

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=[
        'latex2sympy',
        'latex2sympy.parser',
        'latex2sympy.parser.linux',
        'latex2sympy.parser.macOS',
        'latex2sympy.parser.macOS.arm64',
        'latex2sympy.parser.macOS.x86_64',
        'latex2sympy.parser.windows'],
    package_dir={
        'latex2sympy': 'src/latex2sympy',
        'latex2sympy.parser.linux': 'src/latex2sympy/parser/linux',
        'latex2sympy.parser.macOS.arm64': 'src/latex2sympy/parser/macOS/arm64',
        'latex2sympy.parser.macOS.x86_64': 'src/latex2sympy/parser/macOS/x86_64',
        'latex2sympy.parser.macOS.windows': 'src/latex2sympy/parser/windows'
    },
    package_data={
        'latex2sympy': [],
        'latex2sympy.parser.linux': ['latex2antlrJson.so'],
        'latex2sympy.parser.macOS.arm64': ['latex2antlrJson.so'],
        'latex2sympy.parser.macOS.x86_64': ['latex2antlrJson.so'],
        'latex2sympy.parser.windows': ['latex2antlrJson.so']
    },
    install_requires=[
        'sympy==1.10.1'
    ]
)
