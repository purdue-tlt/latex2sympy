from setuptools import setup

setup(
    version="1.7.0",
    name="latex2sympy",
    packages=[
        'latex2sympy',
        'latex2sympy.lib',
        'latex2sympy.lib.linux',
        'latex2sympy.lib.macOS',
        'latex2sympy.lib.macOS.arm64',
        'latex2sympy.lib.macOS.x86_64'],
    package_dir={
        'latex2sympy': 'src/latex2sympy',
        'latex2sympy.lib.linux': 'src/latex2sympy/lib/linux',
        'latex2sympy.lib.macOS.arm64': 'src/latex2sympy/lib/macOS/arm64',
        'latex2sympy.lib.macOS.x86_64': 'src/latex2sympy/lib/macOS/x86_64'
    },
    package_data={
        'latex2sympy': [],
        'latex2sympy.lib.linux': ['latex2antlrJson.so'],
        'latex2sympy.lib.macOS.arm64': ['latex2antlrJson.so'],
        'latex2sympy.lib.macOS.x86_64': ['latex2antlrJson.so']
    },
    install_requires=[
        'sympy==1.10.1'
    ]
)
