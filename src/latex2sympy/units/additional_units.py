from sympy import Rational
from sympy.physics.units.definitions.unit_definitions import kilogram, joule, newton
from sympy.physics.units.quantities import Quantity

# define additional units, scale factors taken from LON-CAPA / CAPA
# https://loncapa04.purdue.edu/adm/help/Physical_Units.hlp

lbf = pound_force = Quantity('pound_force', abbrev='lbf')
pound_force.set_global_relative_scale_factor(Rational('4.44822'), newton)

slug = slugs = Quantity('slug')
slug.set_global_relative_scale_factor(Rational('14.59390'), kilogram)

cal = calories = calorie = Quantity('calorie', abbrev='cal')
calorie.set_global_relative_scale_factor(Rational('4.1868'), joule)

btu = Btu = Quantity('Btu', abbrev='btu')
Btu.set_global_relative_scale_factor(Rational('1.05506E3'), joule)

# TODO how to set dimension and scale for multiple dimensions? need to extend UnitSystem?

degC = degreeCelsius = Quantity('degreeCelsius', abbrev='degC', latex_repr=r'\degree C')

degF = degreeFahrenheit = Quantity('degreeFahrenheit', abbrev='degF', latex_repr=r'\degree F')

dB = decibels = decibel = Quantity('decibel', abbrev='dB')
