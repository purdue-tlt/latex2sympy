from .context import assert_equal
import pytest
from sympy import Sum, I, Symbol, Integer, Add, Mul, Rational, exp, pi, Pow, re, im, arg, Abs

a = Symbol('a', real=True, positive=True)
b = Symbol('b', real=True, positive=True)
i = Symbol('i', real=True, positive=True)
n = Symbol('n', real=True, positive=True)
x = Symbol('x', real=True, positive=True)


def test_complex_expr_rectangular():
    assert_equal('a+\\imaginaryI b', Add(a, Mul(I, b, evaluate=False), evaluate=False))


def test_complex_expr_e():
    assert_equal('e^{\\imaginaryI \\pi }', Integer(-1))


def test_complex_sum():
    assert_equal('\\sum_{i=0}^{n} i \\cdot x', Sum(i * x, (i, 0, n)))


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
    # degrees
    ('50\\angle 60\\degree ', Mul(50, exp(Mul(I, Mul(60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('-50\\angle -60\\degree ', Mul(-1, 50, exp(Mul(I, Mul(-60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50.5\\angle 60.25\\degree ', Mul(Rational(101, 2), exp(Mul(I, Mul(Rational(241, 4), Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('-50\\angle -60.25\\degree ', Mul(-1, 50, exp(Mul(I, Mul(Rational(-241, 4), Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    # radians
    ('50\\angle \\pi ', Mul(50, exp(Mul(I, pi, evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -\\pi ', Mul(50, exp(Mul(I, Mul(-1, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle 3.14 ', Mul(50, exp(Mul(I, Rational(157, 50), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -3.14 ', Mul(50, exp(Mul(I, Rational(-157, 50), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle 2\\pi ', Mul(50, exp(Mul(I, Mul(2, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle 2*\\pi ', Mul(50, exp(Mul(I, Mul(2, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle 2\\cdot \\pi ', Mul(50, exp(Mul(I, Mul(2, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle 2\\times \\pi ', Mul(50, exp(Mul(I, Mul(2, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -2.1\\pi ', Mul(50, exp(Mul(I, Mul(Rational(-21, 10), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{\\pi}{3} ', Mul(50, exp(Mul(I, Mul(Pow(3, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -\\frac{\\pi}{3} ', Mul(50, exp(Mul(I, Mul(-1, Pow(3, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{-\\pi}{3} ', Mul(50, exp(Mul(I, Mul(Pow(3, -1, evaluate=False), Mul(-1, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{\\pi}{-3} ', Mul(50, exp(Mul(I, Mul(Pow(-3, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{2\\pi}{3} ', Mul(50, exp(Mul(I, Mul(Pow(3, -1, evaluate=False), Mul(2, pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{2}{3}\\pi ', Mul(50, exp(Mul(I, Mul(Rational(2, 3), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -\\frac{2}{3}\\pi ', Mul(50, exp(Mul(I, Mul(-1, Rational(2, 3), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{-2}{3}\\pi ', Mul(50, exp(Mul(I, Mul(Rational(-2, 3), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle \\frac{2}{3}', Mul(50, exp(Mul(I, Rational(2, 3), evaluate=False), evaluate=False), evaluate=False)),
    ('50\\angle -\\frac{2}{3}', Mul(50, exp(Mul(I, Rational(-2, 3), evaluate=False), evaluate=False), evaluate=False)),
]


@pytest.mark.parametrize('input, output', complex_number_polar_examples)
def test_complex_number_polar(input, output):
    assert_equal(input, output)


def test_complex_re():
    assert_equal('\\operatorname{Re}{3+\\imaginaryI 4}', re(Add(3, Mul(I, 4, evaluate=False), evaluate=False), evaluate=False))


def test_complex_im():
    assert_equal('\\operatorname{Im}{3+\\imaginaryI 4}', im(Add(3, Mul(I, 4, evaluate=False), evaluate=False), evaluate=False))


def test_complex_abs():
    assert_equal('\\operatorname{Abs}{50\\angle 60\\degree }', Abs(Mul(50, exp(Mul(I, Mul(60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False), evaluate=False))


def test_complex_arg():
    assert_equal('\\operatorname{Arg}{50\\angle 60\\degree }', arg(Mul(50, exp(Mul(I, Mul(60, Pow(180, -1, evaluate=False), pi, evaluate=False), evaluate=False), evaluate=False), evaluate=False), evaluate=False))
