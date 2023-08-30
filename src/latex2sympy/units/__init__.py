from sympy.physics.units.prefixes import prefix_unit
from latex2sympy.units.aliases import UNIT_ALIASES, PREFIX_ALIASES


def create_prefixed_unit(unit, prefix):
    '''
    combine the prefix and unit into a new `Quantity`
    '''
    # `prefix_unit` accepts a dict of prefixes, so construct one
    prefixes = {}
    prefixes[prefix.abbrev] = prefix
    prefixed_units = prefix_unit(unit, prefixes)
    return prefixed_units[0]


def find_unit(text):
    possible_alias = text.replace('\\: ', '').strip()
    if possible_alias in UNIT_ALIASES:
        return UNIT_ALIASES[possible_alias]
    return None
