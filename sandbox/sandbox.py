from latex2sympy.latex2sympy import process_sympy
from latex2sympy.lib import parseToJson
from sympy import srepr

latex = '\\variable{a}^{\\variable{b}}'

print('json: ', parseToJson(latex))

variables = {'a': process_sympy('658.95998'), 'b': process_sympy('185083.8060')}
c_ans_expr = process_sympy(latex, variables)
print('expr: ', c_ans_expr)
print('srepr(expr): ', srepr(c_ans_expr))
c_ans = c_ans_expr.doit(deep=False).evalf(chop=True)
print('expr => doit(deep=True), evalf(chop=True): ', c_ans)
print('srepr(ans): ', srepr(c_ans))


# numeric_responses = ['1', '1.0', '-1', '-1.0', '.5', '-.5', '3x10^3', '3E3', '3,000x10^{-3}', '0.5E-1', '\\frac{1}{3}', '(5\\times 3)^3', '\\sin(1)']
# for latex in numeric_responses:
#     parsed = process_sympy(latex)
#     print('latex: ', latex)
#     print('sympy: ', parsed)
#     print('is_number: ', parsed.is_number)
#     print('is_Number: ', parsed.is_Number)
#     print('srepr: ', srepr(parsed))
#     print('-----------------------------------------------------')
