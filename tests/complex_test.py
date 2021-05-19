from .context import assert_equal
import pytest
from sympy import Sum, I, Symbol, Integer

a = Symbol('a', real=True, positive=True)
b = Symbol('b', real=True, positive=True)
i = Symbol('i', real=True, positive=True)
n = Symbol('n', real=True, positive=True)
x = Symbol('x', real=True, positive=True)


def test_complex():
    assert_equal("a+Ib", a + I * b)


def test_complex_e():
    assert_equal("e^{I\\pi}", Integer(-1))


def test_complex_sum():
    assert_equal("\\sum_{i=0}^{n} i \\cdot x", Sum(i * x, (i, 0, n)))
