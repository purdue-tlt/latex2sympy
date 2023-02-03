from .context import assert_equal
import pytest
from sympy import MatMul, Matrix, MatAdd


def test_linalg_placeholder():
    assert_equal(
        "\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}\\cdot\\variable{v}",
        MatMul(Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {
            'v': Matrix([1, 2])
        }
    )


def test_linalg_placeholder_multiple():
    assert_equal(
        "\\variable{M}\\cdot\\variable{v}",
        MatMul(Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {
            'M': Matrix([[1, 2], [3, 4]]),
            'v': Matrix([1, 2])
        }
    )


def test_linalg_placeholder_multiple_mul():
    assert_equal(
        "\\begin{pmatrix}3&-1\\end{pmatrix}\\cdot\\variable{M}\\cdot\\variable{v}",
        MatMul(Matrix([[3, -1]]), Matrix([[1, 2], [3, 4]]), Matrix([1, 2]), evaluate=False),
        {
            'M': Matrix([[1, 2], [3, 4]]),
            'v': Matrix([1, 2])
        }
    )


def test_linalg_add_flat():
    assert_equal(
        "\\begin{pmatrix}1&2\\end{pmatrix} + \\begin{pmatrix}3&4\\end{pmatrix} + \\begin{pmatrix}5&6\\end{pmatrix}",
        MatAdd(Matrix([[1, 2]]), Matrix([[3, 4]]), Matrix([[5, 6]]), evaluate=False)
    )


def test_linalg_add_flat_lh_not_add():
    assert_equal(
        "\\begin{pmatrix}1&2\\end{pmatrix} + (3 * \\begin{pmatrix}3&4\\end{pmatrix} + \\begin{pmatrix}5&6\\end{pmatrix})",
        MatAdd(Matrix([[1, 2]]), MatMul(3, Matrix([[3, 4]]), evaluate=False), Matrix([[5, 6]]), evaluate=False)
    )
