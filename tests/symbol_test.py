from .context import assert_equal
import pytest
from sympy import Symbol, simplify
from latex2sympy.latex2sympy import process_sympy


def test_symbol_parses_as_positive():
    assert_equal('x', Symbol('x', real=True, positive=True))


def test_symbol_equivalence():
    latex_array = [
        '\\frac{y}{x}^{0.25}',
        '\\frac{y}{x}^{\\frac{1}{4}}',
        '\\frac{y^{0.25}}{x^{0.25}}',
        '\\frac{y^{\\frac{1}{4}}}{x^{\\frac{1}{4}}}',
        'y^{0.25}x^{-0.25}',
        'y^{\\frac{1}{4}}x^{-\\frac{1}{4}}'
    ]

    sympy_array = []
    for latex in latex_array:
        sympy_expr = process_sympy(latex)
        sympy_array.append(process_sympy(latex))

    compare_array = []
    for i in range(len(sympy_array)):
        s1 = sympy_array[i]
        for j in range(len(sympy_array)):
            if i == j:
                continue
            s2 = sympy_array[j]
            s3 = simplify(s1 - s2)
            assert s3 == 0
