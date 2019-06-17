import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from latex2sympy.latex2sympy import process_sympy
from sympy import simplify

def compare(actual, expected):
	if isinstance(expected,(list,)):
		check = expected == actual
		if check:
			value = 0
		else:
			value = 1
	else:
		value = expected - actual
		value_simp = simplify(value)
	assert actual == expected or value == 0 or value_simp == 0

def assert_equal(latex, expr, placeholder_values = {}, linalg = False):
	parsed = process_sympy(latex, placeholder_values, linalg)
	compare(parsed, expr)