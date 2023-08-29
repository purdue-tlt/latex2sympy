import sympy
import sympy.physics.units as sympy_physics_units
from sympy.physics.units.prefixes import prefix_unit
from sympy.physics.units.quantities import PhysicalConstant, Quantity
from latex2sympy.definitions.units import UNIT_PREFIXES, ADDITIONAL_UNITS, ADDITIONAL_UNIT_ALIASES, ALLOWED_CONSTANTS, ADDITIONAL_PREFIX_ALIASES


def get_prefix_matches(text, exact=False):
    '''
    check if the `text` starts with any prefixes, by name, abbrev, or latex.

    checks for exact matches if `exact` is True.

    returns any matches in descending length order.
    '''
    prefix_matches = []
    for prefix in UNIT_PREFIXES:
        prefix_name = str(prefix.name)
        prefix_abbrev = str(prefix.abbrev)
        prefix_latex = sympy.latex(prefix)
        if text == prefix_name if exact else text.startswith(prefix_name):
            prefix_matches.append((prefix, len(prefix_name)))
        elif text == prefix_abbrev if exact else text.startswith(prefix_abbrev):
            prefix_matches.append((prefix, len(prefix_abbrev)))
        elif text == prefix_latex if exact else text.startswith(prefix_latex):
            prefix_matches.append((prefix, len(prefix_latex)))
        if prefix in ADDITIONAL_PREFIX_ALIASES:
            for additional_prefix_alias in ADDITIONAL_PREFIX_ALIASES[prefix]:
                if text == additional_prefix_alias if exact else text.startswith(additional_prefix_alias):
                    prefix_matches.append((prefix, len(additional_prefix_alias)))
    prefix_matches.sort(key=lambda m: m[1], reverse=True)
    return prefix_matches


def create_prefixed_unit(unit, prefix):
    '''
    combine the prefix and unit into a new `Quantity`
    '''
    # `prefix_unit` accepts a dict of prefixes, so construct one
    prefixes = {}
    prefixes[prefix.abbrev] = prefix
    prefixed_units = prefix_unit(unit, prefixes)
    return prefixed_units[0]


def convert_unit(text):
    unit = None
    unit_matches = []

    text = text.replace('\\: ', '')

    # check if a unit matches using additional aliases
    if text in ADDITIONAL_UNIT_ALIASES:
        return ADDITIONAL_UNIT_ALIASES[text]

    # check if a unit matches using additional units
    for u in ADDITIONAL_UNITS:
        if text == str(u.name) or text == str(u.abbrev) or text == sympy.latex(u):
            return u

    # check if a unit matches the given text
    try:
        unit_matches = sympy_physics_units.find_unit(text)
    except AttributeError as e:
        # no matches will throw an AttributeError

        # check if a unit matches using its default latex representation
        for i in dir(sympy_physics_units):
            attr = getattr(sympy_physics_units, i)
            if isinstance(attr, Quantity) and sympy.latex(attr) == text:
                unit_matches.append(i)

        # if no match is found, try to account for prefixes
        if len(unit_matches) == 0:
            # check if the text starts with any prefixes, by name, abbrev, or latex
            prefix_matches = get_prefix_matches(text)
            # return if no prefixes were found
            if len(prefix_matches) == 0:
                return None

            # find the first valid prefix + unit match, if any
            for prefix_match in prefix_matches:
                prefix = prefix_match[0]
                prefix_len = prefix_match[1]
                # check if the remaining text after the prefix is a valid unit
                unit = convert_unit(text[prefix_len:].strip())
                if unit is None:
                    continue
                return create_prefixed_unit(unit, prefix)

    # if matches are found, return the first matching unit
    if len(unit_matches) > 0:
        unit_key = unit_matches[0]
        unit = getattr(sympy_physics_units, unit_key)

    # do not allow constants
    if unit is not None and isinstance(unit, PhysicalConstant) and unit not in ALLOWED_CONSTANTS:
        return None

    return unit
