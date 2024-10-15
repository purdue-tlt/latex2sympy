from sympy import sin, Symbol

from .context import assert_equal

x = Symbol('x', real=True, positive=True)


def test_left_right_cdot():
    assert_equal("\\sin\\left(x\\right)\\cdot x", sin(x) * x)
