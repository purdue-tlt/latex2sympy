#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

echo ''
echo "generating cpp parser..."
# generate cpp parser files
java -jar antlr-4.11.1-complete.jar -Dlanguage=Cpp -package latex2antlr -o latex2sympy/parser/cpp -no-listener LATEX.g4
echo "cpp parser generated"

echo ''
echo "compiling cpp parser..."
# compile cpp
mkdir latex2sympy/parser/cpp/build
cd latex2sympy/parser/cpp/build
conan install .. --build=antlr4-cppruntime --build=jsoncpp
cmake .. -G "Unix Makefiles"
make
make install
echo "cpp parser compiled"

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

# copy compiled cpp parser to root src dir
cp latex2sympy/parser/cpp/build/lib/latex2antlrJson.so latex2sympy/

echo ''
echo "generating python parser..."
# generate python parser files
java -jar antlr-4.11.1-complete.jar -Dlanguage=Python3 -o latex2sympy/parser/python -no-listener LATEX.g4
echo "python parser generated"

# Activate virtual environment
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
# format parser files
autopep8 --in-place latex2sympy/parser/python/*.py
echo "python parser files formatted"

exit 0