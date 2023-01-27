# include "antlr4-runtime.h"
# include "PSLexer.h"
# include "PSParser.h"

using namespace latex2sympy
using namespace antlr4

int main(int, const char **) {
    ANTLRInputStream input(u8"x+\\frac{1}{2}")
    PSLexer lexer( & input)
    CommonTokenStream tokens( & lexer)
    PSParser parser( & tokens)
    tree:: ParseTree * tree = parser.math()

    std: : cout << tree -> toStringTree(&parser) << std: : endl

    return 0
}
