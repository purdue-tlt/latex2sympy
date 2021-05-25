from .context import assert_equal, get_simple_examples
import pytest
from sympy import Abs


def _Abs(*args):
    return Abs(*args, evaluate=False)


examples = get_simple_examples(_Abs)

delimiter_pairs = {
    '|': '|',
    '\\vert': '\\vert',
    '\\lvert': '\\rvert'
}


@pytest.mark.parametrize('input, output', examples)
def test_abs(input, output):
    for left, right in delimiter_pairs.items():
        assert_equal("{left}{input}{right}".format(left=left, right=right, input=input), output)
        assert_equal("\\left{left}{input}\\right{right}".format(left=left, right=right, input=input), output)
        assert_equal("\\mleft{left}{input}\\mright{right}".format(left=left, right=right, input=input), output)
