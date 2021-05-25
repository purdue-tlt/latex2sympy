from .context import assert_equal, get_min_max_examples
import pytest
from sympy import Min


def _Min(*args):
    return Min(*args, evaluate=False)


examples = get_min_max_examples('\\min', _Min)


@pytest.mark.parametrize('input, output', examples)
def test_min(input, output):
    assert_equal(input, output)
