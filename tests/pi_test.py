from .context import assert_equal
import pytest
from sympy import pi, Symbol

def test_pi_frac():
	assert_equal("\\frac{\\pi}{3}", pi/3)
def test_pi_nested():
	assert_equal("\\arccos{\\cos{\\frac{\\pi}{3}}}", pi/3)
def test_pi_arccos():
	assert_equal("\\arccos{-1}", pi)
