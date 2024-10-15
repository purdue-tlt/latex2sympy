from sympy import sin, Symbol

from .context import assert_equal

x = Symbol('x', real=True, positive=True)


def test_overline():
    assert_equal("\\frac{\\sin(x)}{\\overline{x}_n}", sin(x) / Symbol('xbar_n', real=True, positive=True))
