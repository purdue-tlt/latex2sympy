import pytest
from sympy import Max

from .context import assert_equal, get_min_max_examples


def _Max(*args):
    return Max(*args, evaluate=False)


examples = get_min_max_examples('\\max', _Max)


@pytest.mark.parametrize('input, output', examples)
def test_max(input, output):
    assert_equal(input, output)
