#include "antlr4-runtime.h"
#include "LATEXLexer.h"
#include "LATEXParser.h"
#include <chrono>

using namespace latex2antlr;
using namespace antlr4;
using namespace std::chrono;

int main(int, const char**) {
    auto begin = high_resolution_clock::now();

    ANTLRInputStream input(u8"\\frac{1}{\\variable{Period}}\\int ^{\\frac{\\variable{Period}}{2}}_{\\variable{start_{time}}}\\left(\\variable{Vp}\\cdot {\\variable{I_{p}}\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)}\\right)dt");
    LATEXLexer lexer(&input);
    CommonTokenStream tokens(&lexer);
    LATEXParser parser(&tokens);
    LATEXParser::MathContext* math = parser.math();

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end - begin);

    std::cout << math -> toStringTree(&parser) << std::endl;
    std::cout << "Elapsed Time: " << duration.count() << std::endl;

    return 0;
}
