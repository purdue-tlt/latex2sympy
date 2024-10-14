from latex2sympy.latex2sympy import process_sympy
from latex2sympy.units import convert_to
from sympy import im, Mul, re, simplify, srepr

unit_examples = [
    ({'value': '1000', 'unit': 'g'}, {'value': '1,000', 'unit': 'g'}),
    ({'value': '1.5', 'unit': 'kg'}, {'value': '1.5E3', 'unit': 'grams'}),
    ({'value': '1000', 'unit': 'g'}, {'value': '1', 'unit': 'kg'}),
    ({'value': '18.36', 'unit': 'mA'}, {'value': '0.01836', 'unit': 'A'}),
    ({'value': '18.36', 'unit': 'mA'}, {'value': '0.01836', 'unit': 'amperes'}),
    ({'value': '15', 'unit': 'N'}, {'value': '15', 'unit': 'kg\\times \\frac{m}{s^{2}}'}),
    ({'value': '1.34', 'unit': 'Hz'}, {'value': '1.34', 'unit': 's^{-1}'}),
    ({'value': '50.1', 'unit': 'W'}, {'value': '50.1', 'unit': 'kg*m^{2}s^{-3}'}),
    ({'value': '1.34+\\imaginaryJ 3.2', 'unit': 'V'}, {'value': '1.34E3+\\imaginaryJ 3.2E3', 'unit': 'mV'}),
    # ({'value': '100', 'unit': 'apples'}, {'value': '1E2', 'unit': 'apples'}),
    ({'value': '100', 'unit': 's'}, {'value': '1E2', 'unit': 'g'}),
    ({'value': '999', 'unit': 'g'}, {'value': '1', 'unit': 'kg'}),
    ({'value': '1', 'unit': 'degC'}, {'value': '1', 'unit': 'degF'}),
]

for unit_example in unit_examples:
    c = unit_example[0]
    a = unit_example[1]

    c_str = c.get('value')
    c_val = process_sympy(c_str)
    c_unit_str = c.get('unit')
    c_unit = process_sympy(c_unit_str, parse_as_unit=True)
    c_expr = Mul(c_val, c_unit, evaluate=False)
    print('c:', c_str, c_unit_str, '=>', srepr(c_expr))

    a_str = a.get('value')
    a_val = process_sympy(a_str)
    a_unit_str = a.get('unit')
    a_unit = process_sympy(a_unit_str, parse_as_unit=True)
    a_expr = Mul(a_val, a_unit, evaluate=False)
    print('a:', a_str, a_unit_str, '=>', srepr(a_expr))
    print('')

    are_equal_values = c_val == a_val
    print('are_equal values (c == a):', are_equal_values)
    are_equal_units = c_unit == a_unit
    print('are_equal units (c == a):', are_equal_units)
    # are_equal = simplify(c_expr - a_expr) == 0
    # print('are_equal (simplify(c - a) == 0):', are_equal)
    print('')

    if are_equal_values and are_equal_units:
        print('------------------------------------------------------------------')
        continue

    a_converted = convert_to(a_expr, c_unit)
    # simplify the numeric value
    # `convert_to` sometimes adds a multiplication factor, e.g. with complex number values
    if len(a_converted.args) > 2:
        a_converted = Mul(simplify(a_converted.args[0] * a_converted.args[1]), a_converted.args[2], evaluate=False)
    print('try convert a to c’s unit')
    if a_expr == a_converted:
        print('could not convert')
        print('------------------------------------------------------------------')
        continue
    print('a_converted:', srepr(a_converted))
    print('')

    a_converted_val = a_converted.args[0]
    a_converted_unit = a_converted.args[1]
    are_equal_values = (
        re(c_val) == re(a_converted_val) and im(c_val) == im(a_converted_val)
        if c_val.is_complex
        else c_val == a_converted_val
    )
    print('are_equal values (c == a_converted):', are_equal_values)
    are_equal_units = c_unit == a_converted_unit
    print('are_equal units (c == a_converted):', are_equal_units)
    # are_equal = simplify(c_expr - a_converted) == 0
    # print('are_equal (simplify(c - a_converted) == 0):', are_equal)

    if are_equal_values and are_equal_units:
        print('------------------------------------------------------------------')
        continue

    print('')
    c_min = c_val * 0.98
    c_max = c_val * 1.02
    s_1 = simplify(a_converted.args[0] >= c_min)
    s_2 = simplify(a_converted.args[0] <= c_max)
    print('use 2% tolerance range:', [c_min, c_max])
    print('are_equal using range:', s_1 and s_2)
    print('------------------------------------------------------------------')
