from sympy import *
from latex2sympy import process_sympy


latex = '\\left(\\variable{\\alpha }\\cdot \\variable{c}\\cdot \\variable{a}\\right)\\cdot x^{-\\variable{c}-1}_1\\cdot \\left(\\variable{a}\\cdot x^{-\\variable{c}}_1+\\variable{b}\\cdot x^{-\\variable{c}}_2\\right)^{-\\variable{\\alpha }-1}\\cdot dx_1+\\left(\\variable{\\alpha }\\cdot \\variable{c}\\cdot \\variable{b}\\right)\\cdot x^{-\\variable{c}-1}_2\\cdot \\left(\\variable{a}\\cdot x^{-\\variable{c}}_1+\\variable{b}\\cdot x^{-\\variable{c}}_2\\right)^{-\\variable{\\alpha }-1}\\cdot dx_2'
c_ans_expr = process_sympy(latex)
print(c_ans_expr)
print(srepr(c_ans_expr))


# numeric_responses = ['1', '1.0', '-1', '-1.0', '.5', '-.5', '3x10^3', '3E3', '3,000x10^{-3}', '0.5E-1', '\\\\frac{1}{3}', '(5\\\\times 3)^3', '\\\\sin(1)']
# for latex in numeric_responses:
#     parsed = process_sympy(latex)
#     print('latex: ', latex)
#     print('sympy: ', parsed)
#     print('is_number: ', parsed.is_number)
#     print('is_Number: ', parsed.is_Number)
#     print('srepr: ', srepr(parsed))
#     print('-----------------------------------------------------')
