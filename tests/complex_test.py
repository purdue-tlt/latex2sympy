from .context import assert_equal
import pytest
from sympy import Sum, I, Symbol, Integer, Add, Mul, Rational, exp, pi, Pow

a = Symbol('a', real=True, positive=True)
b = Symbol('b', real=True, positive=True)
i = Symbol('i', real=True, positive=True)
n = Symbol('n', real=True, positive=True)
x = Symbol('x', real=True, positive=True)


def test_complex_expr_rectangular():
    assert_equal("a+\\imaginaryI b", Add(a, Mul(I, b, evaluate=False), evaluate=False))


def test_complex_expr_e():
    assert_equal("e^{\\imaginaryI \\pi }", Integer(-1))


def test_complex_sum():
    assert_equal("\\sum_{i=0}^{n} i \\cdot x", Sum(i * x, (i, 0, n)))


complex_number_rectangular_examples = [
    ('3+\\imaginaryI 4', Add(3, Mul(I, 4, evaluate=False), evaluate=False)),
    ('-3-4\\imaginaryI ', Add(-3, Mul(-1, 4, I, evaluate=False), evaluate=False)),
    ('3.14+\\imaginaryI 4.657', Add(Rational(157, 50), Mul(I, Rational(4657, 1000), evaluate=False), evaluate=False)),
    ('3+\\imaginaryJ 4', Add(3, Mul(I, 4, evaluate=False), evaluate=False)),
    ('-3-4\\imaginaryJ ', Add(-3, Mul(-1, 4, I, evaluate=False), evaluate=False)),
    ('3.14+\\imaginaryJ 4.657', Add(Rational(157, 50), Mul(I, Rational(4657, 1000), evaluate=False), evaluate=False)),
]


@pytest.mark.parametrize('input, output', complex_number_rectangular_examples)
def test_complex_number_rectangular(input, output):
    assert_equal(input, output)


complex_number_polar_examples = [
    ('50\\angle 60\\degree ', Mul(50, exp(Mul(I, Mul(60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('-50\\angle -60\\degree ', Mul(-1, 50, exp(Mul(I, Mul(-60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50.5\\angle 60.25\\degree ', Mul(Rational(101, 2), exp(Mul(I, Mul(Rational(241, 4), Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
]


@pytest.mark.parametrize('input, output', complex_number_polar_examples)
def test_complex_number_polar(input, output):
    assert_equal(input, output)
