from sympy import Symbol
from sympy import sympify
from latex2sympy import process_sympy

x = Symbol('x', real=True)

latex = '\\mathrm{\\sin }\\mleft(0\\mright)'
parsed = process_sympy(latex)
print('parsed:', parsed)

# answer = parsed.evalf()
# answer = parsed.evalf(subs={x: '1'})
# print('answer:', answer)
