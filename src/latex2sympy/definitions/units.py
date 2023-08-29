import sympy
import sympy.physics.units as sympy_physics_units
from sympy.physics.units.definitions.unit_definitions import curie, bar
from sympy.physics.units.prefixes import PREFIXES, BIN_PREFIXES
from sympy.physics.units.quantities import Quantity

# combine all known prefixes into a single list
UNIT_PREFIXES = [*PREFIXES.values(), *BIN_PREFIXES.values()]

ADDITIONAL_PREFIX_ALIASES = {
    PREFIXES['mu']: ['u']
}

# define additional units, scale factors taken from LON-CAPA / CAPA

lbf = pound_force = Quantity('pound_force', abbrev='lbf')
pound_force.set_global_relative_scale_factor(sympy.Rational('4.44822'), sympy_physics_units.N)

slug = slugs = Quantity('slug')
slug.set_global_relative_scale_factor(sympy.Rational('14.59390'), sympy_physics_units.kg)

cal = calorie = Quantity('calorie', abbrev='cal')
calorie.set_global_relative_scale_factor(sympy.Rational('4.1868'), sympy_physics_units.J)

btu = Btu = Quantity('Btu', abbrev='btu')
Btu.set_global_relative_scale_factor(sympy.Rational('1.05506E3'), sympy_physics_units.J)

# TODO how to set dimension and scale for multiple dimensions? need to extend SI UnitSystem?

degC = degreeC = degreeCelsius = Quantity('degreeCelsius', abbrev='degC', latex_repr=r'\degree C')

degF = degreeF = degreeFahrenheit = Quantity('degreeFahrenheit', abbrev='degF', latex_repr=r'\degree F')

molar = molar_concentration = Quantity('molar_concentration', abbrev='molar')

ADDITIONAL_UNITS = [
    curie,
    pound_force,
    slug,
    calorie,
    Btu,
    degC,
    degF,
    molar
]

ALLOWED_CONSTANTS = [
    sympy_physics_units.c,
    sympy_physics_units.amu,
    sympy_physics_units.eV
]

_ADDITIONAL_UNIT_ALIASES = {
    sympy_physics_units.second: ['sec', 'secs'],
    sympy_physics_units.minute: ['min', 'mins'],
    sympy_physics_units.hour: ['hr', 'hrs'],
    sympy_physics_units.year: ['yr', 'yrs'],
    sympy_physics_units.pound: ['lb', 'lbs'],
    sympy_physics_units.inch: ['in'],
    sympy_physics_units.bar: ['b'],
    slug: ['slugs'],
    degreeCelsius: ['degC', 'degreeC'],
    degreeFahrenheit: ['degF', 'degreeF']
}

ADDITIONAL_UNIT_ALIASES = {}
for unit, value in _ADDITIONAL_UNIT_ALIASES.items():
    for alias in value:
        ADDITIONAL_UNIT_ALIASES[alias] = unit
