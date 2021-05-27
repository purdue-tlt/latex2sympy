from .context import assert_equal, get_gcd_lcm_examples
import pytest
from sympy import UnevaluatedExpr, lcm, ilcm


def _lcm(*args):
    return UnevaluatedExpr(lcm(*args))


def _ilcm(*args):
    return UnevaluatedExpr(ilcm(*args))


cmd_examples = get_gcd_lcm_examples('\\lcm', _lcm, lcm, _ilcm)
operatorname_examples = get_gcd_lcm_examples('\\operatorname{lcm}', _lcm, lcm, _ilcm)


@pytest.mark.parametrize('input, output', cmd_examples)
def test_lcm_cmd(input, output):
    assert_equal(input, output)


@pytest.mark.parametrize('input, output', operatorname_examples)
def test_lcm_operatorname(input, output):
    assert_equal(input, output)
