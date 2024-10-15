from sympy import (
    acos,
    acosh,
    acot,
    acsc,
    asec,
    asin,
    asinh,
    atan,
    atanh,
    cos,
    cosh,
    cot,
    csc,
    sec,
    sin,
    sinh,
    tan,
    tanh,
)

from .context import assert_equal


def test_trig():
    assert_equal("\\sin{0}", sin(0, evaluate=False))
    assert_equal("\\cos{0}", cos(0, evaluate=False))
    assert_equal("\\tan{0}", tan(0, evaluate=False))
    assert_equal("\\sec{0}", sec(0, evaluate=False))
    assert_equal("\\csc{0}", csc(0, evaluate=False))
    assert_equal("\\cot{0}", cot(0, evaluate=False))


def test_inverse():
    assert_equal("\\arcsin{-1}", asin(-1, evaluate=False))
    assert_equal("\\arccos{-1}", acos(-1, evaluate=False))
    assert_equal("\\arctan{-1}", atan(-1, evaluate=False))
    # not supported by mathlive
    assert_equal("\\arccsc{-1}", acsc(-1, evaluate=False))
    assert_equal("\\arcsec{-1}", asec(-1, evaluate=False))
    # supported by mathlive
    # assert_equal("\\arcctg{-1}", acot(-1, evaluate=False))
    assert_equal("\\arccot{-1}", acot(-1, evaluate=False))


def test_hyperbolic():
    assert_equal("\\sinh{-1}", sinh(-1, evaluate=False))
    assert_equal("\\cosh{-1}", cosh(-1, evaluate=False))
    assert_equal("\\tanh{-1}", tanh(-1, evaluate=False))
    # not supported by mathlive
    # assert_equal("\\csch{-1}", csch(-1, evaluate=False))
    # assert_equal("\\sech{-1}", sech(-1, evaluate=False))
    # supported by mathlive
    # assert_equal("\\coth{-1}", coth(-1, evaluate=False))


def test_inverse_hyperbolic_arc_length():
    assert_equal("\\operatorname{arcsinh}\\mleft(0 \\mright)", asinh(0, evaluate=False))
    assert_equal("\\operatorname{arccosh}\\mleft(0 \\mright)", acosh(0, evaluate=False))
    assert_equal("\\operatorname{arctanh}\\mleft(0 \\mright)", atanh(0, evaluate=False))


def test_inverse_hyperbolic_area():
    assert_equal("\\operatorname{arsinh}\\mleft(0 \\mright)", asinh(0, evaluate=False))
    assert_equal("\\operatorname{arcosh}\\mleft(0 \\mright)", acosh(0, evaluate=False))
    assert_equal("\\operatorname{artanh}\\mleft(0 \\mright)", atanh(0, evaluate=False))
