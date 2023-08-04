from latex2sympy.latex2sympy import process_sympy
from sympy import srepr, simplify
from sympy.physics.units import convert_to, Quantity


def find_unit(expr):
    if expr is None:  # pragma: no cover
        return None
    if isinstance(expr, Quantity):
        return expr
    if not hasattr(expr, 'args') or len(expr.args) <= 0:  # pragma: no cover
        return None
    for arg in expr.args:
        if find_unit(arg) is not None:
            return arg
    return None


unit_examples = [
    ('1000\\g ', '1\\kg ', True),
    ('18.36\\mA ', '0.01836\\A ', True)
]

for unit_example in unit_examples:
    c_str = unit_example[0]
    a_str = unit_example[1]
    expected_are_equal = unit_example[2]

    c = process_sympy(c_str)
    print('c:', c_str, '=>', srepr(c))

    a = process_sympy(a_str)
    print('a:', a_str, '=>', srepr(a))
    print('')

    c_unit = find_unit(c)

    converted_a = convert_to(a, c_unit)
    print('convert a to c’s unit:', srepr(converted_a))
    print('')

    are_equal = simplify(c - converted_a) == 0
    print('are_equal:', are_equal)
    print('are_equal == expected:', are_equal == expected_are_equal)
    print('------------------------------------------------------------------')
