import pytest
from sympy import floor

from .context import assert_equal, get_simple_examples


def _floor(*args):
    return floor(*args, evaluate=False)


examples = get_simple_examples(_floor)


@pytest.mark.parametrize('input, output', examples)
def test_floor_func(input, output):
    assert_equal("\\floor({input})".format(input=input), output)


@pytest.mark.parametrize('input, output', examples)
def test_floor_operatorname(input, output):
    assert_equal("\\operatorname{{floor}}({input})".format(input=input), output)


@pytest.mark.parametrize('input, output', examples)
def test_floor_cmd(input, output):
    assert_equal("\\lfloor {input}\\rfloor".format(input=input), output)
    assert_equal("\\left\\lfloor {input}\\right\\rfloor".format(input=input), output)
    assert_equal("\\mleft\\lfloor {input}\\mright\\rfloor".format(input=input), output)


@pytest.mark.parametrize('input, output', examples)
def test_floor_corners(input, output):
    assert_equal("\\llcorner {input}\\lrcorner".format(input=input), output)
    assert_equal("\\left\\llcorner {input}\\right\\lrcorner".format(input=input), output)
    assert_equal("\\mleft\\llcorner {input}\\mright\\lrcorner".format(input=input), output)
