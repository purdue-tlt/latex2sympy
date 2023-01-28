#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

echo ''
echo "generating cpp parser..."
# generate cpp parser files
java -jar antlr-4.11.1-complete.jar -Dlanguage=Cpp -package latex2antlr -o parser/cpp LATEX.g4
echo "cpp parser generated"

echo ''
echo "compiling cpp parser..."
# compile cpp
mkdir parser/cpp/build
cd parser/cpp/build
conan install .. --build=antlr4-cppruntime
cmake .. -G "Unix Makefiles"
make
echo "cpp parser compiled"

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

echo ''
echo "generating python parser..."
# generate python parser files
java -jar antlr-4.11.1-complete.jar -Dlanguage=Python3 -o parser/python LATEX.g4
echo "python parser generated"

echo ''
echo "formatting python parser files..."
# format parser files
autopep8 --in-place parser/python/*.py
echo "python parser files formatted"

exit 0