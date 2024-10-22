from sympy import binomial, Rational, Symbol

from .context import _Add, assert_equal

x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, positive=True)
theta = Symbol('theta', real=True, positive=True)
gamma = Symbol('gamma', real=True, positive=True)


def test_binomial_numeric():
    assert_equal("\\binom{16}{2}", binomial(16, 2))


def test_binomial_symbols():
    assert_equal("\\binom{x}{y}", binomial(x, y))


def test_binomial_greek_symbols():
    assert_equal("\\binom{\\theta}{\\gamma}", binomial(theta, gamma))


def test_binomial_expr():
    assert_equal("\\binom{16+2}{\\frac{4}{2}}", binomial(_Add(16, 2), Rational(4, 2)))


def test_choose_numeric():
    assert_equal("\\choose{16}{2}", binomial(16, 2))


def test_choose_symbols():
    assert_equal("\\choose{x}{y}", binomial(x, y))


def test_choose_greek_symbols():
    assert_equal("\\choose{\\theta}{\\gamma}", binomial(theta, gamma))
