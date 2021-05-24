from sympy import *
from itertools import product
from latex2sympy import process_sympy


def replace_rationals(expr, replacement):
    new_expr = expr

    # recurse args, if any
    if hasattr(expr, 'args') and len(expr.args) > 0:
        new_args = []

        for arg in expr.args:
            if len(arg.args) > 0:
                new_arg = replace_rationals(arg, replacement)
                new_args.append(new_arg)
            elif isinstance(arg, Rational):
                # negative numbers or subtracting is Mul(-1, number)
                # ignore negative signs
                if isinstance(expr, Mul) and arg == -1:
                    continue
                new_args.append(replacement)
            else:
                new_args.append(arg)

        # has_replacement = False
        # final_args = []
        # for arg in new_args:
        #     if arg == replacement:
        #         if has_replacement:
        #             continue
        #         has_replacement = True
        #     final_args.append(arg)

        # if len(final_args) == 1 and final_args[0] == replacement:
        #     return replacement

        try:
            new_expr = new_expr.func(*new_args, evaluate=False)
        except TypeError as e:
            new_expr = new_expr.func(*new_args)

    return new_expr


def find_symbols(expr):
    symbols = {}

    # recurse args, if any
    if hasattr(expr, 'args') and len(expr.args) > 0:
        for arg in expr.args:
            if len(arg.args) > 0:
                new_symbols = find_symbols(arg)
                symbols = {**symbols, **new_symbols}
            elif isinstance(arg, Symbol):
                symbols[arg] = True

    return symbols


def evaluate(expr, subs):
    try:
        return expr.evalf(subs=subs)
    except Exception as e:
        return 'ERROR'


def get_sample_diff(expr1, expr2):
    symbols_1 = find_symbols(expr1)
    symbols_2 = find_symbols(expr2)

    if symbols_2.keys() != symbols_1.keys():
        return 'ERROR'

    sample_values = [
        # -100,
        # -1,
        0,
        1,
        100
    ]
    values_per_symbol = []
    symbols_list = []
    for symbol in symbols_1.keys():
        symbols_list.append(symbol)
        values_per_symbol.append(sample_values)

    values_product = list(product(*values_per_symbol))

    results_1 = []
    results_2 = []
    for combination in values_product:
        subs = {}
        for i in range(len(combination)):
            symbol = symbols_list[i]
            subs[symbol] = combination[i]
        result_1 = evaluate(expr1, subs)
        result_2 = evaluate(expr2, subs)
        if result_1 == 'ERROR' or result_2 == 'ERROR':
            return 'ERROR'
        results_1.append(result_1)
        results_2.append(result_2)

    error_percentage = 100 * abs(sum(results_1) - sum(results_2)) / sum(results_1)

    return error_percentage


def compare(correct_answer, student_answer):
    print('correct_answer (c): ', correct_answer)
    print('student_answer (a): ', student_answer)
    print('')

    correct_answer_parsed = process_sympy(correct_answer)
    student_answer_parsed = process_sympy(student_answer)

    # print('Double Equals (c == a) =>', correct_answer_parsed == student_answer_parsed)
    # print('')

    equals_diff = factor_terms(simplify(correct_answer_parsed - student_answer_parsed), radical=True)
    equals_result = correct_answer_parsed.equals(student_answer_parsed)
    print('Symbolic using .equals(), (c.equals(a)) =>', equals_result)
    print('\tdiff =>', equals_diff)
    print('')

    simplify_result = simplify(correct_answer_parsed - student_answer_parsed)
    print('Symbolic using simplify(), (simplify(c - a) == 0) =>', simplify_result == 0)
    print('\tsimplified =>', simplify_result)
    print('')

    sample_result = get_sample_diff(correct_answer_parsed, student_answer_parsed)
    print('Sampled =>', sample_result)
    print('')

    c_rep = srepr(correct_answer_parsed)
    a_rep = srepr(student_answer_parsed)
    print('Form and Symbolic using srepr(), (srepr(c) == srepr(a)) =>', c_rep == a_rep)
    print('\tsrepr(c) =>', c_rep)
    print('\tsrepr(a) =>', a_rep)
    print('')

    r = Symbol('replacement', real=True, positive=True)
    correct_answer_replaced = replace_rationals(correct_answer_parsed, r)
    student_answer_replaced = replace_rationals(student_answer_parsed, r)

    print('Double Equals w/o Rationals (replace_rationals(c) == replace_rationals(a)) =>', correct_answer_replaced == student_answer_replaced)
    print('\treplace_rationals(c):', correct_answer_replaced)
    print('\treplace_rationals(a):', student_answer_replaced)
    print('')

    print('.equals() w/o Rationals (replace_rationals(c).equals(replace_rationals(a))) =>', correct_answer_replaced.equals(student_answer_replaced))
    print('')

    print('String Rep w/o Rationals - String Rep (srepr(replace_rationals(c)) == srepr(replace_rationals(a))) =>', srepr(correct_answer_replaced) == srepr(student_answer_replaced))
    print('\tsrepr(replace_rationals(c)):', srepr(correct_answer_replaced))
    print('\tsrepr(replace_rationals(a)):', srepr(student_answer_replaced))

    print('-----------------------------------------------------')


#
# Equality Testing
#

answer_sets = [
    {
        'correct_answer': '(x-y)(x+2y)',
        'student_answers': [
            'x^2+xy-2y^2',
            '(x-y)(x+2y)',
            '(x+2y)(x-y)',
            '(2\\times y+x)(-y+x)',
            '(y\\cdot 2+x)(-y+x)'
        ]
    },
    {
        'correct_answer': '2\\pi \\variable{r}^2',
        'student_answers': [
            '2\\pi \\variable{r}^2',
            '\\pi 2\\variable{r}^2',
            '2\\times \\pi \\times \\variable{r}^2',
            '2\\pi \\variable{r} \\times \\variable{r}'
        ]
    },
    {
        'correct_answer': '2x - 3y',
        'student_answers': [
            '-3y + 2x'
        ]
    },
    {
        'correct_answer': 'x\\times x',
        'student_answers': [
            'x\\times x',
            'x\\cdot x',
            'x^2',
            '(\\sqrt{x})^{4}'
        ]
    },
    {
        'correct_answer': '23e^{-1\\times \\sqrt{t^2}}',
        'student_answers': [
            '23e^{-t}'
        ]
    },
    {
        'correct_answer': 'a=x^2+1',
        'student_answers': [
            'x^2+1=a'
        ]
    },
    {
        'correct_answer': '99.9x',
        'student_answers': [
            '99.86x'
        ]
    },
    {
        'correct_answer': '\\frac{(1+1)\\cdot (100-20-5\\cdot w_t)+0.8\\cdot (340-5-1\\cdot w_c)}{(1+1)\\cdot (1+3)-0.8\\cdot 0.8}',
        'student_answers': [
            '\\frac{428 - 0.8w_c - 10w_t}{7.36}',
            '\\frac{2675}{46} - \\frac{5}{46}w_c - \\frac{125}{92}w_t',
            '58.15220 - 0.1087w_c - 1.3587w_t'
        ]
    },
    {
        'correct_answer': '\\frac{2675}{46} - \\frac{5}{46}w_c - \\frac{125}{92}w_t',
        'student_answers': [
            # '\\frac{(1+1)\\cdot (100-20-5\\cdot w_t)+0.8\\cdot (340-5-1\\cdot w_c)}{(1+1)\\cdot (1+3)-0.8\\cdot 0.8}',
            # '\\frac{428 - 0.8w_c - 10w_t}{7.36}',
            '58.15220 - 0.1087w_c - 1.3587w_t',
            '58.15220 - 1.3587w_t - 0.1087w_c',
            # '58.15220 - 0.1087w_c - 1.3587w_t + x',
            # '58.15220 - 0.1087w_c + x',
            # '58.15220 - 0.1087w_c'
        ]
    }
]

for answer_set in answer_sets:
    correct_answer = answer_set['correct_answer']
    for student_answer in answer_set['student_answers']:
        compare(correct_answer, student_answer)
