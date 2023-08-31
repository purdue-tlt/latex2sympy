from sympy import Symbol
from sympy.physics.units import Quantity
from latex2sympy.units.units import UNIT_ALIASES
from latex2sympy.units.prefixes import PREFIX_ALIASES, create_prefixed_unit


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
    return is_or_contains_instance(expr, Quantity)
