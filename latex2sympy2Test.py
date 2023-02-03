from latex2sympy.latex2antlrJson import parseToJson
from latex2sympy.latex2sympy2 import process_sympy
from sympy import srepr
from time import time

latex = '\\frac{1}{\\variable{Period}}\\int ^{\\frac{\\variable{Period}}{2}}_{\\variable{start_{time}}}\\left(\\variable{Vp}\\cdot {\\variable{I_{p}}\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)}\\right)dt'
# latex = '\\frac{\\left(1+\\variable{b6}/100\\right)^{\\variable{b5}}-1}{\\variable{b6}/100}*\\variable{b16}-\\variable{b15}*\\left(1+\\variable{b6}/100\\right)^{\\variable{b5}}'
# latex = '\\lcm 1,2'

begin = time()

# json_string = parseToJson(latex)
# print(json_string)

expr = process_sympy(latex)
# print(srepr(expr))

end = time()
elapsed = end - begin
print('Elapsed Time:', elapsed * 1000, 'ms')
