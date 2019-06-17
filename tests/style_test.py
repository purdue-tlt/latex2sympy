from .context import assert_equal
import pytest
from sympy import Symbol, sin

x = Symbol('x', real=True)
y = Symbol('y', real=True)

# stripping style function
def test_strip_style():
	assert_equal("\\mathit{x}", x)
def test_strip_style_expr():
	assert_equal("\\mathbf{x + y}", x + y)
def test_strip_style_numeric():
	assert_equal("\\mathsf{21}", 21)

# stripping style function with arguments
def test_strip_style_arg():
	assert_equal("\\fontfamily{cmr}{x}", x)
def test_strip_style_arg_expr():
	assert_equal("\\fontseries{m}{x + y}", x + y)
def test_strip_style_arg_numeric():
	assert_equal("\\textcolor{#CC2428}{21}", 21)

# stripping style inline commands
def test_strip_style_inline():
	assert_equal("{\\tiny x}", x)
def test_strip_style_inline_expr():
	assert_equal("{\\LARGE x + y}", x + y)
def test_strip_style_inline_numeric():
	assert_equal("{\\Huge 21}", 21),

def test_strip_style_partial_math():
	assert_equal("\\mathrm{\\sin }x", sin(x)),