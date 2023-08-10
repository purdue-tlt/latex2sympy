from .context import assert_equal, process_sympy, _Add, _Mul, _Pow
import pytest
import hashlib
from sympy import (
    E, I, oo, pi, sqrt, root, Symbol, Add, Mul, Pow, Abs, factorial, log, Eq, Ne, S, Rational, Integer, UnevaluatedExpr,
    sin, cos, tan, sinh, cosh, tanh, asin, acos, atan, asinh, acosh, atanh,
    csc, sec, Sum, Product, Limit, Integral, Derivative,
    LessThan, StrictLessThan, GreaterThan, StrictGreaterThan,
    exp, binomial, Matrix, MatMul, MatAdd,
    Mod, gcd, lcm, floor, ceiling, Max, Min
)

x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, positive=True)
z = Symbol('z', real=True, positive=True)
a = Symbol('a', real=True, positive=True)
b = Symbol('b', real=True, positive=True)
c = Symbol('c', real=True, positive=True)
f = Symbol('f', real=True, positive=True)
t = Symbol('t', real=True, positive=True)
k = Symbol('k', real=True, positive=True)
n = Symbol('n', real=True, positive=True)
alpha = Symbol('alpha', real=True, positive=True)
theta = Symbol('theta', real=True, positive=True)

# shorthand definitions


def _Abs(a):
    return Abs(a, evaluate=False)


def _factorial(a):
    return factorial(a, evaluate=False)


def _log(a, b):
    return log(a, b, evaluate=False)


def pytest_generate_tests(metafunc):
    metafunc.parametrize('s, eq', metafunc.cls.GOOD_PAIRS)


class TestAllGood(object):
    # These latex strings should parse to the corresponding SymPy expression
    GOOD_PAIRS = [
        ("0", Rational(0)),
        ("1", Rational(1)),
        ("-3.14", Rational(-314, 100)),
        ("5-3", _Add(5, _Mul(-1, 3))),
        ("(-7.13)(1.5)", _Mul(Rational('-7.13'), Rational('1.5'))),
        ("\\left(-7.13\\right)\\left(1.5\\right)", _Mul(Rational('-7.13'), Rational('1.5'))),
        ("x", x),
        ("2x", 2 * x),
        ("x^2", x**2),
        ("x^\\alpha ", _Pow(x, alpha)),
        ("x^{3 + 1}", x**_Add(3, 1)),
        ("x^{\\left\\{3 + 1\\right\\}}", x**_Add(3, 1)),
        ("-3y + 2x", _Add(_Mul(2, x), Mul(-1, 3, y, evaluate=False))),
        ("-c", -c),
        ("a \\cdot b", a * b),
        ("a / b", a / b),
        ("a \\div b", a / b),
        # add
        ("a + b", a + b),
        # add_flat
        ("(b * c + a) + (2c + x)", Add(_Mul(b, c), a, _Mul(2, c), x, evaluate=False)),
        ("(b * c) + (2c + x)", Add(_Mul(b, c), _Mul(2, c), x, evaluate=False)),
        ("a + b - a", Add(a, b, _Mul(-1, a), evaluate=False)),
        ("a^2 + b^2 = c^2", Eq(a**2 + b**2, c**2)),
        ("a^2 + b^2 != 2c^2", Ne(a**2 + b**2, 2 * c**2)),
        ("a\\mod b", Mod(a, b)),
        ("\\sin 2\\cdot \\theta ", sin(_Mul(2, theta))),
        ("\\sin \\theta ", sin(theta)),
        ("\\sin(\\theta )", sin(theta)),
        ("\\sin \\left(\\theta \\right)", sin(theta)),
        ("\\sin ^{-1} a", asin(a)),
        ("\\sin a \\cos b", _Mul(sin(a), cos(b))),
        ("\\sin \\cos \\theta ", sin(cos(theta))),
        ("\\sin \\cos(\\theta )a", sin(_Mul(cos(theta), a), evaluate=False)),
        ("\\sin(\\cos \\theta )", sin(cos(theta))),
        ("\\sin -a", sin(_Mul(-1, a), evaluate=False)),
        ("\\sin +a", sin(a, evaluate=False)),
        ("\\sin x(y)^{2}", sin(_Mul(x, _Pow(y, 2)), evaluate=False)),
        ("\\sin x(y)^\\theta ", sin(_Mul(x, _Pow(y, theta)), evaluate=False)),
        ("\\arcsin(a)", asin(a)),
        ("\\arccos(a)", acos(a)),
        ("\\arctan(a)", atan(a)),
        ("\\sinh(a)", sinh(a)),
        ("\\cosh(a)", cosh(a)),
        ("\\tanh(a)", tanh(a)),
        ("\\sinh ^{-1}(a)", asinh(a)),
        ("\\cosh ^{-1}(a)", acosh(a)),
        ("\\tanh ^{-1}(a)", atanh(a)),
        ("\\arcsinh(a)", asinh(a)),
        ("\\arccosh(a)", acosh(a)),
        ("\\arctanh(a)", atanh(a)),
        ("\\arsinh(a)", asinh(a)),
        ("\\arcosh(a)", acosh(a)),
        ("\\artanh(a)", atanh(a)),
        ("\\operatorname{arcsinh}(a)", asinh(a)),
        ("\\operatorname{arccosh}(a)", acosh(a)),
        ("\\operatorname{arctanh}(a)", atanh(a)),
        ("\\operatorname{arsinh}(a)", asinh(a)),
        ("\\operatorname{arcosh}(a)", acosh(a)),
        ("\\operatorname{artanh}(a)", atanh(a)),
        ("\\operatorname{gcd}(a, b)", UnevaluatedExpr(gcd(a, b))),
        ("\\operatorname{lcm}(a, b)", UnevaluatedExpr(lcm(a, b))),
        ("\\operatorname{gcd}(a,b)", UnevaluatedExpr(gcd(a, b))),
        ("\\operatorname{lcm}(a,b)", UnevaluatedExpr(lcm(a, b))),
        ("\\operatorname{floor}(a)", floor(a)),
        ("\\operatorname{ceil}(b)", ceiling(b)),
        ("\\cos ^2(x)", cos(x)**2),
        ("\\cos ^\\theta (x)", cos(x)**theta),
        ("\\cos ^\\theta ^\\alpha (x)", cos(x)**theta**alpha),
        ("\\cos (x)^2", cos(x)**2),
        ("\\gcd (a,b)", UnevaluatedExpr(gcd(a, b))),
        ("\\gcd ^2(a,b)", _Pow(UnevaluatedExpr(gcd(a, b)), 2)),
        ("\\gcd ^\\theta (a,b)", _Pow(UnevaluatedExpr(gcd(a, b)), theta)),
        ("\\lcm (a,b)", UnevaluatedExpr(lcm(a, b))),
        ("\\gcd (a,b)", UnevaluatedExpr(gcd(a, b))),
        ("\\lcm (a,b)", UnevaluatedExpr(lcm(a, b))),
        ("\\floor (a)", floor(a)),
        ("\\ceil (b)", ceiling(b)),
        ("\\max (a,b)", Max(a, b)),
        ("\\min (a,b)", Min(a, b)),
        ("\\frac{a}{b}", a / b),
        ("\\frac{a+b}{c}", _Mul(a + b, _Pow(c, -1))),
        ("\\frac{7}{3}", Rational(7, 3)),
        ("(\\csc x)(\\sec y)", csc(x) * sec(y)),
        ("\\lim _{x \\to 3}a", Limit(a, x, 3)),
        ("\\lim _{x \\rightarrow 3}a", Limit(a, x, 3)),
        ("\\lim _{x \\Rightarrow 3}a", Limit(a, x, 3)),
        ("\\lim _{x \\longrightarrow 3}a", Limit(a, x, 3)),
        ("\\lim _{x \\Longrightarrow 3}a", Limit(a, x, 3)),
        ("\\lim _{x \\to 3^{+}}a", Limit(a, x, 3, dir='+')),
        ("\\lim _{x \\to 3^{-}}a", Limit(a, x, 3, dir='-')),
        ("\\lim _{\\theta \\to 3}a", Limit(a, theta, 3)),
        # without spaces
        ("\\infty", oo),
        ("\\infty\\%", oo),
        ("\\$\\infty", oo),
        ("-\\infty", -oo),
        ("-\\infty\\%", -oo),
        ("-\\$\\infty", -oo),
        # with spaces
        ("\\infty ", oo),
        ("\\infty \\%", oo),
        ("\\$\\infty ", oo),
        ("-\\infty ", -oo),
        ("-\\infty \\%", -oo),
        ("-\\$\\infty ", -oo),
        ("\\lim _{x\\to \\infty }\\frac{1}{x}", Limit(_Mul(1, _Pow(x, -1)), x, oo)),
        ("\\frac{\\differentialD }{\\differentialD x}x", Derivative(x, x)),
        ("\\frac{\\differentialD }{\\differentialD t}x", Derivative(x, t)),
        ("\\frac{\\differentialD y}{\\differentialD t}x", _Mul(x, Derivative(y, t))),
        # ("f(x)", f(x)),
        # ("f(x, y)", f(x, y)),
        # ("f(x, y, z)", f(x, y, z)),
        # ("\\frac{d f(x)}{\\differentialD x}", Derivative(f(x), x)),
        # ("\\frac{d\\theta(x)}{\\differentialD x}", Derivative(theta(x), x)),
        ("|x|", _Abs(x)),
        ("\\left|x\\right|", _Abs(x)),
        ("||x||", _Abs(_Abs(x))),
        ("|x||y|", _Abs(x) * _Abs(y)),
        ("||x||y||", _Abs(_Abs(x) * _Abs(y))),
        ("\\lfloor x\\rfloor ", floor(x)),
        ("\\lceil y\\rceil ", ceiling(y)),
        ("\\pi ^{|xy|}", pi**_Abs(x * y)),
        ("\\frac{\\pi}{3}", _Mul(pi, _Pow(3, -1))),
        ("\\sin{\\frac{\\pi }{2}}", sin(_Mul(pi, _Pow(2, -1)), evaluate=False)),
        ("a+b\\imaginaryI ", a + I * b),
        ("\\exponentialE ^{\\imaginaryI \\pi }", exp(_Mul(I, pi), evaluate=False)),
        ("\\exponentialE ^\\pi ", exp(pi, evaluate=False)),
        ("\\int x\\differentialD x", Integral(x, x)),
        ("\\int x\\differentialD \\theta ", Integral(x, theta)),
        ("\\int (x^2 - y)\\differentialD x", Integral(x**2 - y, x)),
        ("\\int x+a\\differentialD x", Integral(_Add(x, a), x)),
        ("\\int \\differentialD a", Integral(1, a)),
        ("\\int _0^7 \\differentialD x", Integral(1, (x, 0, 7))),
        ("\\int _a^b x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int ^b_a x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int _{a}^b x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int ^{b}_a x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int _{a}^{b} x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int _{  }^{}x \\differentialD x", Integral(x, x)),
        ("\\int ^{  }_{ }x \\differentialD x", Integral(x, x)),
        ("\\int ^{b}_{a} x \\differentialD x", Integral(x, (x, a, b))),
        ("\\int ^\\alpha _\\theta  x \\differentialD x", Integral(x, (x, theta, alpha))),
        # ("\\int_{f(a)}^{f(b)} f(z) dz", Integral(f(z), (z, f(a), f(b)))),
        ("\\int (x+a)", Integral(_Add(x, a), x)),
        ("\\int a + b + c \\differentialD x", Integral(Add(a, b, c, evaluate=False), x)),
        ("\\int \\frac{\\differentialD z}{z}", Integral(Pow(z, -1), z)),
        ("\\int \\frac{\\differentialD \\theta }{\\theta }", Integral(Pow(theta, -1), theta)),
        ("\\int \\frac{3\\differentialD z}{z}", Integral(3 * Pow(z, -1), z)),
        ("\\int \\frac{1}{x}\\differentialD x", Integral(_Mul(1, Pow(x, -1)), x)),
        ("\\int \\frac{1}{a}+\\frac{1}{b} \\differentialD x", Integral(_Add(_Mul(1, _Pow(a, -1)), _Mul(1, Pow(b, -1))), x)),
        ("\\int \\frac{3 \\cdot \\differentialD \\theta }{\\theta }", Integral(3 * _Mul(1, _Pow(theta, -1)), theta)),
        ("\\int \\frac{1}{x}+1\\differentialD x", Integral(_Add(_Mul(1, _Pow(x, -1)), 1), x)),
        ("x_0", Symbol('x_0', real=True, positive=True)),
        ("x_{1}", Symbol('x_1', real=True, positive=True)),
        ("x_a", Symbol('x_a', real=True, positive=True)),
        ("x_{b}", Symbol('x_b', real=True, positive=True)),
        ("h_\\theta", Symbol('h_{\\theta}', real=True, positive=True)),
        ("h_\\theta ", Symbol('h_{\\theta}', real=True, positive=True)),
        ("h_{\\theta}", Symbol('h_{\\theta}', real=True, positive=True)),
        # ("h_{\\theta}(x_0, x_1)", Symbol('h_{theta}', real=True)(Symbol('x_{0}', real=True), Symbol('x_{1}', real=True))),
        ("x!", _factorial(x)),
        ("100!", _factorial(100)),
        ("\\theta !", _factorial(theta)),
        ("(x+1)!", _factorial(_Add(x, 1))),
        ("\\left(x+1\\right)!", _factorial(_Add(x, 1))),
        ("(x!)!", _factorial(_factorial(x))),
        ("x!!!", _factorial(_factorial(_factorial(x)))),
        ("5!7!", _Mul(_factorial(5), _factorial(7))),
        ("a|^{a=1}", Integer(1)),
        ("a|^{5*2}", a),
        ("a|^{a*5*2}", _Mul(a, 5, 2)),
        ("a|^{a=5*2}", _Mul(5, 2)),
        ("a|_{a=5*2}", _Mul(5, 2)),
        ("ab|^{b=5*2}_{b=1}", _Mul(a, _Add(_Mul(5, 2), _Mul(1, -1)))),
        ("\\sqrt{x}", sqrt(x)),
        ("\\sqrt{x+b}", sqrt(_Add(x, b))),
        ("\\sqrt[3]{\\sin x}", root(sin(x), 3)),
        ("\\sqrt[y]{\\sin x}", root(sin(x), y)),
        ("\\sqrt[\\theta ]{\\sin x}", root(sin(x), theta)),
        ("x<y", StrictLessThan(x, y)),
        ("x\\leq y", LessThan(x, y)),
        ("x>y", StrictGreaterThan(x, y)),
        ("x\\geq y", GreaterThan(x, y)),
        ("\\sum _{k=1}^{3}c", Sum(c, (k, 1, 3))),
        ("\\sum _{k=1}^3c", Sum(c, (k, 1, 3))),
        ("\\sum _{k=1}^\\theta c", Sum(c, (k, 1, theta))),
        ("\\sum ^{3}_{k=1}c", Sum(c, (k, 1, 3))),
        ("\\sum ^3_{k=1}c", Sum(c, (k, 1, 3))),
        ("\\sum _{k=1}^{10}k^2", Sum(k**2, (k, 1, 10))),
        ("\\sum _{n=0}^{\\infty }\\frac{1}{n!}", Sum(_Mul(1, _Pow(_factorial(n), -1)), (n, 0, oo))),
        ("\\prod _{a=b}^{c} x", Product(x, (a, b, c))),
        ("\\prod _{a=b}^c x", Product(x, (a, b, c))),
        ("\\prod ^{c}_{a=b} x", Product(x, (a, b, c))),
        ("\\prod ^c_{a=b} x", Product(x, (a, b, c))),
        ("\\ln x", _log(x, E)),
        ("\\ln xy", _log(x * y, E)),
        ("\\log x", _log(x, 10)),
        ("\\log xy", _log(x * y, 10)),
        ("\\log _\\theta x", _log(x, theta)),
        ("\\log _{2} x", _log(x, 2)),
        ("\\log _ax", _log(x, a)),
        ("\\log _{a}x", _log(x, a)),
        ("\\log _{11}x", _log(x, 11)),
        ("\\log _{a^2}x", _log(x, _Pow(a, 2))),
        ("[x]", x),
        ("[a+b]", _Add(a, b)),
        ("\\frac{\\differentialD }{\\differentialD x}[\\tan x]", Derivative(tan(x), x)),
        ("2\\overline{x}", 2 * Symbol('xbar', real=True, positive=True)),
        ("2\\overline{x}_n", 2 * Symbol('xbar_n', real=True, positive=True)),
        ("\\frac{x}{\\overline{x}_n}", x / Symbol('xbar_n', real=True, positive=True)),
        ("\\frac{\\sin (x)}{\\overline{x}_n}", sin(x) / Symbol('xbar_n', real=True, positive=True)),
        ("2\\bar{x}", 2 * Symbol('xbar', real=True, positive=True)),
        ("2\\bar{x}_n", 2 * Symbol('xbar_n', real=True, positive=True)),
        ("\\sin\\left(\\theta \\right) \\cdot4", sin(theta) * 4),
        ("\\ln \\left(\\theta \\right)", _log(theta, E)),
        ("\\ln \\left(x-\\theta \\right)", _log(x - theta, E)),
        ("\\ln \\left(\\left(x-\\theta \\right)\\right)", _log(x - theta, E)),
        ("\\ln \\left(\\left[x-\\theta \\right]\\right)", _log(x - theta, E)),
        ("\\ln \\left(\\left\\{x-\\theta \\right\\}\\right)", _log(x - theta, E)),
        ("\\ln \\left(\\left|x-\\theta \\right|\\right)", _log(_Abs(x - theta), E)),
        ("\\frac{1}{2}xy(x+y)", Mul(Rational(1, 2), x, y, (x + y), evaluate=False)),
        ("\\frac{1}{2}\\theta (x+y)", Mul(Rational(1, 2), theta, (x + y), evaluate=False)),
        ("1-f(x)", 1 - f * x),

        ("\\begin{matrix}1&2\\\\3&4\\end{matrix}", Matrix([[1, 2], [3, 4]])),
        ("\\begin{matrix}x&x^2\\\\\\sqrt{x}&x\\end{matrix}", Matrix([[x, x**2], [_Pow(x, S.Half), x]])),
        ("\\begin{matrix}\\sqrt{x}\\\\\\sin(\\theta)\\end{matrix}", Matrix([_Pow(x, S.Half), sin(theta)])),
        ("\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}", Matrix([[1, 2], [3, 4]])),
        ("\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}", Matrix([[1, 2], [3, 4]])),

        # scientific notation
        ("2.5\\times 10^2", Rational(250)),
        ("1,500\\times 10^{-1}", Rational(150)),

        # e notation
        ("2.5E2", Rational(250)),
        ("1,500E-1", Rational(150)),

        # "E" as a symbol
        ('ER+E_C', Add(Mul(Symbol('E', real=True, positive=True), Symbol('R', real=True, positive=True), evaluate=False), Symbol('E_C', real=True, positive=True), evaluate=False)),

        # multiplication without cmd
        ("2x2y", Mul(2, x, 2, y, evaluate=False)),
        ("2x2", Mul(2, x, 2, evaluate=False)),
        ("x2", x * 2),

        # lin alg processing
        ("\\theta\\begin{matrix}1&2\\\\3&4\\end{matrix}", MatMul(theta, Matrix([[1, 2], [3, 4]]), evaluate=False)),
        ("\\theta\\begin{matrix}1\\\\3\\end{matrix} - \\begin{matrix}-1\\\\2\\end{matrix}", MatAdd(MatMul(theta, Matrix([[1], [3]]), evaluate=False), MatMul(-1, Matrix([[-1], [2]]), evaluate=False), evaluate=False)),
        ("\\theta\\begin{matrix}1&0\\\\0&1\\end{matrix}*\\begin{matrix}3\\\\-2\\end{matrix}", MatMul(theta, Matrix([[1, 0], [0, 1]]), Matrix([3, -2]), evaluate=False)),
        ("\\frac{1}{9}\\theta\\begin{matrix}1&2\\\\3&4\\end{matrix}", MatMul(Rational(1, 9), theta, Matrix([[1, 2], [3, 4]]), evaluate=False)),
        ("\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}", [Matrix([1, 2, 3]), Matrix([4, 3, 1])]),
        ("\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix};\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}", [Matrix([1, 2, 3]), Matrix([4, 3, 1])]),
        ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}\\right\\}", [Matrix([1, 2, 3]), Matrix([4, 3, 1])]),
        ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix},\\begin{pmatrix}1\\\\1\\\\1\\end{pmatrix}\\right\\}", [Matrix([1, 2, 3]), Matrix([4, 3, 1]), Matrix([1, 1, 1])]),
        ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}\\right\\}", Matrix([1, 2, 3])),
        ("\\left{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}\\right}", Matrix([1, 2, 3])),
        ("{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}}", Matrix([1, 2, 3])),

        # us dollars
        ("\\$1,000.00", Rational(1000)),
        ("\\$543.21", Rational(54321, 100)),
        ("\\$0.009", Rational(9, 1000)),

        # percentages
        ("100\\%", Rational(1)),
        ("1.5\\%", Rational(15, 1000)),
        ("0.05\\%", Rational(5, 10000)),

        # empty set
        ("\\emptyset", S.EmptySet),
        ("\\emptyset ", S.EmptySet),

        # divide by zero
        ("\\frac{1}{0}", _Mul(1, _Pow(0, -1))),
        ("1+\\frac{5}{0}", _Add(1, _Mul(5, _Pow(0, -1)))),

        # adjacent single char sub sup
        ("4^26^2", _Mul(_Pow(4, 2), _Pow(6, 2))),
        ("x_22^2", _Mul(Symbol('x_2', real=True, positive=True), _Pow(2, 2))),

        # mathit
        ("\\mathit{a}", Symbol('a', real=True, positive=True))
    ]

    def test_good_pair(self, s, eq):
        assert_equal(s, eq)
