from parser.cpp.build.lib.latex2antlrJson import parseToJson
# import json
from latex2sympy2 import process_sympy
from sympy import srepr
from time import time

latex = '\\gcd(a, b)'

json_string = parseToJson(latex)
print(json_string)
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
