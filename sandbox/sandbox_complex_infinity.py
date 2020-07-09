from sympy import *
from latex2sympy import process_sympy
from math import isclose
import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


#
# Complex Infinity, large numbers, doit(), and evalf()
#

# print(process_sympy('\\tilde{\\infty}'))

# latex = '1.44431744348608\\times 10^521725'
# ans = process_sympy(latex)
# print(ans)
# print(srepr(ans))

# ans_eval = ans.doit(deep=False).evalf(chop=True)
# print(ans_eval)
# print(srepr(ans_eval))

# print('==', ans_eval == c_ans)
# print('isclose', isclose(ans_eval, c_ans))


examples = [
    ('\\frac{\\variable{A}}{\\variable{B}}', {'A': '1', 'B': '0'}),

    ('\\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\lim _{x\\to 1 }(x^2-1)/(x-1)', {}),

    ('\\lim _{x\\to 1 }(x^2-1)/(x-1) + \\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} \\cdot \\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} + \\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} \\cdot \\lim _{x\\to 1 }(x^2-1)/(x-1)', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} + \\lim _{x\\to 1 }(x^2-1)/(x-1)', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} + \\lim _{x\\to 1 }(x^2-1)/(x-1) + \\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\frac{1}{0} \\cdot \\lim _{x\\to 1 }(x^2-1)/(x-1) \\cdot \\variable{b}^{\\variable{c}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),
]

for (latex, variables) in examples:
    print()
    print('latex: ', latex)
    print('variables: ', variables)

    expr = process_sympy(latex, variables)
    print('expr: ', expr)
    print('srepr(expr): ', srepr(expr))

    ans = None
    try:
        with time_limit(3):
            ans = expr.doit().evalf(chop=True)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: doit().evalf() timed out!')

    if ans is not None and (ans.is_Number or ans.is_infinite):
        print('SUCCESS: doit().evalf() worked!')
        continue

    try:
        with time_limit(3):
            ans = expr.doit(deep=False).evalf(chop=True)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: doit(deep=False).evalf() timed out!')

    if ans is not None and (ans.is_Number or ans.is_infinite):
        print('SUCCESS: doit(deep=False).evalf() worked!')
        continue

    try:
        with time_limit(3):
            ans = expr.evalf(chop=True).doit()
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: evalf().doit() timed out!')

    if ans is not None and (ans.is_Number or ans.is_infinite):
        print('SUCCESS: evalf().doit() worked!')
        continue

    try:
        with time_limit(3):
            ans = expr.evalf(chop=True).doit(deep=False)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: evalf().doit(deep=False) timed out!')

    if ans is not None and (ans.is_Number or ans.is_infinite):
        print('SUCCESS: evalf().doit(deep=False) worked!')
        continue
