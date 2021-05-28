from .context import assert_equal
import pytest
from sympy import asinh, acos


def test_arcsinh():
    assert_equal("\\operatorname{arcsinh}\\left(1\\right)", asinh(1, evaluate=False))


def test_arccos():
    assert_equal("\\arccos{-1}", acos(-1, evaluate=False))
