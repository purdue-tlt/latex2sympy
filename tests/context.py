from sympy import simplify, srepr, Add, Mul, Pow
from latex2sympy import process_sympy
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# shorthand definitions


def _Add(a, b):
    return Add(a, b, evaluate=False)


def _Mul(a, b):
    return Mul(a, b, evaluate=False)


def _Pow(a, b):
    return Pow(a, b, evaluate=False)


def compare(actual, expected, symbolically=False):
    if symbolically:
        assert simplify(actual - expected) == 0
    else:
        actual_exp_tree = srepr(actual)
        expected_exp_tree = srepr(expected)
        try:
            assert actual_exp_tree == expected_exp_tree
        except Exception:
            if isinstance(actual, int) or isinstance(actual, float) or actual.is_number and isinstance(expected, int) or isinstance(expected, float) or expected.is_number:
                assert actual == expected or actual - expected == 0 or simplify(actual - expected) == 0
            else:
                print('expected_exp_tree = ', expected_exp_tree)
                print('actual exp tree = ', actual_exp_tree)
                raise


def assert_equal(latex, expr, variable_values={}, symbolically=False):
    parsed = process_sympy(latex, variable_values)
    compare(parsed, expr, symbolically)
