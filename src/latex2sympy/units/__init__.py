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
