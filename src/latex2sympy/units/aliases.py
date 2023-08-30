from sympy import latex
import sympy.physics.units.definitions.unit_definitions as units
from sympy.physics.units.definitions.unit_definitions import (
    second, ampere,
    # Constants
    speed_of_light, electronvolt, atomic_mass_constant,
    # Derived
    minute, hour, year,
    # Other
    pound, inch, bar, degree, percent
)
from sympy.physics.units.quantities import Quantity, PhysicalConstant
from sympy.physics.units.systems.mks import all_units as mks_units
from sympy.physics.units.systems.mksa import all_units as mksa_units
from sympy.physics.units.systems.si import all_units as si_units
from sympy.physics.units.prefixes import PREFIXES, BIN_PREFIXES, micro
import latex2sympy.units.additional_units as additional_units

# `all_units` contains every MKS/MKSA/SI unit and each possible prefixed variation
all_units = [*mks_units, *mksa_units, *si_units]
ALL_PREFIXES = {**PREFIXES, **BIN_PREFIXES}

# construct a dict of every allowed string alias of each prefix
# store every prefix’s name, abbrev, and latex repr as an alias
PREFIX_ALIASES = {}

for abbrev, prefix in ALL_PREFIXES.items():
    # abbrev
    PREFIX_ALIASES[abbrev] = prefix
    # name
    prefix_name = str(prefix.name)
    PREFIX_ALIASES[prefix_name] = prefix
    # latex
    prefix_latex = latex(prefix)
    if '\\text' not in prefix_latex:
        PREFIX_ALIASES[prefix_latex] = prefix

# add additional custom prefix alias
PREFIX_ALIASES['u'] = micro

# define which constants are allowed
ALLOWED_CONSTANTS = [
    speed_of_light,
    atomic_mass_constant,
    electronvolt
]

# define additional aliases for pre-defined units
CUSTOM_UNIT_ALIASES = {
    degree: [r'\degree'],
    percent: [r'\%'],
    ampere: ['amp', 'amps', 'Amp', 'Amps'],
    second: ['sec', 'secs'],
    minute: ['min', 'mins'],
    hour: ['hr', 'hrs'],
    year: ['yr', 'yrs'],
    pound: ['lb', 'lbs'],
    inch: ['in'],
    bar: ['b']
}

# TODO: fix centiliter etc. not marked as prefixed


def get_base_unit(unit):
    unit_name = str(unit.name)
    if unit.is_prefixed:
        base_unit_name = None
        for _, prefix in PREFIXES.items():
            prefix_name = str(prefix.name)
            if unit_name.startswith(prefix_name):
                base_unit_name = unit_name[len(prefix_name):]
        if base_unit_name is not None and base_unit_name in dir(units):
            return getattr(units, base_unit_name)
    return None


def get_unit_aliases(unit, attribute_name=None):
    unit_aliases = []

    # abbrev
    unit_abbrev = str(unit.abbrev)
    unit_aliases.append(unit_abbrev)

    # name
    unit_name = str(unit.name)
    unit_aliases.append(unit_name)

    if unit_name == 'common_year':
        print()

    # allow capitalized name, e.g. "Gram", "Milligram"
    # except when containing underscores, e.g. "atomic_mass_constant"
    if '_' not in unit_name:
        unit_aliases.append(unit_name.capitalize())

    # if provided, allow attribute name, and capitalized attribute name (if not prefixed)
    if attribute_name is not None and attribute_name != unit_name and attribute_name != unit_abbrev:
        unit_aliases.append(attribute_name)
        if not unit.is_prefixed and '_' not in attribute_name:
            unit_aliases.append(attribute_name.capitalize())

    # if the unit is prefixed, check if the base unit is pluralized
    # if so, then add the pluralized name and pluralized capital name of the prefixed unit
    if unit.is_prefixed:
        base_unit = get_base_unit(unit)
        base_unit_name = str(base_unit.name) if base_unit is not None else None
        if base_unit is not None and f'{base_unit_name}s' in dir(units):
            unit_aliases.append(f'{unit_name}s')
            unit_aliases.append(f'{unit_name.capitalize()}s')

    # allow "u" as an additional "micro" prefix
    if unit.is_prefixed and unit_abbrev.startswith('mu'):
        unit_aliases.append('u' + unit_abbrev[2:])

    # latex
    unit_latex = latex(unit)
    if '\\text' not in unit_latex:
        unit_aliases.append(unit_latex)

    # add custom unit aliases, if defined
    if u in CUSTOM_UNIT_ALIASES:
        unit_aliases.extend(CUSTOM_UNIT_ALIASES[u])

    return unit_aliases


# construct a dict of every allowed string alias of each unit
UNIT_ALIASES = {}

# store every defined unit attribute’s aliases
# store every unit’s name, capitalized name, abbrev, and latex repr as an alias
# e.g. for `g = gram = grams = Quantity("gram", abbrev="g")`
# adds records for "g", "gram", "grams", "Gram", "Grams"
for attr in dir(units):
    u = getattr(units, attr)
    if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in ALLOWED_CONSTANTS):
        for alias in get_unit_aliases(u, attr):
            UNIT_ALIASES[alias] = u

# `all_units` contains every MKS/MKSA/SI unit and each possible prefixed variation
# store every unit’s name, capitalized name, abbrev, and latex repr as an alias
for u in all_units:
    if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in ALLOWED_CONSTANTS):
        for alias in get_unit_aliases(u):
            UNIT_ALIASES[alias] = u

# store every additional unit’s attribute name mappings
# e.g. for `lbf = pound_force = Quantity('pound_force', abbrev='lbf')`
# creates records for "lbf", "pound_force"
for attr in dir(additional_units):
    u = getattr(additional_units, attr)
    if isinstance(u, Quantity):
        UNIT_ALIASES[attr] = u

        unit_latex = latex(u)
        if '\\text' not in unit_latex:
            UNIT_ALIASES[unit_latex] = u

# ALIASES_BY_UNIT = {}
# for alias, unit in UNIT_ALIASES.items():
#     base_unit = get_base_unit(unit)
#     unit_name = str(unit.name) if base_unit is None else str(base_unit.name)
#     aliases = ALIASES_BY_UNIT.get(unit_name, [])
#     aliases.append(alias)
#     ALIASES_BY_UNIT[unit_name] = aliases

# print(ALIASES_BY_UNIT)

# output = list(UNIT_ALIASES)
# print(output)
# print(len(output))
