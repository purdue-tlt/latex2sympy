import antlr4
from latex2sympy.parser.python.LATEXParser import LATEXParser
from latex2sympy.parser.python.LATEXLexer import LATEXLexer
from latex2sympy.latex2sympy import process_sympy
from time import time
from sympy import srepr

latex = '\\frac{1}{\\variable{Period}}\\int ^{\\frac{\\variable{Period}}{2}}_{\\variable{start_{time}}}\\left(\\variable{Vp}\\cdot {\\variable{I_{p}}\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)}\\right)dt'
# latex = '\\frac{\\left(1+\\variable{b6}/100\\right)^{\\variable{b5}}-1}{\\variable{b6}/100}*\\variable{b16}-\\variable{b15}*\\left(1+\\variable{b6}/100\\right)^{\\variable{b5}}'

begin = time()

# stream = antlr4.InputStream(latex)
# lex = LATEXLexer(stream)
# tokens = antlr4.CommonTokenStream(lex)
# parser = LATEXParser(tokens)
# math = parser.math()

expr = process_sympy(latex)
# print(srepr(expr))

end = time()
elapsed = end - begin
print('Elapsed Time:', elapsed * 1000, 'ms')
