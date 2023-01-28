#include "antlr4-runtime.h"
#include "LATEXLexer.h"
#include "LATEXParser.h"
#include <pybind11/pybind11.h>
#include <chrono>

using namespace latex2antlr;
using namespace antlr4;
using namespace std::chrono;

int parse(const std::string& input) {
    auto begin = high_resolution_clock::now();

    ANTLRInputStream stream(input);
    LATEXLexer lexer(&stream);
    CommonTokenStream tokens(&lexer);
    LATEXParser parser(&tokens);
    LATEXParser::MathContext* math = parser.math();

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - begin);

    std::cout << math -> toStringTree(&parser) << std::endl;
    std::cout << "Elapsed Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    return 0;
}

namespace py = pybind11;

PYBIND11_MODULE(latex2antlr2py, m) {
    m.doc() = "pybind11 latex2antlr2py plugin"; // optional module docstring
    m.def("parse", &parse, "A function which parses latex");
}
