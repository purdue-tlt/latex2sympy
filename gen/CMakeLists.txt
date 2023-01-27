cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project("latex2sympy")

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE INTERNAL "" FORCE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(gen PSLexer.cpp PSParser.cpp PSListener.cpp PSBaseListener.cpp)

add_executable(latex2sympy latex2sympy.cpp)
target_link_libraries(latex2sympy gen ${CONAN_LIBS})