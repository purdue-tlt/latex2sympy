import sympy.physics.units as sympy_units
import latex2sympy.units.additional_units as additional_units
from latex2sympy.units.units import UNIT_ALIASES
from latex2sympy.units.prefixes import PREFIX_ALIASES, create_prefixed_unit
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


def is_or_contains_instance(expr, type):
    '''
    Determine if the expression `expr` is or contains an instance of `type`
    '''
    if expr is None:  # pragma: no cover
        return False
    if isinstance(expr, type):
        return True
    if not hasattr(expr, 'args') or len(expr.args) <= 0:  # pragma: no cover
        return False

    for arg in expr.args:
        if is_or_contains_instance(arg, type):
            return True

    return False


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
    if expr == sympy_units.gray and target_units == additional_units.sievert or\
            expr == additional_units.sievert and target_units == sympy_units.gray:
        return expr
    return sympy_units.convert_to(expr, target_units, SIE)
