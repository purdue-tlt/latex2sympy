cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

SET(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ version selection")
SET(CMAKE_CXX_STANDARD_REQUIRED ON)

project("latex2antlrJson")

# install pybind11
# ----------------------------------------------------------------------------------------

include(FetchContent)
FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG        v2.10.3
	GIT_SHALLOW    TRUE
)
FetchContent_MakeAvailable(pybind11)

# install conan requirements
# ----------------------------------------------------------------------------------------

if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
	message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
	file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/0.18.1/conan.cmake"
				"${CMAKE_BINARY_DIR}/conan.cmake"
				TLS_VERIFY ON)
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)

conan_cmake_run(REQUIRES jsoncpp/1.9.5
				BASIC_SETUP
				BUILD missing
				ARCH ${CONAN_SETTING_ARCH})

# compile antlr and cpp lexer and parser
# ----------------------------------------------------------------------------------------

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# required if linking to static library
add_definitions(-DANTLR4CPP_STATIC)

# using /MD flag for antlr4_runtime (for Visual C++ compilers only)
# set(ANTLR4_WITH_STATIC_CRT OFF)

# Specify the version of the antlr4 library needed for this project.
# By default the latest version of antlr4 will be used.  You can specify a
# specific, stable version by setting a repository tag value or a link
# to a zip file containing the libary source.
# set(ANTLR4_TAG 4.11.1)
# set(ANTLR4_ZIP_REPOSITORY https://github.com/antlr/antlr4/archive/refs/tags/4.11.1.zip)

# add external build for antlrcpp
include(ExternalAntlr4Cpp)
# add antrl4cpp artifacts to project environment
include_directories(${ANTLR4_INCLUDE_DIRS})

# set variable pointing to the antlr tool that supports C++
set(ANTLR_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/antlr-4.11.1-complete.jar)
# add macros to generate ANTLR Cpp code from grammar
find_package(ANTLR REQUIRED)

# Call macro to add lexer and grammar to your build dependencies
antlr_target(LATEX LATEX.g4 
			LEXER
			PARSER
			PACKAGE latex2antlr)

# include generated files in project environment
include_directories(${ANTLR_LATEX_OUTPUT_DIR})

# create python module
# ----------------------------------------------------------------------------------------

set(python_module_name latex2antlrJson)

pybind11_add_module(${python_module_name} src/latex2sympy/latex2antlrJson.cpp ${ANTLR_LATEX_CXX_OUTPUTS})
target_link_libraries(${python_module_name} PUBLIC antlr4_static ${CONAN_LIBS})

target_compile_features(${python_module_name} PUBLIC cxx_std_17)
set_target_properties(${python_module_name} PROPERTIES SUFFIX ".so")

install(TARGETS ${python_module_name} DESTINATION .)