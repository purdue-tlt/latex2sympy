from sympy import srepr
from latex2sympy.latex2sympy import process_sympy
from latex2sympy.lib.macOS.arm64.latex2antlrJson import parseToJson

latex_strings = [
    '\\operatorname{arg}(3+4I)',
    '\\operatorname{im}(3+4I)',
    '\\operatorname{re}(3+4I)',
    # '\\text{4+5}'
]
for latex in latex_strings:
    print('latex => ', latex)
    # print('json => ', parseToJson(latex))
    s = process_sympy(latex)
    print('srepr() => ', srepr(s))
    print('evalf() => ', s.evalf())
    print('')
