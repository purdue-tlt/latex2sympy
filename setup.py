from skbuild import setup

setup(
    version="1.6.1",
    name="latex2sympy",
    packages=['latex2sympy', 'latex2sympy.parser', 'latex2sympy.parser.python'],
    package_dir={'': 'src'},
    cmake_install_dir='src/latex2sympy'
)
