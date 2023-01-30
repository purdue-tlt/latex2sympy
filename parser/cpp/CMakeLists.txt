cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project("latex2antlrJson")

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE INTERNAL "" FORCE)

include(FetchContent)
FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG        v2.10.3
	GIT_SHALLOW    TRUE
)

FetchContent_MakeAvailable(pybind11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(latex2antlr LATEXLexer.cpp LATEXParser.cpp LATEXListener.cpp LATEXBaseListener.cpp)

pybind11_add_module(latex2antlrJson latex2antlrJson.cpp)
target_link_libraries(latex2antlrJson PUBLIC latex2antlr ${CONAN_LIBS})
target_compile_features(latex2antlrJson PUBLIC cxx_std_17)
set_target_properties(latex2antlrJson PROPERTIES SUFFIX ".so")
