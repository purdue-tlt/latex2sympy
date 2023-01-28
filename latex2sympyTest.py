import antlr4
try:
    from parser.python.LATEXParser import LATEXParser
    from parser.python.LATEXLexer import LATEXLexer
except Exception:
    from .parser.python.LATEXParser import LATEXParser
    from .parser.python.LATEXLexer import LATEXLexer
from time import time

begin = time()
stream = antlr4.InputStream('\\frac{1}{\\variable{Period}}\\int ^{\\frac{\\variable{Period}}{2}}_{\\variable{start_{time}}}\\left(\\variable{Vp}\\cdot {\\variable{I_{p}}\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)}\\right)dt')
lex = LATEXLexer(stream)
tokens = antlr4.CommonTokenStream(lex)
parser = LATEXParser(tokens)
math = parser.math()
end = time()
print('Elapsed Time:', end - begin)
