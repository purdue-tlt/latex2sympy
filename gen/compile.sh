mkdir build
cd build
conan install .. --build=antlr4-cppruntime
cmake .. -G "Unix Makefiles"
make