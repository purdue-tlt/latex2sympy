import os.path
import pickle

from sympy import latex
import sympy.physics.units.definitions.unit_definitions as sympy_units
from sympy.physics.units.quantities import Quantity, PhysicalConstant
from sympy.physics.units.systems.mks import all_units as mks_units, units as mks_base_units
from sympy.physics.units.systems.mksa import all_units as mksa_units, units as mksa_base_units
from sympy.physics.units.systems.si import all_units as si_units, units as si_base_units
from latex2sympy.units.sie import all_units as sie_units
from latex2sympy.units.prefixes import NEW_SI_PREFIXES, SI_PREFIXES, INFORMATION_SI_PREFIXES, BIN_PREFIXES, ALL_PREFIXES, PREFIX_ALIASES, prefix_unit
import latex2sympy.units.unit_definitions as additional_units
import json

# -------------------------------------------------------------------------------------------------
# define fixed sympy units / additional prefixed units
# -------------------------------------------------------------------------------------------------

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
    sympy_units.amu: ['u'],
    sympy_units.mil: ['mrad'],
    sympy_units.meter: ['metre', 'metres', 'Metre', 'Metres']
}

# the default liter unit does not correctly define "L" as its abbrev
liter = additional_units.liter
liter_prefixed_units = prefix_unit(liter, SI_PREFIXES)
# add alternate spelling
custom_unit_aliases[liter] = ['litre', 'litres', 'Litre', 'Litres']

# the default gray unit does not correctly define "Gy" as its abbrev
gray = additional_units.gray
gray_prefixed_units = prefix_unit(gray, SI_PREFIXES)

# the default bit unit does not correctly define "bit" as its abbrev
bit = additional_units.bit
# define all binary and SI prefixes for bit
bit_prefixed_units = prefix_unit(bit, BIN_PREFIXES)
bit_si_prefixed_units = prefix_unit(bit, INFORMATION_SI_PREFIXES)
# also add "b" as an alternate abbrev for bit, and all its prefixed forms
custom_unit_aliases[bit] = ['b']
for bit_prefixed_unit in [*bit_prefixed_units, *bit_si_prefixed_units]:
    bit_prefixed_unit_abbrev = str(bit_prefixed_unit.abbrev)
    custom_unit_aliases[bit_prefixed_unit] = [
        bit_prefixed_unit_abbrev[:-2]
    ]

# the default byte unit does not correctly define "B" as its abbrev
byte = additional_units.byte
# define all binary and SI prefixes for byte
byte_prefixed_units = prefix_unit(byte, BIN_PREFIXES)
byte_si_prefixed_units = prefix_unit(byte, INFORMATION_SI_PREFIXES)

# define additional prefixed units
additional_sympy_prefixed_units = [
    *liter_prefixed_units,
    *gray_prefixed_units,
    *bit_prefixed_units,
    *bit_si_prefixed_units,
    *byte_prefixed_units,
    *byte_si_prefixed_units,
]

units_to_prefix = [
    sympy_units.eV,
    sympy_units.Ci,
    sympy_units.bar,
    additional_units.molar,
    additional_units.calorie,
    additional_units.sievert
]
for u in units_to_prefix:
    additional_sympy_prefixed_units.extend(prefix_unit(u, SI_PREFIXES))

# add new SI prefixed versions of all SI base units
base_units = [*mks_base_units, *mksa_base_units, *si_base_units]
for base_unit in base_units:
    additional_sympy_prefixed_units.extend(prefix_unit(base_unit, NEW_SI_PREFIXES))

# units that will replace the original sympy versions
fixed_sympy_units = {}
fixed_sympy_units[str(liter.name)] = liter
fixed_sympy_units[str(gray.name)] = gray
fixed_sympy_units[str(bit.name)] = bit
fixed_sympy_units[str(byte.name)] = byte
for u in [*liter_prefixed_units, *gray_prefixed_units, *bit_prefixed_units, *byte_prefixed_units]:
    fixed_sympy_units[str(u.name)] = u

# -------------------------------------------------------------------------------------------------

# define which PhysicalConstants are allowed
allowed_constants = [
    sympy_units.speed_of_light,
    sympy_units.atomic_mass_constant,
    sympy_units.electronvolt,
    sympy_units.elementary_charge
]

# define with sympy units should be excluded
units_to_exclude = [
    sympy_units.quart,
    # CGS derived units
    sympy_units.dyne,
    sympy_units.erg,
    # CGS units for electromagnetic quantities
    sympy_units.statampere,
    sympy_units.statcoulomb,
    sympy_units.statvolt,
    sympy_units.gauss,
    sympy_units.maxwell,
    sympy_units.debye,
    sympy_units.oersted
]

# sympy unit aliases we don't want to use
aliases_to_exclude = [
    'l',
    'cl',
    'dl',
    'ml',
    'v',
    'pa',
    'wb',
    'hz'
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
    'hectare'
]

# sympy unit aliases that should be capitalized
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
    'ccs',
    'rpms'
]

# -------------------------------------------------------------------------------------------------


def capitalize_first_letter(name):
    return name[0].upper() + name[1:]


def get_base_unit(unit, dir_module):
    unit_name = str(unit.name)
    if not unit.is_prefixed:  # pragma: no cover
        return None
    base_unit_name = None
    for _, prefix in ALL_PREFIXES.items():
        prefix_name = str(prefix.name)
        if unit_name.startswith(prefix_name):
            base_unit_name = unit_name[len(prefix_name):]
    if base_unit_name is not None and base_unit_name in dir(dir_module):
        return getattr(dir_module, base_unit_name)
    return None


def get_aliases_for_unit(unit, dir_module=None, attr_name=None):
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

    # check if the unit is prefixed
    # if the base unit is found and is pluralized, add the pluralized name and pluralized capital name of the prefixed unit
    if unit.is_prefixed:
        # if dir_module is not provided, attempt to find the base unit in either location
        if dir_module is None:
            additional_base_unit = get_base_unit(unit, additional_units)
            sympy_base_unit = get_base_unit(unit, sympy_units)
            base_unit = additional_base_unit if additional_base_unit is not None else sympy_base_unit
            dir_list = dir(additional_units if additional_base_unit is not None else sympy_units)
        else:
            base_unit = get_base_unit(unit, sympy_units)
            dir_list = dir(dir_module)
        base_unit_name = str(base_unit.name) if base_unit is not None else None
        if base_unit is not None and (f'{base_unit_name}s' in dir_list or base_unit_name in aliases_to_pluralize):
            unit_aliases.append(f'{unit_name}s')
            unit_aliases.append(f'{capitalize_first_letter(unit_name)}s')

        # add alternate spellings for "meter" and "liter" prefixed units
        if base_unit_name in ['meter', 'liter']:
            alt_base_unit_name = 'metre' if base_unit_name == 'meter' else 'litre'
            alt_unit_aliases = []
            for ua in unit_aliases:
                if base_unit_name in ua:
                    alt_unit_aliases.append(ua.replace(base_unit_name, alt_base_unit_name))
            unit_aliases.extend(alt_unit_aliases)

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
# -------------------------------------------------------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pickle_file_path = f'{ROOT_DIR}/unit_aliases.pkl'
pickle_file_exists = os.path.isfile(pickle_file_path)
if pickle_file_exists:
    pickle_file = open(pickle_file_path, 'rb')
    UNIT_ALIASES = pickle.load(pickle_file)
    pickle_file.close()
else:
    UNIT_ALIASES = {}

    # add aliases for defined attributes
    for attr in dir(sympy_units):
        u = getattr(sympy_units, attr)
        if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in allowed_constants) and attr not in aliases_to_exclude and u not in units_to_exclude:
            # override sympy units that have been fixed
            if str(u.name) in fixed_sympy_units:
                u = fixed_sympy_units[str(u.name)]
            for alias in get_aliases_for_unit(u, sympy_units, attr):
                if alias in UNIT_ALIASES and str(u.name) != str(UNIT_ALIASES[alias].name):  # pragma: no cover
                    raise Exception(f'attr: alias "{alias}" conflicted between {str(u.name)} and {str(UNIT_ALIASES[alias].name)}')
                UNIT_ALIASES[alias] = u

    # `all_si_units` contains every MKS/MKSA/SI unit and each possible prefixed variation
    all_si_units = set([
        *mks_units,
        *mksa_units,
        *si_units,
        *sie_units,
        *additional_sympy_prefixed_units,
    ])
    # add aliases for all prefixed units
    for u in all_si_units:
        if isinstance(u, Quantity) and (not isinstance(u, PhysicalConstant) or u in allowed_constants) and u not in units_to_exclude:
            # override sympy units that have been fixed
            if str(u.name) in fixed_sympy_units:
                u = fixed_sympy_units[str(u.name)]
            for alias in get_aliases_for_unit(u):
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
if not pickle_file_exists:
    pickle_file = open(pickle_file_path, 'wb')
    pickle.dump(UNIT_ALIASES, pickle_file)
    pickle_file.close()

# -------------------------------------------------------------------------------------------------
# test output
# -------------------------------------------------------------------------------------------------

# ALIASES_BY_UNIT = {}
# for alias, unit in UNIT_ALIASES.items():
#     base_sympy_unit = get_base_unit(unit, sympy_units)
#     base_unit = get_base_unit(unit, additional_units) if base_sympy_unit is None else base_sympy_unit
#     unit_name = str(unit.name) if base_unit is None else str(base_unit.name)

#     unit_obj = ALIASES_BY_UNIT.get(unit_name, {})
#     aliases = unit_obj.get('aliases', [])

#     if unit.is_prefixed and base_unit is not None:
#         prefixes = unit_obj.get('prefixes', {})

#         prefix_name = str(unit.name).replace(str(base_unit.name), '')
#         prefix = PREFIX_ALIASES[prefix_name]
#         prefix_index = [*ALL_PREFIXES.keys()].index(str(prefix.abbrev))
#         prefixes_key = f'{prefix_index}-{prefix_name}'
#         prefix_aliases = prefixes.get(prefixes_key, [])

#         prefix_aliases.append(alias)

#         prefixes[prefixes_key] = prefix_aliases
#         prefixes = dict(sorted(prefixes.items(), key=lambda kvp: int(kvp[0][:kvp[0].find('-')])))
#         unit_obj['prefixes'] = prefixes
#     else:
#         aliases.append(alias)

#     unit_obj['aliases'] = aliases
#     ALIASES_BY_UNIT[unit_name] = unit_obj

# with open('src/latex2sympy/units/unit_aliases.json', 'w', encoding='utf-8') as f:
#     json.dump(ALIASES_BY_UNIT, f, ensure_ascii=False, indent=4)

# print(ALIASES_BY_UNIT)
