from sympy import Symbol
from sympy import sympify
from latex2sympy import process_sympy

x = Symbol('x', real=True)

latex = '\\mathit{x+1}'
parsed = process_sympy(latex)
answer = parsed.evalf()
print(parsed, answer)

# latex = 'x'
# parsed = process_sympy(latex)
# answer = parsed.evalf(subs={x: '1'})
# print(answer)
