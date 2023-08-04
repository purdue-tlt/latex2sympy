from .context import assert_equal, _Add, _Mul, _Eq, x, y
import pytest
from sympy import Integral, sin, Symbol


theta = Symbol('theta', real=True, positive=True)


func_arg_examples = [
    ('\\int ', 'x\\differentialD x', Integral(x, x)),
    ('\\sin', '\\theta ', sin(theta))
]

example_groups = [
    ('1+2', '3-4', _Mul(_Add(1, 2), _Add(3, _Mul(-1, 4))))
]

example_relation_lists = [
    ('x=1', 'y=2', [_Eq(x, 1), _Eq(y, 2)])
]

func_modifiable_delimiter_pairs = {
    '(': ')',
    '\\lgroup ': '\\rgroup ',
    '\\{': '\\}',
    '\\lbrace ': '\\rbrace ',
    '[': ']',
    '\\lbrack ': '\\rbrack ',
}

delimiter_pairs = {
    '{': '}',
    **func_modifiable_delimiter_pairs
}


@pytest.mark.parametrize('func, args, output', func_arg_examples)
def test_func_arg_groupings(func, args, output):
    # none
    assert_equal("{func} {args}".format(func=func, args=args), output)
    # normal brace (not modifiable)
    assert_equal("{func}{{{args}}}".format(func=func, args=args), output)
    # rest of delimiters, with modifications
    for left, right in func_modifiable_delimiter_pairs.items():
        assert_equal("{func}{left}{args}{right}".format(left=left, right=right, func=func, args=args), output)
        assert_equal("{func}\\left{left}{args}\\right{right}".format(left=left, right=right, func=func, args=args), output)
        assert_equal("{func}\\mleft{left}{args}\\mright{right}".format(left=left, right=right, func=func, args=args), output)


@pytest.mark.parametrize('group1, group2, output', example_groups)
def test_delimiter_groupings(group1, group2, output):
    for left, right in delimiter_pairs.items():
        assert_equal("{left}{group1}{right}{left}{group2}{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\left{left}{group1}\\right{right}\\left{left}{group2}\\right{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\mleft{left}{group1}\\mright{right}\\mleft{left}{group2}\\mright{right}".format(left=left, right=right, group1=group1, group2=group2), output)


@pytest.mark.parametrize('group1, group2, output', example_relation_lists)
def test_delimiter_relation_lists(group1, group2, output):
    for left, right in delimiter_pairs.items():
        assert_equal("{left}{group1},{group2}{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("{left}{group1};{group2}{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\left{left}{group1},{group2}\\right{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\left{left}{group1};{group2}\\right{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\mleft{left}{group1},{group2}\\mright{right}".format(left=left, right=right, group1=group1, group2=group2), output)
        assert_equal("\\mleft{left}{group1};{group2}\\mright{right}".format(left=left, right=right, group1=group1, group2=group2), output)
