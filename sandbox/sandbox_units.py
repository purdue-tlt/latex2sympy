from latex2sympy.latex2sympy import process_sympy
from sympy import srepr, simplify, Mul
from sympy.physics.units import convert_to

unit_examples = [
    ({'value': '1000', 'unit': 'g'}, {'value': '1,000', 'unit': 'g'}, True),
    ({'value': '1.5', 'unit': 'kg'}, {'value': '1.5E3', 'unit': 'grams'}, True),
    ({'value': '1000', 'unit': 'g'}, {'value': '1', 'unit': 'kg'}, True),
    ({'value': '18.36', 'unit': 'mA'}, {'value': '0.01836', 'unit': 'A'}, True),
    ({'value': '18.36', 'unit': 'mA'}, {'value': '0.01836', 'unit': 'amperes'}, True),
    ({'value': '15', 'unit': 'N'}, {'value': '15', 'unit': 'kg\\times \\frac{m}{s^{2}}'}, True),
    ({'value': '1.34', 'unit': 'Hz'}, {'value': '1.34', 'unit': 's^{-1}'}, True),
    ({'value': '50.1', 'unit': 'W'}, {'value': '50.1', 'unit': 'kg*m^{2}s^{-3}'}, True),
    ({'value': '1.34+\\imaginaryJ 3.2', 'unit': 'V'}, {'value': '1.34E3+\\imaginaryJ 3.2E3', 'unit': 'mV'}, True),
]

for unit_example in unit_examples:
    c = unit_example[0]
    a = unit_example[1]
    expected_are_equal = unit_example[2]

    c_str = c.get('value')
    c_val = process_sympy(c_str)
    c_unit_str = c.get('unit')
    c_unit = process_sympy(c_unit_str, parse_letters_as_units=True)
    c_expr = Mul(c_val, c_unit, evaluate=False)
    print('c:', c_str, c_unit_str, '=>', srepr(c_expr))

    a_str = a.get('value')
    a_val = process_sympy(a_str)
    a_unit_str = a.get('unit')
    a_unit = process_sympy(a_unit_str, parse_letters_as_units=True)
    a_expr = Mul(a_val, a_unit, evaluate=False)
    print('a:', a_str, a_unit_str, '=>', srepr(a_expr))
    print('')

    are_equal = simplify(c_expr - a_expr) == 0
    print('are_equal (simplify):', are_equal)
    print('')

    # if a_unit == c_unit or are_equal:
    #     print('------------------------------------------------------------------')
    #     continue

    converted_a_expr = convert_to(a_expr, c_unit)
    if len(converted_a_expr.args) > 2:
        converted_a_expr = Mul(simplify(converted_a_expr.args[0] * converted_a_expr.args[1]), converted_a_expr.args[2], evaluate=False)
    print('convert a to c’s unit:', srepr(converted_a_expr))
    print('')

    # c_min = c_val * 0.98
    # c_max = c_val * 1.02
    # s_1 = simplify(converted_a_expr.args[0] >= c_min)
    # s_2 = simplify(converted_a_expr.args[0] <= c_max)
    # print('within range:', s_1 and s_2)

    are_equal = simplify(c_expr - converted_a_expr) == 0
    print('are_equal converted (simplify):', are_equal)
    print('are_equal == expected:', are_equal == expected_are_equal)
    print('------------------------------------------------------------------')
