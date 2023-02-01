# from latex2antlrJson import parseToJson
# import json
from latex2sympy2 import process_sympy
from sympy import srepr
from time import time

latex = '\\frac{1}{\\variable{Period}}\\int ^{\\frac{\\variable{Period}}{2}}_{\\variable{start_{time}}}\\left(\\variable{Vp}\\cdot {\\variable{I_{p}}\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)\\cdot \\left(\\sin \\mleft(2\\cdot \\frac{\\pi }{\\variable{Period}}t\\mright)\\right)}\\right)dt'

# json_string = parseToJson(latex)
# print(json_string)
# math_json = json.loads(json_string)
# print(math_json)

# expr = process_sympy(latex)
# print(srepr(expr))

begin = time()
expr = process_sympy(latex)
print(srepr(expr))
end = time()
elapsed = end - begin
print('Elapsed Time:', elapsed * 1000, 'ms')
