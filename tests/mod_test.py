from sympy import Mod, pi, Rational, sqrt

from .context import _Add, _Mul, _Pow, assert_equal, x, y


def _Mod(*args):
    return Mod(*args, evaluate=False)


def test_mod_usual():
    assert_equal("128\\mod 3", _Mod(128, 3))
    assert_equal("7\\mod 128", _Mod(7, 128))
    assert_equal("5\\mod 10", _Mod(5, 10))
    assert_equal("5\\mod 5", _Mod(5, 5))
    assert_equal("3\\mod 2", _Mod(3, 2))
    assert_equal("0 \\mod 6", _Mod(0, 6))
    assert_equal("6109\\mod 28", _Mod(6109, 28))
    assert_equal("4000000000\\mod 28791", _Mod(4000000000, 28791))
    assert_equal("128\\times 10^{300}\\mod 876123", _Mod(Rational('128E300'), 876123))
    assert_equal("876,123\\mod 128E300)", _Mod(876123, Rational('128E300')))


def test_mod_negative():
    assert_equal("-1\\mod 2", _Mod(-1, 2))
    assert_equal("-3\\mod 3", _Mod(-3, 3))
    assert_equal("-12\\mod -12", _Mod(-12, -12))
    assert_equal("-128\\mod 4", _Mod(-128, 4))
    assert_equal("9\\mod -213", _Mod(9, -213))
    assert_equal("123123\\mod -541", _Mod(123123, -541))
    assert_equal("-123123\\mod 541", _Mod(-123123, 541))
    assert_equal("-97E34\\mod 7", _Mod(Rational('-97E34'), 7))


def test_mod_fraction():
    assert_equal("\\frac{1}{2} \\mod 3", _Mod(Rational(1, 2), 3))
    assert_equal("\\frac{6}{2} \\mod 3", _Mod(Rational(6, 2), 3))
    assert_equal("\\frac{-14}{2} \\mod 5", _Mod(Rational(-14, 2), 5))
    assert_equal("123\\mod \\frac{42}{6}", _Mod(123, Rational(42, 6)))
    assert_equal("431\\mod \\frac{2}{123}", _Mod(431, Rational(2, 123)))
    assert_equal("\\frac{5}{5} \\mod \\frac{5}{5}", _Mod(Rational(5, 5), Rational(5, 5)))
    assert_equal("\\frac{849}{-21}\\mod \\frac{92}{2}", _Mod(Rational(849, -21), Rational(92, 2)))
    assert_equal("13\\times 10^9\\mod \\frac{21}{-2}", _Mod(Rational('13E9'), Rational(21, -2)))


def test_mod_float():
    assert_equal("0.41\\mod 2", _Mod(Rational('0.41'), 2))
    assert_equal("143E-13\\mod 21", _Mod(Rational('143E-13'), 21))
    assert_equal("-9.80665\\mod 9.80665", _Mod(Rational('-9.80665'), Rational('9.80665')))
    assert_equal("0.0000923423\\mod -8341.234802909", _Mod(Rational('0.0000923423'), Rational('-8341.234802909')))
    assert_equal("\\sqrt{5}\\mod \\sqrt{2}", _Mod(sqrt(5, evaluate=False), sqrt(2, evaluate=False)))
    assert_equal("987\\mod \\pi", _Mod(987, pi))
    assert_equal("\\pi\\mod \\frac{1+\\sqrt{5}}{2})", _Mod(pi, _Mul(_Pow(2, -1), _Add(1, sqrt(5, evaluate=False)))))
    assert_equal("1234\\mod 1E-29", _Mod(1234, Rational('1E-29')))


def test_mod_expr():
    assert_equal("1+1\\mod 2", 1 + _Mod(1, 2))
    assert_equal("876123\\mod 128\\times 10^{300}", _Mod(876123, Rational('128E300')))
    assert_equal("141\\mod \\frac{9}{3}", _Mod(141, Rational(9, 3)))
    assert_equal("\\frac{872}{12\\mod 9 * 4} * 2", _Mul(872, _Pow(_Mul(_Mod(12, 9), 4), -1), 2))
    assert_equal("1E-32 * (1E29\\mod 74)", _Mul(Rational('1E-32'), _Mod(Rational('1E29'), 74)))
    assert_equal("299,792,458\\mod 9.81", _Mod(299792458, Rational('9.81')))


def test_mod_symbol():
    assert_equal("x\\mod y", _Mod(x, y))
    assert_equal("2x\\mod y", _Mod(2 * x, y))
    assert_equal("y + \\frac{3\\mod 2}{4}", _Add(y, _Mul(_Mod(3, 2), _Pow(4, -1))))
    assert_equal("0.5x * 2 + \\sqrt{x}\\mod 8y", _Add(_Mul(Rational(1, 2), x, 2), _Mod(sqrt(x), _Mul(8, y))))
    assert_equal(
        "6.673E-11 * \\frac{(8.85418782E-12\\mod 9x) + 4}{2y}",
        _Mul(Rational('6.673E-11'), _Add(_Mod(Rational('8.85418782E-12'), _Mul(9, x)), 4), _Pow(_Mul(2, y), -1)),
    )
