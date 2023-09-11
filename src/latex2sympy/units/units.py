from sympy import latex, Mul, srepr
import sympy.physics.units.definitions.dimension_definitions as sympy_dimensions
import sympy.physics.units.definitions.unit_definitions as sympy_units
from sympy.physics.units.quantities import Quantity, PhysicalConstant
from sympy.physics.units.systems.mks import all_units as mks_units
from sympy.physics.units.systems.mksa import all_units as mksa_units
from sympy.physics.units.systems.si import all_units as si_units
from sympy.physics.units.systems.si import SI
from latex2sympy.units.prefixes import PREFIXES, BIN_PREFIXES, ALL_PREFIXES, prefix_unit
import latex2sympy.units.additional_units as additional_units

# define which PhysicalConstants are allowed
allowed_constants = [
    sympy_units.speed_of_light,
    sympy_units.atomic_mass_constant,
    sympy_units.electronvolt,
    sympy_units.elementary_charge
]

# define additional aliases for sympy units
custom_unit_aliases = {
    sympy_units.degree: [r'\degree'],
    sympy_units.percent: [r'\%'],
    sympy_units.ampere: ['amp', 'amps', 'Amp', 'Amps'],
    sympy_units.second: ['sec', 'secs', 'Sec', 'Secs'],
    sympy_units.minute: ['min', 'mins', 'Min', 'Mins'],
    sympy_units.hour: ['hr', 'hrs', 'Hr', 'Hrs'],
    sympy_units.year: ['yr', 'yrs', 'Yr', 'Yrs'],
    sympy_units.pound: ['lb', 'lbs'],
    sympy_units.inch: ['in'],
    sympy_units.microgram: ['mcg'],
    sympy_units.dyne: ['dyn'],
    sympy_units.amu: ['u']
}

# define fixed sympy units/additional prefixed units

# the default liter unit does not correctly define "L" as its abbrev
liter = additional_units.liter
liter_prefixed_units = prefix_unit(liter, PREFIXES)

# add additional prefixed units
eV_prefixed_units = prefix_unit(sympy_units.eV, PREFIXES)
Ci_prefixed_units = prefix_unit(sympy_units.Ci, PREFIXES)
bar_prefixed_units = prefix_unit(sympy_units.bar, PREFIXES)
byte_prefixed_units = prefix_unit(sympy_units.byte, BIN_PREFIXES)
bit_prefixed_units = prefix_unit(sympy_units.bit, BIN_PREFIXES)
M_prefixed_units = prefix_unit(additional_units.molar, PREFIXES)

additional_sympy_prefixed_units = [
    *liter_prefixed_units,
    *eV_prefixed_units,
    *Ci_prefixed_units,
    *bar_prefixed_units,
    *byte_prefixed_units,
    *bit_prefixed_units,
    *M_prefixed_units
]

# units that will replace the original sympy versions
fixed_sympy_units = {}
fixed_sympy_units[str(liter.name)] = liter
for u in [*liter_prefixed_units, *byte_prefixed_units]:
    fixed_sympy_units[str(u.name)] = u

# add missing sympy dimensions
SI.set_quantity_dimension(sympy_units.hectare, sympy_dimensions.area)
SI.set_quantity_scale_factor(sympy_units.hectare, 10000 * sympy_units.meter**2)

# sympy unit aliases we don't want to use
aliases_to_exclude = [
    'l',
    'cl',
    'dl',
    'ml',
    'v',
    'pa',
    'wb'
]

# sympy unit aliases that should have a pluralized form added
aliases_to_pluralize = [
    'becquerel',
    'katal',
    'gray',
    'curie',
    'rutherford',
    'permille',
    'tonne',
    'dioptre',
    'diopter',
    'dalton',
    'torr',
    'statampere',
    'statcoulomb',
    'statvolt',
    'franklin',
    'hectare',
    'maxwell'
]

# sympy unit aliases that should not have a capitalized form added
aliases_to_not_capitalize = [
    'au',
    'h',
    'amu',
    'amus',
    'nmi',
    'mmu',
    'mmus',
    'mi',
    'mmHg',
    'psi',
    'kt',
    'ccs'
]


def capitalize_first_letter(name):
    return name[0].upper() + name[1:]


def get_base_unit(unit, dir_module):
    unit_name = str(unit.name)
    if unit.is_prefixed:
        base_unit_name = None
        for _, prefix in ALL_PREFIXES.items():
            prefix_name = str(prefix.name)
            if unit_name.startswith(prefix_name):
                base_unit_name = unit_name[len(prefix_name):]
        if base_unit_name is not None and base_unit_name in dir(dir_module):
            return getattr(dir_module, base_unit_name)
    return None


def get_aliases_for_unit(unit, dir_module, attr_name=None):
    unit_aliases = []

    # abbrev
    unit_abbrev = str(unit.abbrev)
    if '_' not in unit_abbrev:
        unit_aliases.append(unit_abbrev)

    # name
    unit_name = str(unit.name)
    if '_' not in unit_name:
        unit_aliases.append(unit_name)
        # plural name
        if unit_name in aliases_to_pluralize:
            unit_aliases.append(f'{unit_name}s')
        # capitalized name
        if unit_name not in aliases_to_not_capitalize:
            unit_name_capitalized = capitalize_first_letter(unit_name)
            unit_aliases.append(unit_name_capitalized)
            # plural capitalized name
            if unit_name in aliases_to_pluralize:
                unit_aliases.append(f'{unit_name_capitalized}s')

    # attr name
    # except when containing underscores, e.g. "metric_ton"
    if attr_name is not None and '_' not in attr_name and \
            attr_name != unit_name and attr_name != unit_abbrev:
        unit_aliases.append(attr_name)
        # plural attr name
        if attr_name in aliases_to_pluralize:
            unit_aliases.append(f'{attr_name}s')
        # capitalized attr name, when not prefixed, and not excluded
        if not unit.is_prefixed and attr_name not in aliases_to_not_capitalize:
            attr_capitalized = capitalize_first_letter(attr_name)
            unit_aliases.append(attr_capitalized)
            # plural capitalized attr name
            if attr_name in aliases_to_pluralize:
                unit_aliases.append(f'{attr_capitalized}s')

    # if the unit is prefixed, check if the base unit is pluralized in the given `dir_module`
    # if so, then add the pluralized name and pluralized capital name of the prefixed unit
    if unit.is_prefixed:
        base_unit = get_base_unit(unit, dir_module)
        base_unit_name = str(base_unit.name) if base_unit is not None else None
        if base_unit is not None and (f'{base_unit_name}s' in dir(dir_module) or base_unit_name in aliases_to_pluralize):
            unit_aliases.append(f'{unit_name}s')
            unit_aliases.append(f'{capitalize_first_letter(unit_name)}s')

    # add "u" as an additional "micro" prefix
    if unit.is_prefixed and unit_abbrev.startswith('mu'):
        unit_aliases.append('u' + unit_abbrev[2:])

    # latex
    # except when value contains "\text{}" or "\r{}" or "\circ"
    unit_latex = latex(unit)
    if '\\text{' not in unit_latex and '\\r{' not in unit_latex and '\\circ' not in unit_latex:
        unit_aliases.append(unit_latex)

    # custom unit aliases, if defined
    if u in custom_unit_aliases:
        unit_aliases.extend(custom_unit_aliases[u])

    return unit_aliases


# -------------------------------------------------------------------------------------------------

# construct a dict of every allowed string alias of each unit
UNIT_ALIASES = {}

# add aliases for defined attributes
for attr in dir(sympy_units):
    u = getattr(sympy_units, attr)
    if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in allowed_constants) and attr not in aliases_to_exclude:
        # override sympy units that have been fixed
        if str(u.name) in fixed_sympy_units:
            u = fixed_sympy_units[str(u.name)]
        for alias in get_aliases_for_unit(u, sympy_units, attr):
            if alias in UNIT_ALIASES and str(u.name) != str(UNIT_ALIASES[alias].name):  # pragma: no cover
                raise Exception(f'attr: alias "{alias}" conflicted between {str(u.name)} and {str(UNIT_ALIASES[alias].name)}')
            UNIT_ALIASES[alias] = u

# `all_si_units` contains every MKS/MKSA/SI unit and each possible prefixed variation
all_si_units = set([*mks_units, *mksa_units, *si_units, *additional_sympy_prefixed_units])
# add aliases for all prefixed units
for u in all_si_units:
    if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in allowed_constants):
        for alias in get_aliases_for_unit(u, sympy_units):
            if alias in UNIT_ALIASES and str(u.name) != str(UNIT_ALIASES[alias].name):  # pragma: no cover
                raise Exception(f'unit: alias "{alias}" conflicted between {str(u.name)} and {str(UNIT_ALIASES[alias].name)}')
            UNIT_ALIASES[alias] = u

# add aliases for additional units
for attr in dir(additional_units):
    u = getattr(additional_units, attr)
    if isinstance(u, Quantity):
        for alias in get_aliases_for_unit(u, additional_units, attr):
            if alias in UNIT_ALIASES and str(u.name) != str(UNIT_ALIASES[alias].name):  # pragma: no cover
                raise Exception(f'additional unit: alias "{alias}" conflicted between {str(u.name)} and {str(UNIT_ALIASES[alias].name)}')
            UNIT_ALIASES[alias] = u

# -------------------------------------------------------------------------------------------------

# # test output
# ALIASES_BY_UNIT = {}
# for alias, unit in UNIT_ALIASES.items():
#     if isinstance(unit, Mul):
#         ALIASES_BY_UNIT[alias] = srepr(unit)
#         continue
#     base_sympy_unit = get_base_unit(unit, sympy_units)
#     base_unit = get_base_unit(unit, additional_units) if base_sympy_unit is None else base_sympy_unit
#     unit_name = str(unit.name) if base_unit is None else str(base_unit.name)
#     aliases = ALIASES_BY_UNIT.get(unit_name, [])
#     aliases.append(alias)
#     ALIASES_BY_UNIT[unit_name] = aliases
# print(ALIASES_BY_UNIT)

# output = list(UNIT_ALIASES)
# print(output)
# print(len(output))