from sympy import *
# from sympy.abc import x,y,z,a,b,c,f,t,k,n
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)
a = Symbol('a', real=True)
b = Symbol('b', real=True)
c = Symbol('c', real=True)
f = Symbol('f', real=True)
t = Symbol('t', real=True)
k = Symbol('k', real=True)
n = Symbol('n', real=True)

from latex2sympy import process_sympy
import hashlib

theta = Symbol('theta', real=True)

# shorthand definitions
def _Add(a, b):
    return Add(a, b, evaluate=False)
def _Mul(a, b):
    return Mul(a, b, evaluate=False)
def _Pow(a, b):
    return Pow(a, b, evaluate=False)
def _Abs(a):
    return Abs(a, evaluate=False)
def _factorial(a):
    return factorial(a, evaluate=False)
def _log(a, b):
    return log(a, b, evaluate=False)


# These latex strings should parse to the corresponding
# SymPy expression
GOOD_PAIRS = [
    ("0", 0),
    ("1", 1),
    ("-3.14", _Mul(-1, 3.14)),
    ("(-7.13)(1.5)", _Mul(_Mul(-1, 7.13), 1.5)),
    ("\\left(-7.13\\right)\\left(1.5\\right)", _Mul(_Mul(-1, 7.13), 1.5)),
    ("x", x),
    ("2x", 2*x),
    ("x^2", x**2),
    ("x^{3 + 1}", x**_Add(3,1)),
    ("x^{\\left\\{3 + 1\\right\\}}", x**_Add(3,1)),
    ("-c", -c),
    ("a \\cdot b", a * b),
    ("a / b", a / b),
    ("a \\div b", a / b),
    ("a + b", a + b),
    ("a + b - a", _Add(a+b, -a)),
    ("a^2 + b^2 = c^2", Eq(a**2 + b**2, c**2)),
    ("a^2 + b^2 != 2c^2", Ne(a**2 + b**2, 2*c**2)),
    ("\\sin \\theta", sin(theta)),
    ("\\sin(\\theta)", sin(theta)),
    ("\\sin\\left(\\theta\\right)", sin(theta)),
    ("\\sin^{-1} a", asin(a)),
    ("\\sin a \\cos b", _Mul(sin(a), cos(b))),
    ("\\sin \\cos \\theta", sin(cos(theta))),
    ("\\sin(\\cos \\theta)", sin(cos(theta))),
    ("\\arcsin(a)", asin(a)),
    ("\\arccos(a)", acos(a)),
    ("\\arctan(a)", atan(a)),
    ("\\sinh(a)", sinh(a)),
    ("\\cosh(a)", cosh(a)),
    ("\\tanh(a)", tanh(a)),
    ("\\sinh^{-1}(a)", asinh(a)),
    ("\\cosh^{-1}(a)", acosh(a)),
    ("\\tanh^{-1}(a)", atanh(a)),
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
    ("\\cos^2(x)", cos(x)**2),
    ("\\cos(x)^2", cos(x)**2),
    ("\\frac{a}{b}", a / b),
    ("\\frac{a + b}{c}", _Mul(a + b, _Pow(c,-1))),
    ("\\frac{7}{3}", _Mul(7, _Pow(3,-1))),
    ("(\\csc x)(\\sec y)", csc(x)*sec(y)),
    ("\\lim_{x \\to 3} a", Limit(a, x, 3)),
    ("\\lim_{x \\rightarrow 3} a", Limit(a, x, 3)),
    ("\\lim_{x \\Rightarrow 3} a", Limit(a, x, 3)),
    ("\\lim_{x \\longrightarrow 3} a", Limit(a, x, 3)),
    ("\\lim_{x \\Longrightarrow 3} a", Limit(a, x, 3)),
    ("\\lim_{x \\to 3^{+}} a", Limit(a, x, 3, dir='+')),
    ("\\lim_{x \\to 3^{-}} a", Limit(a, x, 3, dir='-')),
    ("\\infty", oo),
    ("\\lim_{x \\to \\infty} \\frac{1}{x}", Limit(_Mul(1, _Pow(x,-1)), x, oo)),
    ("\\frac{d}{dx} x", Derivative(x, x)),
    ("\\frac{d}{dt} x", Derivative(x, t)),
    # ("f(x)", f(x)),
    # ("f(x, y)", f(x, y)),
    # ("f(x, y, z)", f(x, y, z)),
    # ("\\frac{d f(x)}{dx}", Derivative(f(x), x)),
    # ("\\frac{d\\theta(x)}{dx}", Derivative(theta(x), x)),
    ("|x|", _Abs(x)),
    ("\\left|x\\right|", _Abs(x)),
    ("||x||", _Abs(Abs(x))),
    ("|x||y|", _Abs(x)*_Abs(y)),
    ("||x||y||", _Abs(_Abs(x)*_Abs(y))),
    ("\\pi^{|xy|}", pi**_Abs(x*y)),
    ("\\frac{\\pi}{3}", pi/3),
    ("\\sin{\\frac{\\pi}{2}}", sin(pi/2) ),
    ("a+bI", a+I*b ),
    ("e^{I\\pi}", -1 ),
    ("\\int x dx", Integral(x, x)),
    ("\\int x d\\theta", Integral(x, theta)),
    ("\\int (x^2 - y)dx", Integral(x**2 - y, x)),
    ("\\int x + a dx", Integral(_Add(x, a), x)),
    ("\\int da", Integral(1, a)),
    ("\\int_0^7 dx", Integral(1, (x, 0, 7))),
    ("\\int_a^b x dx", Integral(x, (x, a, b))),
    ("\\int^b_a x dx", Integral(x, (x, a, b))),
    ("\\int_{a}^b x dx", Integral(x, (x, a, b))),
    ("\\int^{b}_a x dx", Integral(x, (x, a, b))),
    ("\\int_{a}^{b} x dx", Integral(x, (x, a, b))),
    ("\\int_{  }^{}x dx", Integral(x, x)),
    ("\\int^{  }_{ }x dx", Integral(x, x)),
    ("\\int^{b}_{a} x dx", Integral(x, (x, a, b))),
    # ("\\int_{f(a)}^{f(b)} f(z) dz", Integral(f(z), (z, f(a), f(b)))),
    ("\\int (x+a)", Integral(_Add(x,a), x)),
    ("\\int a + b + c dx", Integral(_Add(_Add(a,b),c), x)),
    ("\\int \\frac{dz}{z}", Integral(Pow(z,-1), z)),
    ("\\int \\frac{3 dz}{z}", Integral(3*Pow(z, -1), z)),
    ("\\int \\frac{1}{x} dx", Integral(Pow(x, -1), x)),
    ("\\int \\frac{1}{a} + \\frac{1}{b} dx", Integral(_Add(_Pow(a,-1), Pow(b,-1)),x)),
    ("\\int \\frac{3 \\cdot d\\theta}{\\theta}", Integral(3*_Pow(theta,-1), theta)),
    ("\\int \\frac{1}{x} + 1 dx", Integral(_Add(_Pow(x, -1), 1), x)),
    ("x_0", Symbol('x_{0}', real=True)),
    ("x_{1}", Symbol('x_{1}', real=True)),
    ("x_a", Symbol('x_{a}', real=True)),
    ("x_{b}", Symbol('x_{b}', real=True)),
    ("h_\\theta", Symbol('h_{theta}', real=True)),
    ("h_{\\theta}", Symbol('h_{theta}', real=True)),
    # ("h_{\\theta}(x_0, x_1)", Symbol('h_{theta}', real=True)(Symbol('x_{0}', real=True), Symbol('x_{1}', real=True))),
    ("x!", _factorial(x)),
    ("100!", _factorial(100)),
    ("\\theta!", _factorial(theta)),
    ("(x + 1)!", _factorial(_Add(x, 1))),
    ("\\left(x + 1\\right)!", _factorial(_Add(x, 1))),
    ("(x!)!", _factorial(_factorial(x))),
    ("x!!!", _factorial(_factorial(_factorial(x)))),
    ("5!7!", _Mul(_factorial(5), _factorial(7))),
    ("\\sqrt{x}", sqrt(x)),
    ("\\sqrt{x + b}", sqrt(_Add(x, b))),
    ("\\sqrt[3]{\\sin x}", root(sin(x), 3)),
    ("\\sqrt[y]{\\sin x}", root(sin(x), y)),
    ("\\sqrt[\\theta]{\\sin x}", root(sin(x), theta)),
    ("x < y", StrictLessThan(x, y)),
    ("x \\leq y", LessThan(x, y)),
    ("x > y", StrictGreaterThan(x, y)),
    ("x \\geq y", GreaterThan(x, y)),
    ("\\sum_{k = 1}^{3} c", Sum(c, (k, 1, 3))),
    ("\\sum_{k = 1}^3 c", Sum(c, (k, 1, 3))),
    ("\\sum^{3}_{k = 1} c", Sum(c, (k, 1, 3))),
    ("\\sum^3_{k = 1} c", Sum(c, (k, 1, 3))),
    ("\\sum_{k = 1}^{10} k^2", Sum(k**2, (k, 1, 10))),
    ("\\sum_{n = 0}^{\\infty} \\frac{1}{n!}", Sum(_Pow(_factorial(n),-1), (n, 0, oo))),
    ("\\prod_{a = b}^{c} x", Product(x, (a, b, c))),
    ("\\prod_{a = b}^c x", Product(x, (a, b, c))),
    ("\\prod^{c}_{a = b} x", Product(x, (a, b, c))),
    ("\\prod^c_{a = b} x", Product(x, (a, b, c))),
    ("\\ln x", _log(x, E)),
    ("\\ln xy", _log(x*y, E)),
    ("\\log x", _log(x, 10)),
    ("\\log xy", _log(x*y, 10)),
    # ("\\log_2 x", _log(x, 2)),
    ("\\log_{2} x", _log(x, 2)),
    # ("\\log_a x", _log(x, a)),
    ("\\log_{a} x", _log(x, a)),
    ("\\log_{11} x", _log(x, 11)),
    ("\\log_{a^2} x", _log(x, _Pow(a, 2))),
    ("[x]", x),
    ("[a + b]", _Add(a, b)),
    ("\\frac{d}{dx} [ \\tan x ]", Derivative(tan(x), x)),
    ("2\\overline{x}", 2*Symbol('xbar', real=True)),
    ("2\\overline{x}_n", 2*Symbol('xbar_{n}', real=True)),
    ("\\frac{x}{\\overline{x}_n}", x/Symbol('xbar_{n}', real=True)),
    ("\\frac{\\sin(x)}{\\overline{x}_n}", sin(Symbol('x', real=True))/Symbol('xbar_{n}', real=True)),
    ("2\\bar{x}", 2*Symbol('xbar', real=True)),
    ("2\\bar{x}_n", 2*Symbol('xbar_{n}', real=True)),
    ("\\sin\\left(\\theta\\right) \\cdot4", sin(theta)*4),
    ("\\ln\\left(\\theta\\right)", _log(theta, E)),
    ("\\ln\\left(x-\\theta\\right)", _log(x-theta, E)),
    ("\\ln\\left(\\left(x-\\theta\\right)\\right)", _log(x-theta, E)),
    ("\\ln\\left(\\left[x-\\theta\\right]\\right)", _log(x-theta, E)),
    ("\\ln\\left(\\left\\{x-\\theta\\right\\}\\right)", _log(x-theta, E)),
    ("\\ln\\left(\\left|x-\\theta\\right|\\right)", _log(_Abs(x-theta), E)),
    ("\\frac{1}{2}xy(x+y)", x*y*(x+y)/2 ),
    ("\\frac{1}{2}\\theta(x+y)", theta*(x+y)/2 ),
    ("1-f(x)", 1-f*x ),
    ("\\binom{16}{2}", binomial(16,2) ),
    ("\\binom{x}{y}", binomial(x,y) ),
    ("\\binom{\\theta}{\\gamma}", binomial(theta,Symbol('gamma', real=True)) ),
    ("\\binom{16+2}{\\frac{4}{2}}", binomial(16+2,4/2) ),
    ("\\choose{16}{2}", binomial(16,2) ),
    ("\\choose{x}{y}", binomial(x,y) ),
    ("\\choose{\\theta}{\\gamma}", binomial(theta,Symbol('gamma', real=True)) ),
    ("\\begin{matrix}1&2\\\\3&4\\end{matrix}", Matrix([[1,2],[3,4]])),
    ("\\begin{matrix}x&x^2\\\\\\sqrt{x}&x\\end{matrix}", Matrix([[x,x**2],[sqrt(x),x]])),
    ("\\begin{matrix}\\sqrt{x}\\\\\\sin(\\theta)\\end{matrix}", Matrix([sqrt(x),sin(theta)])),
    ("\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}", Matrix([[1,2],[3,4]])),
    ("\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}", Matrix([[1,2],[3,4]])),

    # placeholder parsing
    ("[!value_1!]", Symbol('value_1' + hashlib.md5('value_1'.encode()).hexdigest(), real=True)),
    ("4\\cdot[!value_1!]", 4*Symbol('value_1' + hashlib.md5('value_1'.encode()).hexdigest(), real=True)),
    ("4\\cdot[!alpha!]*\\alpha", 4*Symbol('alpha' + hashlib.md5('alpha'.encode()).hexdigest(), real=True)*Symbol('alpha', real=True)),
    ("4\\cdot[!value1!]\\frac{[!value_2!]}{[!a!]}\\cdot x^2", 4*Symbol('value1' + hashlib.md5('value1'.encode()).hexdigest(), real=True)*Symbol('value_2' + hashlib.md5('value_2'.encode()).hexdigest(), real=True)/Symbol('a' + hashlib.md5('a'.encode()).hexdigest(), real=True)*x**2),

    ("\\exp(3)", exp(3)),
    ("\\exp3", exp(3)),
    ("\\exponentialE(3)", exp(3)),

    # e as exponential function
    ("e^3", exp(3)),
    ("e^x", exp(x)),
    ("e^{x+y}", exp(x+y)),
    ("\\sin(x)*e^x", sin(x)*exp(x)),
    ("e",exp(1)),

    # e in scientific e notation
    ("2.5E2", 250),
    ("1,500E-1", 150),

    # stripping style function
    ("\\mathit{x}", x),
    ("\\mathbf{x + y}", x + y),
    ("\\mathsf{21}", 21),

    # stripping style function with arguments
    ("\\fontfamily{cmr}{x}", x),
    ("\\fontseries{m}{x + y}", x + y),
    ("\\textcolor{#CC2428}{21}", 21),

    # stripping style inline commands
    ("{\\tiny x}", x),
    ("{\\LARGE x + y}", x + y),
    ("{\\Huge 21}", 21),

    # lin alg processing
    ("\\theta\\begin{matrix}1&2\\\\3&4\\end{matrix}", MatMul(theta,Matrix([[1,2],[3,4]])) ),
    ("\\theta\\begin{matrix}1\\\\3\\end{matrix} - \\begin{matrix}-1\\\\2\\end{matrix}", MatAdd(MatMul(theta, Matrix([[1],[3]])), -1*Matrix([[-1],[2]]) ) ),
    ("\\theta\\begin{matrix}1&0\\\\0&1\\end{matrix}*\\begin{matrix}3\\\\-2\\end{matrix}", MatMul(MatMul(theta, Matrix([[1,0],[0,1]])), Matrix([3,-2])) ),
    ("\\frac{1}{9}\\theta\\begin{matrix}1&2\\\\3&4\\end{matrix}", MatMul(MatMul(1,Pow(9,-1, evaluate=False), evaluate=False), MatMul(theta, Matrix([[1,2],[3,4]]) ) ) ),
    ("\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}", [Matrix([1,2,3]), Matrix([4,3,1])]),
    ("\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix};\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}", [Matrix([1,2,3]), Matrix([4,3,1])]),
    ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix}\\right\\}", [Matrix([1,2,3]), Matrix([4,3,1])]),
    ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix},\\begin{pmatrix}1\\\\1\\\\1\\end{pmatrix}\\right\\}", [Matrix([1,2,3]), Matrix([4,3,1]), Matrix([1,1,1])]),
    ("\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}\\right\\}", Matrix([1,2,3])),
    ("\\left{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}\\right}", Matrix([1,2,3])),
    ("{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}}", Matrix([1,2,3])),

    # placeholder replacement during latex2sympy with linalg forced
    ("\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\cdot[!v!]", MatMul(Matrix([[1,2],[3,4]]), Matrix([1,2])), {'v': Matrix([1,2])}, True ),
    ("[!M!]\\cdot[!v!]", MatMul(Matrix([[1,2],[3,4]]), Matrix([1,2])), {'M': Matrix([[1,2],[3,4]]), 'v': Matrix([1,2])}, True ),
    ("\\begin{pmatrix}3&-1\\end{pmatrix}\\cdot[!M!]\\cdot[!v!]", MatMul(MatMul(Matrix([[3,-1]]), Matrix([[1,2],[3,4]])), Matrix([1,2])), {'M': Matrix([[1,2],[3,4]]), 'v': Matrix([1,2])}, True ),
]

# These bad latex strings should raise an exception when parsed
BAD_STRINGS = [
    "(",
    ")",
    # "a / b /",
    "\\frac{d}{dx}",
    "(\\frac{d}{dx})"
    "\\sqrt{}",
    "\\sqrt",
    "{",
    "}",
    # "1.1.1",
    "\\mathit{TEST}"
    "\\frac{2}{}",
    "\\frac{}{2}",
    "\\int",
    # "1 +",
    # "a +",
    "!",
    "!0",
    "_",
    "^",
    # "a // b",
    # "a \\cdot \\cdot b",
    # "a \\div \\div b",
    "|",
    "||x|",
    "()",
    "((((((((((((((((()))))))))))))))))",
    "-",
    "\\frac{d}{dx} + \\frac{d}{dt}",
    # "f()",
    # "f(,",
    # "f(x,,y)",
    # "f(x,y,",
    "\\sin^x",
    "\\cos^2",
    # "\\cos 1 \\cos",
    "@","#","$","%","&","*",
    "\\",
    "~",
    "\\frac{(2 + x}{1 - x)}",
    "\\lim_{\\pi \\to 3} a",
    # because mix of COMMA and SEMICOLON
    "\\left\\{\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix},\\begin{pmatrix}4\\\\3\\\\1\\end{pmatrix};\\begin{pmatrix}1\\\\1\\\\1\\end{pmatrix}\\right\\}"
]

total_good = 0
passed_good = 0
total = 0
passed = 0
for s, eq, *args in GOOD_PAIRS:
    # extra settings
    force_linalg = False
    placeholder_values = {}
    if args:
        placeholder_values = args[0] if len(args) > 0 else placeholder_values
        force_linalg = args[1] if len(args) > 1 else force_linalg

    # counters
    total += 1
    total_good += 1
    try:
        parsed = process_sympy(s, placeholder_values, force_linalg)
        if isinstance(eq,(list,)):
            check = eq == parsed
            if check:
                value = 0
            else:
                value = 1
        else:
            value = eq - parsed
            value_simp = simplify(value)

        if parsed != eq and value != 0 and value_simp != 0:
            print("ERROR: \"%s\" did not parse to %s but parsed to %s" % (s, eq, parsed))
            print("diff: %s and simplified: %s" % (value, value_simp))
        else:
            passed += 1
            passed_good += 1
            try:
                subs={x: 1, y: 2, z: 3, a: 4, b: 5, c: 6, f: 7, t: 8, k: 9, n: 10, theta: 3.5}
                # print("%s => %s => %s" % (s, parsed, parsed.evalf(subs=subs)))
            except:
                print("INFO: Parsed successfully, but could not evaluate: \"%s\"" % s)
    except Exception as e:
        print("ERROR: Exception when parsing \"%s\"" % s)
for s in BAD_STRINGS:
    total += 1
    try:
        process_sympy(s)
        print("ERROR: Exception should have been raised for \"%s\"" % s)
    except Exception:
        passed += 1

print("%d/%d GOOD STRINGS PASSED" % (passed_good, total_good))
print("%d/%d STRINGS PASSED" % (passed, total))
if(passed < total):
    raise ValueError('Not all tests passed')
