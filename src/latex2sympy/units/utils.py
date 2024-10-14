import sympy.physics.units as sympy_units

from latex2sympy.units.prefixes import PREFIX_ALIASES
from latex2sympy.units.sie import SIE
from latex2sympy.units.unit_aliases import UNIT_ALIASES
from latex2sympy.units.unit_definitions import gray, sievert
from latex2sympy.utils.expression import is_or_contains_instance


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
    Check if the expr is or contains a `Quantity`.

    A single unit will be `Quantity` object, e.g. `kg`.

    A unit expression will contain a `Quantity`, e.g. `m^{2}`.
    '''
    return is_or_contains_instance(expr, sympy_units.Quantity)


def convert_to(expr, target_units):
    '''
    Convert the given expr to the target units using the "SI Extended" unit system.

    If not able to convert, an exception is raised.
    '''
    # do not convert between gray and sievert, as they measure different kinds of radiation doses
    if expr == gray and target_units == sievert or expr == sievert and target_units == gray:
        raise Exception(f'Could not convert "{str(expr)}" to "{str(target_units)}"')

    converted_expr = sympy_units.convert_to(expr, target_units, SIE)

    # if the expressions are equal, that means they could not convert
    if converted_expr == expr:
        raise Exception(f'Could not convert "{str(expr)}" to "{str(target_units)}"')

    return converted_expr
