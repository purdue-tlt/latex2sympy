cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

project("latex2antlrJson")

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)

include(GNUInstallDirs)
include(FetchContent)

FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG        v2.10.3
	GIT_SHALLOW    TRUE
)
FetchContent_MakeAvailable(pybind11)

if(DEFINED SKBUILD)

	if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
		message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
		file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/0.18.1/conan.cmake"
					"${CMAKE_BINARY_DIR}/conan.cmake"
					TLS_VERIFY ON)
	endif()

	include(${CMAKE_BINARY_DIR}/conan.cmake)

	conan_cmake_run(REQUIRES antlr4-cppruntime/4.11.1 jsoncpp/1.9.5
					BASIC_SETUP)
else()
	include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
	conan_basic_setup()
endif()

add_library(latex2antlr src/latex2sympy/parser/cpp/LATEXLexer.cpp src/latex2sympy/parser/cpp/LATEXParser.cpp)

set(python_module_name latex2antlrJson)
pybind11_add_module(${python_module_name} src/latex2sympy/parser/cpp/latex2antlrJson.cpp)
target_link_libraries(${python_module_name} PUBLIC latex2antlr ${CONAN_LIBS})
target_compile_features(latex2antlrJson PUBLIC cxx_std_17)
set_target_properties(latex2antlrJson PROPERTIES SUFFIX ".so")

install(TARGETS ${python_module_name} DESTINATION .)