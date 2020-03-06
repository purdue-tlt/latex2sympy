from sympy import Symbol, sympify, simplify, Eq, factor, srepr, pi, Number, Mul, Pow, Integer, Float, N, Rational, Add, sin, latex
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
# Zeroes, Infinity, doit(), and evalf()
#


examples = [
    ('\\frac{\\variable{A}}{\\variable{B}}', {'A': '2', 'B': '0'}),

    ('\\sin \\mleft(\\variable{a}\\mright)+\\left(\\frac{\\variable{b}}{\\variable{c}}\\cdot \\pi \\right)+\\variable{b}^{\\variable{c}}\\cdot \\sqrt{\\variable{a}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),

    ('\\lim _{x\\to 1 }(x^2-1)/(x-1)', {}),

    ('\\lim _{x\\to 1 }(x^2-1)/(x-1) + \\sin \\mleft(\\variable{a}\\mright)+\\left(\\frac{\\variable{b}}{\\variable{c}}\\cdot \\pi \\right)+\\variable{b}^{\\variable{c}}\\cdot \\sqrt{\\variable{a}}', {'a': process_sympy('853.5764'), 'b': process_sympy('658.95998'), 'c': process_sympy('185,083.8060')}),
]

for (latex, variables) in examples:
    print()
    print('latex: ', latex)
    print('variables: ', variables)

    expr = process_sympy(latex, variables)
    # print('expr: ', expr)
    # print('srepr(expr): ', srepr(expr))

    ans = None
    try:
        with time_limit(5):
            ans = expr.doit().evalf(chop=True)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: doit().evalf() timed out!')

    if ans is not None:
        print('SUCCESS: doit().evalf() worked!')
        continue

    try:
        with time_limit(5):
            ans = expr.doit(deep=False).evalf(chop=True)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: doit(deep=False).evalf() timed out!')

    if ans is not None:
        print('SUCCESS: doit(deep=False).evalf() worked!')
        continue

    try:
        with time_limit(5):
            ans = expr.evalf(chop=True).doit()
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: evalf().doit() timed out!')

    if ans is not None:
        print('SUCCESS: evalf().doit() worked!')
        continue

    try:
        with time_limit(5):
            ans = expr.evalf(chop=True).doit(deep=False)
            print('ans: ', ans)
            print('srepr(ans): ', srepr(ans))
    except TimeoutException as e:
        print('ERROR: evalf().doit(deep=False) timed out!')

    if ans is not None:
        print('SUCCESS: evalf().doit(deep=False) worked!')
        continue


#
# Number Testing
#

# latex = '14.0,6.0,6.0'
# print(process_sympy(latex))
# print(process_sympy(latex) - process_sympy(latex))
# print(srepr(process_sympy(latex)))

# c_ans = Float('4.21972215369185e+521726', 15)
# print(c_ans)
# print(srepr(c_ans))

# print('==', ans == c_ans)
# print('isclose', isclose(ans, c_ans))

# numeric_responses = ['1', '1.0', '-1', '-1.0', '.5', '-.5', '3x10^3', '3E3', '3,000x10^{-3}', '0.5E-1', '\\frac{1}{3}', '(5\\times 3)^3', '\\sin(1)']
# for latex in numeric_responses:
#     parsed = process_sympy(latex)
#     print('latex: ', latex)
#     print('sympy: ', parsed)
#     print('is_number: ', parsed.is_number)
#     print('is_Number: ', parsed.is_Number)
#     print('srepr: ', srepr(parsed))
#     print('-----------------------------------------------------')

#
# Equality Testing
#

# answer_sets = [
#     # {
#     #     'correct_answer': '(x-y)(x+2y)',
#     #     'student_answers': [
#     #         'x^2+xy-2y^2',
#     #         '(x-y)(x+2y)',
#     #         '(x+2y)(x-y)',
#     #         '(2\\times y+x)(-y+x)',
#     #         '(y\\cdot 2+x)(-y+x)'
#     #     ]
#     # },
#     # {
#     #     'correct_answer': '2\\pi \\variable{r}^2',
#     #     'student_answers': [
#     #         '2\\pi \\variable{r}^2',
#     #         '\\pi 2\\variable{r}^2',
#     #         '2\\times \\pi \\times \\variable{r}^2',
#     #         '2\\pi \\variable{r} \\times \\variable{r}'
#     #     ]
#     # },
#     # {
#     #     'correct_answer': '2x - 3y',
#     #     'student_answers': [
#     #         '-3y + 2x'
#     #     ]
#     # },
#     # {
#     #     'correct_answer': 'x\\times x',
#     #     'student_answers': [
#     #         'x\\times x',
#     #         'x\\cdot x',
#     #         'x^2',
#     #         '(\\sqrt{x})^{4}'
#     #     ]
#     # },
#     # {
#     #     'correct_answer': '23e^{-1\\times \\sqrt{t^2}}',
#     #     'student_answers': [
#     #         '23e^{-t}'
#     #     ]
#     # }
#     {
#         'correct_answer': 'a=x^2+1',
#         'student_answers': [
#             'x^2+1=a'
#         ]
#     }
# ]

# for answer_set in answer_sets:
#     correct_answer = answer_set['correct_answer']
#     correct_answer_parsed = process_sympy(answer_set['correct_answer'])
#     for student_answer in answer_set['student_answers']:
#         student_answer_parsed = process_sympy(student_answer)
#         print('correct_answer (c): ', correct_answer, correct_answer_parsed)
#         print('student_answer (a): ', student_answer, student_answer_parsed)
#         print('')
#         print('Expression Tree (srepr(c) == srepr(a)) =>', srepr(correct_answer_parsed) == srepr(student_answer_parsed))
#         print('srepr(c) =>', srepr(correct_answer_parsed))
#         print('srepr(a) =>', srepr(student_answer_parsed))
#         print('')
#         # print('Structural (c == a) =>', correct_answer_parsed == student_answer_parsed)
#         print('Symbolic (simplify(c - s) == 0) =>', simplify(correct_answer_parsed - student_answer_parsed) == 0)
#         print('simplified =>', simplify(correct_answer_parsed - student_answer_parsed))
#         print('')
#         print('Numeric Substitution (c.equals(s)) =>', correct_answer_parsed.equals(student_answer_parsed))
#         print('-----------------------------------------------------')
