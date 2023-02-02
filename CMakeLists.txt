cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

SET(CMAKE_CXX_STANDARD 17)
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

if(DEFINED SKBUILD)

	if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
		message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
		file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/0.18.1/conan.cmake"
					"${CMAKE_BINARY_DIR}/conan.cmake"
					TLS_VERIFY ON)
	endif()

	include(${CMAKE_BINARY_DIR}/conan.cmake)

	conan_cmake_run(REQUIRES antlr4-cppruntime/4.11.1 jsoncpp/1.9.5
					BASIC_SETUP
					BUILD missing)
else()
	include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
	conan_basic_setup()
endif()

# compile antlr cpp lexer and parser
# ----------------------------------------------------------------------------------------

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

find_package(antlr4-runtime REQUIRED)
find_package(antlr4-generator REQUIRED)

set(ANTLR4_JAR_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/antlr-4.11.1-complete.jar)

antlr4_generate(
	latex2antlr
	${CMAKE_CURRENT_SOURCE_DIR}/LATEX.g4
	BOTH
	FALSE
	FALSE
	"latex2antlr"
)

include_directories(${PROJECT_BINARY_DIR} ${ANTLR4_INCLUDE_DIR} ${ANTLR4_INCLUDE_DIR_latex2antlr})

# ----------------------------------------------------------------------------------------

# add cpp antlr lexer and parser
add_library(latex2antlr ${ANTLR4_SRC_FILES_latex2antlr})

# create python module
set(python_module_name latex2antlrJson)

pybind11_add_module(${python_module_name} src/latex2sympy/parser/cpp/latex2antlrJson.cpp)
target_link_libraries(${python_module_name} PUBLIC latex2antlr ${CONAN_LIBS})
target_compile_features(${python_module_name} PUBLIC cxx_std_17)
set_target_properties(${python_module_name} PROPERTIES SUFFIX ".so")

install(TARGETS ${python_module_name} DESTINATION .)