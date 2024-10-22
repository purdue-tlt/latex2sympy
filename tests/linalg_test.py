import pytest
from sympy import MatAdd, MatMul, Matrix

from .context import _Pow, assert_equal, process_sympy


def test_linalg_placeholder():
    assert_equal(
        "\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\cdot\\variable{v}",
        MatMul(Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {'v': Matrix([1, 2])},
    )


def test_linalg_placeholder_multiple():
    assert_equal(
        "\\variable{M}\\cdot\\variable{v}",
        MatMul(Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {'M': Matrix([[1, 2], [3, 4]]), 'v': Matrix([1, 2])},
    )


def test_linalg_placeholder_multiple_mul():
    assert_equal(
        "\\begin{pmatrix}3&-1\\end{pmatrix}\\cdot\\variable{M}\\cdot\\variable{v}",
        MatMul(Matrix([[3, -1]]), Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {'M': Matrix([[1, 2], [3, 4]]), 'v': Matrix([1, 2])},
    )


def test_linalg_add_flat_lh_is_add():
    assert_equal(
        "\\begin{pmatrix}1&2\\end{pmatrix} + \\begin{pmatrix}3&4\\end{pmatrix} + \\begin{pmatrix}5&6\\end{pmatrix}",
        MatAdd(Matrix([[1, 2]]), Matrix([[3, 4]]), Matrix([[5, 6]]), evaluate=False),
    )


def test_linalg_add_flat_lh_is_not_add():
    assert_equal(
        "\\begin{pmatrix}1&2\\end{pmatrix} + (3 * \\begin{pmatrix}3&4\\end{pmatrix} + \\begin{pmatrix}5&6\\end{pmatrix})",
        MatAdd(Matrix([[1, 2]]), MatMul(3, Matrix([[3, 4]]), evaluate=False), Matrix([[5, 6]]), evaluate=False),
    )


def test_linalg_divide():
    assert_equal("\\begin{pmatrix}3&4\\end{pmatrix} / 5", MatMul(Matrix([[3, 4]]), _Pow(5, -1), evaluate=False))


def test_linalg_mod_should_fail():
    with pytest.raises(Exception):
        process_sympy("5 \\mod \\begin{pmatrix}3&4\\end{pmatrix}")


def test_linalg_mul_flat_in_unary():
    assert_equal("-\\begin{pmatrix}1&2\\end{pmatrix}", MatMul(-1, Matrix([[1, 2]]), evaluate=False))


def test_linalg_in_frac():
    assert_equal("\\frac{\\begin{pmatrix}1&2\\end{pmatrix}}{5}", MatMul(Matrix([[1, 2]]), _Pow(5, -1), evaluate=False))
