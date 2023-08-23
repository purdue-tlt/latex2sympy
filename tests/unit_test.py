from .context import _Mul, _Pow, assert_equal
import pytest
from sympy import Symbol
import sympy.physics.units as sympy_physics_units

unit_examples = [
    # si units
    ('g', sympy_physics_units.g),
    ('kg', sympy_physics_units.kg),
    ('A', sympy_physics_units.A),
    # si units by name
    ('grams', sympy_physics_units.g),
    ('ampere', sympy_physics_units.A),
    # TODO si units by latex
    # ('\\Omega', sympy_physics_units.ohm),
    # compound si units
    ('kg\\times \\frac{m}{s^{2}}', _Mul(sympy_physics_units.kg, sympy_physics_units.m, _Pow(_Pow(sympy_physics_units.s, 2), -1))),
    ('kg*m^{2}s^{-3}', _Mul(sympy_physics_units.kg, _Pow(sympy_physics_units.m, 2), _Pow(sympy_physics_units.s, -3))),
    # non si-units
    ('c', Symbol('c', real=True)),
    ('apples', Symbol('apples', real=True)),
]


@pytest.mark.parametrize('input, output', unit_examples)
def test_covert_unit(input, output):
    assert_equal(input, output, parse_letters_as_units=True)
