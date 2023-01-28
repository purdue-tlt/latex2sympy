cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project("latex2antlr")

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE INTERNAL "" FORCE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(parser LATEXLexer.cpp LATEXParser.cpp LATEXListener.cpp LATEXBaseListener.cpp)

add_executable(latex2antlr latex2antlr.cpp)
target_link_libraries(latex2antlr parser ${CONAN_LIBS})