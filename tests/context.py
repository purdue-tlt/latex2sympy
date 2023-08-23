from sympy import srepr, Add, Mul, Pow, Rational, pi, sqrt, Symbol, exp, Eq
from latex2sympy.latex2sympy import process_sympy


x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, positive=True)
z = Symbol('z', real=True, positive=True)


# shorthand definitions


def _Add(*args):
    return Add(*args, evaluate=False)


def _Mul(*args):
    return Mul(*args, evaluate=False)


def _Pow(a, b):
    return Pow(a, b, evaluate=False)


def _Eq(a, b):
    return Eq(a, b, evaluate=False)


def get_simple_examples(func):
    '''
    Returns an array of tuples, containing the string `input`, sympy `output` using the provided sympy `func`.
    '''
    return [
        ("1.1", func(Rational(11, 10))),
        ("6.9", func(Rational(69, 10))),
        ("3.5", func(Rational(35, 10))),
        ("8", func(Rational(8))),
        ("0", func(Rational(0))),
        ("290348E32", func(Rational('290348E32'))),
        ("1237.293894239480234", func(Rational('1237.293894239480234'))),
        ("8623.4592104E-2", func(Rational('8623.4592104E-2'))),
        ("\\pi ", func(pi)),
        ("\\sqrt{100}", func(sqrt(100, evaluate=False))),
        ("12,123.4", func(Rational(121234, 10))),
        ("-9.4", func(Rational(-94, 10))),
        ("-35.9825", func(Rational(-359825, 10000))),
        ("-\\sqrt{5}", func(-sqrt(5, evaluate=False))),
        ("-324E-3", func(Rational(-324, 1000))),
        ("-0.23", func(Rational(-23, 100))),
        ("\\frac{1}{2}", func(Rational(1, 2))),
        ("\\frac{6}{2}", func(Rational(6, 2))),
        ("\\frac{9}{5}", func(Rational(9, 5))),
        ("\\frac{-42}{5}", func(Rational(-42, 5))),
        ("-\\frac{325}{3}", func(Rational(-325, 3))),
        ("\\frac{\\pi }{2}", func(_Mul(_Pow(2, -1), pi))),
        ("\\frac{1+6}{3}", func(_Mul(_Pow(3, -1), _Add(1, 6)))),
        ("\\frac{7*4}{5}", func(_Mul(_Pow(5, -1), _Mul(7, 4)))),
        ("15-2.3", func(_Add(15, _Mul(-1, Rational(23, 10))))),
        ("x", func(x)),
        ("x + y", func(x + y)),
        ("\\frac{9x}{4}", func(_Mul(_Pow(4, -1), _Mul(9, x)))),
        ("y\\pi", func(_Mul(y, pi))),
        ("2y-y-y", func(_Add(_Mul(-1, y), _Mul(-1, y), _Mul(2, y))))
    ]


def get_min_max_examples(cmd, func):
    return [
        (f"{cmd}(1, 5)", func(1, 5)),
        (f"{cmd}(12, 4)", func(12, 4)),
        (f"{cmd}(109, 120)", func(109, 120)),
        (f"{cmd}(3, 3)", func(3, 3)),
        (f"{cmd}(0, 0)", func(0, 0)),
        (f"{cmd}(1)", func(1)),
        (f"{cmd}(1092198374, 290348E32)", func(1092198374, Rational('290348E32'))),
        (f"{cmd}(5, 2, 17, 4)", func(5, 2, 17, 4)),

        (f"{cmd}(-9, 4)", func(-9, 4)),
        (f"{cmd}(4, -9)", func(4, -9)),
        (f"{cmd}(-7)", func(-7)),
        (f"{cmd}(-2, -2)", func(-2, -2)),
        (f"{cmd}(-324E-3, -58)", func(Rational('-324E-3'), -58)),
        (f"{cmd}(-1, 0, 1, -37, 42)", func(-1, 0, 1, -37, 42)),

        (f"{cmd}(\\pi, 3)", func(pi, 3)),
        (f"{cmd}(1234.56789, 1234.5678901)", func(Rational('1234.56789'), Rational('1234.5678901'))),
        (f"{cmd}(12.4, 9.5)", func(Rational(124, 10), Rational(95, 10))),
        (f"{cmd}(6, 6.2)", func(6, Rational(62, 10))),
        (f"{cmd}(-98.7)", func(Rational(-987, 10))),
        (f"{cmd}(7.1, 9)", func(Rational(71, 10), 9)),
        (f"{cmd}(-21E-12, 0.00005)", func(Rational('-21E-12'), Rational('0.00005'))),
        (f"{cmd}(\\sqrt{{3}}, 0, 1)", func(sqrt(3), 0, 1)),

        (f"{cmd}(\\frac{{1}}{{2}}, \\frac{{1}}{{4}})", func(Rational(1, 2), Rational(1, 4))),
        (f"{cmd}(\\frac{{6}}{{2}}, 3)", func(Rational(6, 2), 3)),
        (f"{cmd}(\\frac{{2}}{{4}}, \\frac{{1}}{{2}})", func(Rational(2, 4), Rational(1, 2))),
        (f"{cmd}(\\frac{{-12}}{{5}}, 6.4)", func(Rational(-12, 5), Rational(64, 10))),
        (f"{cmd}(\\frac{{1}}{{10}})", func(Rational(1, 10))),
        (f"{cmd}(1.5, \\frac{{\\pi }}{{2}})", func(Rational(15, 10), _Mul(_Pow(2, -1), pi))),
        (f"{cmd}(\\frac{{-4}}{{3}}, \\frac{{-2}}{{1}}, \\frac{{0}}{{9}}, -3)", func(Rational(-4, 3), Rational(-2, 1), Rational(0, 9), -3)),

        (f"{cmd}(\\frac{{1+6}}{{3}}, 7)", func(_Mul(_Pow(3, -1), _Add(1, 6)), 7)),
        (f"{cmd}(58*9)", func(_Mul(58, 9))),
        (f"{cmd}(1+\\frac{{6}}{{3}}, -5)", func(_Add(1, Rational(6, 3)), -5)),
        (f"{cmd}(7*\\frac{{4}}{{5}}, 092) * 2", func(_Mul(7, Rational(4, 5)), 92) * 2),
        (f"38+{cmd}(13, 15-2.3)", 38 + func(13, _Add(15, _Mul(-1, Rational(23, 10))))),
        (f"\\sqrt{{{cmd}(99.9999999999999, 100)}}", sqrt(func(Rational('99.9999999999999'), 100), evaluate=False)),
        (f"{cmd}(\\frac{{274}}{{5+2}}, \\exp(12.4), 1.4E2)", func(_Mul(_Pow(_Add(5, 2), -1), 274), exp(Rational('12.4')), Rational('1.4E2'))),

        (f"{cmd}(x)", func(x)),
        (f"{cmd}(x, y)", func(x, y)),
        (f"{cmd}(y, x)", func(y, x)),
        (f"{cmd}(x+y, y+x)", func(_Add(x, y), _Add(y, x))),
        (f"{cmd}(9\\frac{{x}}{{4}}, z)", func(_Mul(9, _Pow(4, -1), x), z)),
        (f"{cmd}(y\\pi, 9)", func(y * pi, 9)),
        (f"{cmd}(2y-y, y + 1)", func(_Add(_Mul(2, y), _Mul(y, -1)), _Add(y, 1))),
        (f"{cmd}(z, y, x)", func(z, y, x)),

        (f"{cmd}(1,2)", func(1, 2)),
        (f"{cmd}(9,876,543)", func(9, 876, 543)),
        (f"{cmd}(x, y,z)", func(x, y, z)),
        (f"{cmd}(5.8,7.4, 2.2,-10)", func(Rational('5.8'), Rational('7.4'), Rational('2.2'), -10)),
        (f"{cmd}(\\pi,12E2,84,\\sqrt{{5}},\\frac{{12}}{{5}})", func(pi, Rational('12E2'), 84, sqrt(5), Rational(12, 5))),
        (f"{cmd}(823,51)", func(823, 51)),
        (f"{cmd}(72*4, 23, 9)", func(_Mul(72, 4), 23, 9))
    ]


def get_gcd_lcm_examples(cmd, func, func_eval, multi_func):
    return [
        (f"{cmd}(18, 3)", func(18, 3)),
        (f"{cmd}(3, 18)", func(3, 18)),
        (f"{cmd}(2, 2)", func(2, 2)),
        (f"{cmd}(0, 21)", func(0, 21)),
        (f"{cmd}(21, 0)", func(21, 0)),
        (f"{cmd}(0, 0)", func(0, 0)),
        (f"{cmd}(6128, 24)", func(6128, 24)),
        (f"{cmd}(24, 6128)", func(24, 6128)),
        (f"{cmd}(1E20, 1000000)", func(Rational('1E20'), 1000000)),
        (f"{cmd}(128*10^{{32}}, 1)", func(Rational('128E32'), 1)),

        (f"{cmd}(-12, 4)", func(-12, 4)),
        (f"{cmd}(219, -9)", func(219, -9)),
        (f"{cmd}(-8, -64)", func(-8, -64)),
        (f"{cmd}(-5, -5)", func(-5, -5)),
        (f"{cmd}(-1, 182033)", func(-1, 182033)),
        (f"{cmd}(25, -6125)", func(25, -6125)),
        (f"{cmd}(243, -2.9543127E21)", func(243, Rational('-2.9543127E21'))),

        (f"{cmd}(2.4, 3.6)", func(Rational('2.4'), Rational('3.6'))),
        (f"{cmd}(3.6, 2.4)", func(Rational('3.6'), Rational('2.4'))),
        (f"{cmd}(\\pi, 3)", func(pi, 3)),
        (f"{cmd}(618, 1.5)", func(618, Rational('1.5'))),
        (f"{cmd}(-1.5, 618)", func(Rational('-1.5'), 618)),
        (f"{cmd}(0.42, 2)", func(Rational('0.42'), 2)),
        (f"{cmd}(1.43E-13, 21)", func(Rational('1.43E-13'), 21)),
        (f"{cmd}(21, -143E-13)", func(21, Rational('-143E-13'))),
        (f"{cmd}(9.80655, 9.80655)", func(Rational('9.80655'), Rational('9.80655'))),
        (f"{cmd}(0.0000923423, -8341.234802909)", func(Rational('0.0000923423'), Rational('-8341.234802909'))),
        (f"{cmd}(\\sqrt{{5}}, \\sqrt{{2}})", func(sqrt(5, evaluate=False), sqrt(2, evaluate=False))),

        (f"{cmd}(\\frac{{1}}{{2}}, 3)", func(Rational(1, 2), 3)),
        (f"{cmd}(3, \\frac{{1}}{{2}})", func(3, Rational(1, 2))),
        (f"{cmd}(\\frac{{6}}{{2}}, 3)", func(Rational(6, 2), 3)),
        (f"{cmd}(\\frac{{1}}{{10}}, \\frac{{1}}{{10}})", func(Rational(1, 10), Rational(1, 10))),
        (f"{cmd}(42, \\frac{{42}}{{6}})", func(42, Rational(42, 6))),
        (f"{cmd}(\\frac{{10000000}}{{10}}, 10000)", func(Rational(10000000, 10), 10000)),

        (f"{cmd}(1+1, 8)", func(1 + 1, 8)),
        (f"920*{cmd}(9, 12*\\frac{{4}}{{2}})", 920 * func(9, 12 * Rational(4, 2))),
        (f"{cmd}(32-128, 10)*22", _Mul(func(32 - 128, 10), 22)),
        (f"\\sqrt{{{cmd}(1.25E24, 1E12)}}", sqrt(func(Rational('1.25E24'), Rational('1E12')), evaluate=False)),
        (f"{cmd}(92.0, 000+2)", func(Rational('92.0'), 000 + 2)),

        (f"{cmd}(830,450)", func(830, 450)),
        (f"{cmd}(6,321,429)", multi_func(6, 321, 429)),
        (f"{cmd}(14,2324)", func(14, 2324)),
        (f"{cmd}(3, 6, 2)", multi_func(3, 6, 2)),
        (f"{cmd}(144, 2988, 37116)", multi_func(144, 2988, 37116)),
        (f"{cmd}(144,2988, 37116,18, 72)", multi_func(144, 2988, 37116, 18, 72)),
        (f"{cmd}(144, 2988, 37116, 18, 72, 12, 6)", multi_func(144, 2988, 37116, 18, 72, 12, 6)),
        (f"{cmd}(32)", func(32, 32)),
        (f"{cmd}(-8, 4,-2)", multi_func(-8, 4, -2)),
        (f"{cmd}(6*4,48, 3)", multi_func(6 * 4, 48, 3)),
        (f"{cmd}(6*4,48,3)", multi_func(6 * 4, 48, 3)),
        (f"{cmd}(2.4,3.6, 0.6)", func(Rational('2.4'), func_eval(Rational('3.6'), Rational('0.6')))),
        (f"{cmd}(2.4,3.6,0.6)", func(Rational('2.4'), func_eval(Rational('3.6'), Rational('0.6')))),
        (f"{cmd}(\\sqrt{{3}}, \\sqrt{{2}}, \\sqrt{{100}})", func(sqrt(3), func_eval(sqrt(2), sqrt(100)))),
        (f"{cmd}(1E12, 1E6,1E3, 10)", multi_func(Rational('1E12'), Rational('1E6'), Rational('1E3'), 10)),
    ]


def compare(actual, expected):
    actual_exp_tree = srepr(actual)
    expected_exp_tree = srepr(expected)
    try:
        assert actual_exp_tree == expected_exp_tree
    except Exception:
        print('expected_exp_tree = ', expected_exp_tree)
        print('actual exp tree = ', actual_exp_tree)
        raise


def assert_equal(latex, expr, variable_values={}, parse_letters_as_units=False):
    parsed = process_sympy(latex, variable_values, parse_letters_as_units)
    compare(parsed, expr)
