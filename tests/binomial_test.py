from .context import process_sympy
import pytest
from sympy import binomial, Symbol

x = Symbol('x', real=True)
y = Symbol('y', real=True)
theta = Symbol('theta', real=True)
gamma = Symbol('gamma', real=True)

class TestBinomial():
	def test_binomial_numeric(self):
		assert process_sympy("\\binom{16}{2}") == binomial(16,2)
	def test_binomial_symbols(self):
		assert process_sympy("\\binom{x}{y}") == binomial(x,y)
	def test_binomial_greek_symbols(self):
		assert process_sympy("\\binom{\\theta}{\\gamma}") == binomial(theta,gamma)
	def test_binomial_expr(self):
		assert process_sympy("\\binom{16+2}{\\frac{4}{2}}") == binomial(16+2,4/2)
	def test_choose_numeric(self):
		assert process_sympy("\\choose{16}{2}") == binomial(16,2)
	def test_choose_symbols(self):
		assert process_sympy("\\choose{x}{y}") == binomial(x,y)
	def test_choose_greek_symbols(self):
		assert process_sympy("\\choose{\\theta}{\\gamma}") == binomial(theta,gamma)