from .context import assert_equal, get_variable_symbol
import pytest
from sympy import UnevaluatedExpr, Symbol, Mul, Pow, Max, Min, gcd, lcm, floor, ceiling, Rational

x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, positive=True)

x_variable_symbol = get_variable_symbol('x')


def test_variable_letter():
    assert_equal("\\variable{x}", x_variable_symbol)


def test_variable_digit():
    assert_equal("\\variable{1}", get_variable_symbol('1'))


def test_variable_letter_subscript():
    assert_equal("\\variable{x_y}", get_variable_symbol('x_y'))


def test_variable_wrapped_single_letter_subscript():
    assert_equal("\\variable{x_{y}}", get_variable_symbol('x_{y}'))


def test_variable_letter_comma_subscript():
    assert_equal("\\variable{x_{i,j}}", get_variable_symbol('x_{i,j}'))


def test_variable_single_digit_subscript():
    assert_equal("\\variable{x_1}", get_variable_symbol('x_1'))


def test_variable_wrapped_single_digit_subscript():
    assert_equal("\\variable{x_{1}}", get_variable_symbol('x_{1}'))


def test_variable_after_subscript_required():
    with pytest.raises(Exception):
        assert_equal("\\variable{x_}", get_variable_symbol('x_'))


def test_variable_before_subscript_required():
    with pytest.raises(Exception):
        assert_equal("\\variable{_x}", get_variable_symbol('_x'))


def test_variable_bad_name():
    with pytest.raises(Exception):
        assert_equal("\\variable{\\sin xy}", None)


def test_variable_in_expr():
    assert_equal("4\\cdot\\variable{x}", 4 * x_variable_symbol)


def test_variable_greek_letter():
    assert_equal("\\variable{\\alpha }\\alpha", get_variable_symbol('\\alpha ') * Symbol('alpha', real=True, positive=True))


def test_variable_greek_letter_subscript():
    assert_equal("\\variable{\\alpha _{\\beta }}\\alpha ", get_variable_symbol('\\alpha _{\\beta }') * Symbol('alpha', real=True, positive=True))


def test_variable_bad_unbraced_long_subscript():
    with pytest.raises(Exception):
        assert_equal("\\variable{x_yz}", None)


def test_variable_bad_unbraced_long_complex_subscript():
    with pytest.raises(Exception):
        assert_equal("\\variable{x\\beta 10_y\\alpha 20}", None)


def test_variable_braced_subscript():
    assert_equal("\\variable{x\\beta 10_{y\\alpha 20}}", get_variable_symbol('x\\beta 10_{y\\alpha 20}'))


def test_variable_complex_expr():
    assert_equal("4\\cdot\\variable{value1}\\frac{\\variable{value_2}}{\\variable{a}}\\cdot x^2", 4 * get_variable_symbol('value1') * get_variable_symbol('value_2') / get_variable_symbol('a') * x**2)


def test_variable_dollars():
    assert_equal("\\$\\variable{x}", x_variable_symbol)


def test_variable_percentage():
    assert_equal("\\variable{x}\\%", Mul(x_variable_symbol, Pow(100, -1, evaluate=False), evaluate=False))


def test_variable_single_arg_func():
    assert_equal("\\floor(\\variable{x})", floor(x_variable_symbol))
    assert_equal("\\ceil(\\variable{x})", ceiling(x_variable_symbol))


def test_variable_multi_arg_func():
    assert_equal("\\gcd(\\variable{x}, \\variable{y})", UnevaluatedExpr(gcd(x_variable_symbol, get_variable_symbol('y'))))
    assert_equal("\\lcm(\\variable{x}, \\variable{y})", UnevaluatedExpr(lcm(x_variable_symbol, get_variable_symbol('y'))))
    assert_equal("\\max(\\variable{x}, \\variable{y})", Max(x_variable_symbol, get_variable_symbol('y'), evaluate=False))
    assert_equal("\\min(\\variable{x}, \\variable{y})", Min(x_variable_symbol, get_variable_symbol('y'), evaluate=False))


def test_variable_substitute_sympy_value():
    assert_equal("\\variable{x}", Rational(3, 5), {'x': Rational(3, 5)})
