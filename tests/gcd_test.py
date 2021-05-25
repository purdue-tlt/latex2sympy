from .context import assert_equal, get_gcd_lcm_examples
import pytest
from sympy import UnevaluatedExpr, gcd, igcd


def _gcd(a, b):
    return UnevaluatedExpr(gcd(a, b))


def _igcd(*args):
    return UnevaluatedExpr(igcd(*args))


cmd_examples = get_gcd_lcm_examples('\\gcd', _gcd, gcd, _igcd)
operatorname_examples = get_gcd_lcm_examples('\\operatorname{gcd}', _gcd, gcd, _igcd)


@pytest.mark.parametrize('input, output', cmd_examples)
def test_gcd_cmd(input, output):
    assert_equal(input, output)


@pytest.mark.parametrize('input, output', operatorname_examples)
def test_gcd_operatorname(input, output):
    assert_equal(input, output)
