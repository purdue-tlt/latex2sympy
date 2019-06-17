from .context import assert_equal
import pytest
import hashlib
from sympy import Symbol

x = Symbol('x', real=True)

def test_grasple_placeholder():
	assert_equal("[!value!]", Symbol('value' + hashlib.md5('value'.encode()).hexdigest(), real=True))
def test_grasple_placeholder_expr():
	assert_equal("4\\cdot[!value_1!]", 4*Symbol('value_1' + hashlib.md5('value_1'.encode()).hexdigest(), real=True))
def test_grasple_placeholder_with_command():
	assert_equal("4\\cdot[!alpha!]*\\alpha", 4*Symbol('alpha' + hashlib.md5('alpha'.encode()).hexdigest(), real=True)*Symbol('alpha', real=True))
def test_grasple_placeholder_complex():
	assert_equal("4\\cdot[!value1!]\\frac{[!value_2!]}{[!a!]}\\cdot x^2", 4*Symbol('value1' + hashlib.md5('value1'.encode()).hexdigest(), real=True)*Symbol('value_2' + hashlib.md5('value_2'.encode()).hexdigest(), real=True)/Symbol('a' + hashlib.md5('a'.encode()).hexdigest(), real=True)*x**2)