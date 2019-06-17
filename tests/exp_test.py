from .context import assert_equal
import pytest
from sympy import exp, sin, Symbol

x = Symbol('x', real=True)
y = Symbol('y', real=True)

def test_exp():
	assert_equal("e", exp(1))
def test_exp_func():
	assert_equal("\\exp(3)", exp(3))
def test_exp_func_no_delim():
	assert_equal("\\exp3", exp(3))
def test_exp_command():
	assert_equal("\\exponentialE(3)", exp(3))
def test_exp_numeric():
	assert_equal("e^3", exp(3))
def test_exp_symbol():
	assert_equal("e^x", exp(x))
def test_exp_symbol_expr():
	assert_equal("e^{x+y}", exp(x+y))
def test_exp_symbol_expr_group():
	assert_equal("e^{(x+y)}", exp(x+y))
def test_exp_expr():
	assert_equal("\\sin(x)*e^x", sin(x)*exp(x))
