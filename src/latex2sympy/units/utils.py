import sympy.physics.units as sympy_units
from latex2sympy.utils.expression import is_or_contains_instance
from latex2sympy.units.unit_definitions import sievert
from latex2sympy.units.unit_aliases import UNIT_ALIASES
from latex2sympy.units.prefixes import PREFIX_ALIASES
from latex2sympy.units.sie import SIE


def find_prefix(text):
    possible_prefix = text.replace('\\: ', '').strip()
    if possible_prefix in PREFIX_ALIASES:
        return PREFIX_ALIASES[possible_prefix]
    return None


def find_unit(text):
    possible_alias = text.replace('\\: ', '').strip()
    if possible_alias in UNIT_ALIASES:
        return UNIT_ALIASES[possible_alias]
    return None


def is_unit(expr):
    '''
    Check if the expr is or contains a `Quantity`
    '''
    return is_or_contains_instance(expr, sympy_units.Quantity)


def convert_to(expr, target_units):
    '''
    Convert the given expr to the target units using the "SI Extended" unit system.

    If not able to convert, expr is returned unchanged.
    '''
    # do not convert gray with sievert
    if expr == sympy_units.gray and target_units == sievert or expr == sievert and target_units == sympy_units.gray:
        return expr
    return sympy_units.convert_to(expr, target_units, SIE)
