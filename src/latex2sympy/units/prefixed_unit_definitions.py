from sympy.physics.units.systems.mks import units as mks_base_units
from sympy.physics.units.systems.mksa import units as mksa_base_units
from sympy.physics.units.systems.si import units as si_base_units
from latex2sympy.units.prefixes import NEW_SI_PREFIXES, SI_PREFIXES, INFORMATION_SI_PREFIXES, BIN_PREFIXES, prefix_unit, create_prefixed_unit
from sympy.physics.units.definitions.unit_definitions import (
    steradian, eV, Ci, bar
)
from latex2sympy.units.unit_definitions import (
    lumen, liter, gray, bit, byte, molar, calorie, sievert
)

# explicitly create these prefixed units for use in UNIT_ALIASES
liter_prefixed_units = prefix_unit(liter, SI_PREFIXES)
gray_prefixed_units = prefix_unit(gray, SI_PREFIXES)
# create all binary and SI prefixes for bit
bit_prefixed_units = prefix_unit(bit, BIN_PREFIXES)
bit_si_prefixed_units = prefix_unit(bit, INFORMATION_SI_PREFIXES)
# create all binary and SI prefixes for byte
byte_prefixed_units = prefix_unit(byte, BIN_PREFIXES)
byte_si_prefixed_units = prefix_unit(byte, INFORMATION_SI_PREFIXES)

# only create milli and micro prefixed steradians
steradian_prefixed_units = [
    create_prefixed_unit(steradian, SI_PREFIXES['m']),
    create_prefixed_unit(steradian, SI_PREFIXES['mu'])
]

# define additional prefixed units
additional_prefixed_units = [
    *liter_prefixed_units,
    *gray_prefixed_units,
    *bit_prefixed_units,
    *bit_si_prefixed_units,
    *byte_prefixed_units,
    *byte_si_prefixed_units,
    *steradian_prefixed_units
]

# create all SI prefixed versions of these units
units_to_prefix = [
    lumen,
    eV,
    Ci,
    bar,
    molar,
    calorie,
    sievert
]
for u in units_to_prefix:
    additional_prefixed_units.extend(prefix_unit(u, SI_PREFIXES))

# create new SI prefixed versions of all SI base units
base_units = [*mks_base_units, *mksa_base_units, *si_base_units]
for base_unit in base_units:
    additional_prefixed_units.extend(prefix_unit(base_unit, NEW_SI_PREFIXES))
