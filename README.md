# latex2sympy

latex2sympy parses LaTeX math expressions and converts them into the equivalent SymPy form.

## Installation

```sh
sh scripts/setup.sh
```

If you plan to edit the parser grammar ensure you have java installed on your machine.

## Compiling

The script below should be run **every time the file `LATEX.g4` or `src/latex2sympy/latex2antlrJson.cpp` are modified**.

```sh
sh scripts/compile.sh
```

Pre-compiled parsers are stored in `src/latex2sympy/lib`. **`src/latex2sympy/lib/linux` contains the parser used in azure functions** (see below).

`compile.sh` will only compile for the current system.

### macOS arm64
Run `compile.sh` on an M1 Mac

### macOS x86_64
Run `compile.sh` on an Intel Mac, or inside a "Rosetta" Terminal on an M1 Mac

### azure-functions-python / Linux

1. Use docker to get the azure function image from https://hub.docker.com/_/microsoft-azure-functions-python, e.g. `mcr.microsoft.com/azure-functions/python:4-python3.9`
1. Start a new instance and open its terminal
1. Install git, build-essentials, default-jre
	```sh
	apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y git && \
	apt-get install -y build-essential && \
	apt-get install -y default-jre

	```
1. clone latex2sympy with git and compile
	```sh
	# make a dir for the repo
	cd /
	mkdir git
	cd git
	# clone repo
	git clone https://github.com/purdue-tlt/latex2sympy.git
	cd latex2sympy
	# setup venv
	sh scripts/setup.sh
	# compile
	sh scripts/compile.sh
	```
1. copy `latex2antlrJson.so` from container
	```sh
	docker cp container_name:/git/latex2sympy/src/latex2sympy/lib/linux/latex2antlrJson.so ~/git/purdue/github/latex2sympy/src/latex2sympy/lib/linux/
	```
1. commit the updated file

## Testing

```sh
sh scripts/test.sh
```

## Usage

In Python:

```python
from latex2sympy.latex2sympy import process_sympy

process_sympy("\\frac{d}{dx} x^{2}")
# => "diff(x**(2), x)"
```

To modify parser grammar, view the existing structure in `LATEX.g4`.

To modify the action associated with each grammar, look into `src/latex2sympy/latex2antlrJson.cpp` and `src/latex2sympy/latex2sympy.py`.
