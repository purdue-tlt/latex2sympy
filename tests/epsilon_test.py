from sympy import Symbol

from tests.context import assert_equal

x = Symbol('x', real=True)
y = Symbol('y', real=True)


def test_epsilon_letter():
    assert_equal("\\variable{x}\\leq\\variable{y}", (
            Symbol('x', real=True) >= Symbol(
        'y', real=True)))


# def test_epsilon_digit():
#     assert_equal("\\variable{1}", Symbol('1' + hashlib.md5('1'.encode()).hexdigest(), real=True))

res = test_epsilon_letter()
print(res)
