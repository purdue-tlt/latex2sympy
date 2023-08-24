from .context import _Mul, _Pow, assert_equal
from latex2sympy.latex2sympy import create_prefixed_unit
import pytest
from sympy import Symbol
import sympy.physics.units as sympy_physics_units
from sympy.physics.units.prefixes import PREFIXES


unit_examples = [
    # si units
    ('g', sympy_physics_units.g),
    ('kg', sympy_physics_units.kg),
    ('A', sympy_physics_units.A),
    # si units by name
    ('grams', sympy_physics_units.g),
    ('ampere', sympy_physics_units.A),
    # si units by latex
    ('\\Omega', sympy_physics_units.ohm),
    ('\\mu g', sympy_physics_units.microgram),
    # si units with prefixes that are not pre-defined
    ('mV', create_prefixed_unit(sympy_physics_units.V, PREFIXES['m'])),
    ('millivolt', create_prefixed_unit(sympy_physics_units.V, PREFIXES['m'])),
    ('\\mu \\Omega ', create_prefixed_unit(sympy_physics_units.ohm, PREFIXES['mu'])),
    # compound si units
    ('kg\\times \\frac{m}{s^{2}}', _Mul(sympy_physics_units.kg, sympy_physics_units.m, _Pow(_Pow(sympy_physics_units.s, 2), -1))),
    ('kg*m^{2}s^{-3}', _Mul(sympy_physics_units.kg, _Pow(sympy_physics_units.m, 2), _Pow(sympy_physics_units.s, -3))),
    # do not allow constants
    ('c', Symbol('c', real=True, positive=True)),
    # non si-units
    ('apples', Symbol('apples', real=True, positive=True)),
    ('apples\\times grams', _Mul(Symbol('apples', real=True, positive=True), sympy_physics_units.g)),
]


@pytest.mark.parametrize('input, output', unit_examples)
def test_covert_unit(input, output):
    assert_equal(input, output, parse_letters_as_units=True)
