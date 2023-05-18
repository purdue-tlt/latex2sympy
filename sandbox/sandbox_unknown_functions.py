from sympy import srepr
from latex2sympy.latex2sympy import process_sympy
from latex2sympy.lib.macOS.arm64.latex2antlrJson import parseToJson

latex_strings = [
    '\\operatorname{arg}(3+4I)',
    '\\operatorname{im}(3+4I)',
    '\\operatorname{re}(3+4I)',

    '\\sympy{\'re(3+4*I)\'}',
    '\\maxima{\'sum(k, k, 1, n)\'}',
    '\\maxima{\'factor( x**2 + 2*x + 1)\'}',
    '\\mathematica{\'Cos[x]^2 (1 - Cos[y]^2)\'}'
]

for latex in latex_strings:
    print('latex => ', latex)
    print('json => ', parseToJson(latex))
    s = process_sympy(latex)
    print('sympy => ', s)
    print('srepr() => ', srepr(s))
    print('evalf() => ', s.evalf())
    print('')
