from setuptools import setup

setup(
    version="1.11.2",
    name="latex2sympy",
    packages=[
        'latex2sympy',
        'latex2sympy.lib',
        'latex2sympy.lib.linux',
        'latex2sympy.lib.macOS',
        'latex2sympy.units',
        'latex2sympy.units.unit_aliases',
        'latex2sympy.utils',
    ],
    package_dir={
        'latex2sympy': 'src/latex2sympy',
        'latex2sympy.lib.linux': 'src/latex2sympy/lib/linux',
        'latex2sympy.lib.macOS': 'src/latex2sympy/lib/macOS',
        'latex2sympy.units': 'src/latex2sympy/units',
        'latex2sympy.units.unit_aliases': 'src/latex2sympy/units/unit_aliases',
        'latex2sympy.utils': 'src/latex2sympy/utils',
    },
    package_data={
        'latex2sympy': [],
        'latex2sympy.lib.linux': ['latex2antlrJson.so'],
        'latex2sympy.lib.macOS': ['latex2antlrJson.so'],
        'latex2sympy.units': [],
        'latex2sympy.units.unit_aliases': [],
        'latex2sympy.utils': [],
    },
    install_requires=['sympy==1.12'],
)
