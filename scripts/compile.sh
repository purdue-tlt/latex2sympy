#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

echo ''
echo "generate and compile cpp parser..."
mkdir build
cd build
conan install .. --build missing
cmake .. -G "Unix Makefiles"
make
echo "cpp parser generated and compiled"

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

# copy compiled cpp parser to root src dir
cp build/lib/latex2antlrJson.so src/latex2sympy/

echo ''
echo "generating python parser..."
java -jar antlr-4.11.1-complete.jar -Dlanguage=Python3 -o src/latex2sympy/parser/python -no-listener LATEX.g4
echo "python parser generated"

echo ''
echo "activating venv..."
if test -f .env/bin/activate
then source .env/bin/activate && echo "venv activate (bin)"
elif test -f .env/Scripts/activate
then source .env/Scripts/activate && echo "venv activated (Scripts)"
else exit 1
fi

echo ''
echo "formatting python parser files..."
autopep8 --in-place src/latex2sympy/parser/python/*.py
echo "python parser files formatted"

exit 0