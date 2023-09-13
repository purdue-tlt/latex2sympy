from sympy import Rational, pi
import sympy.physics.units.definitions.unit_definitions as sympy_units
import sympy.physics.units.definitions.dimension_definitions as sympy_dimensions
from sympy.physics.units.quantities import Quantity

# redefine liter to add "L" as its abbrev, to work with prefixes
liter = Quantity('liter', abbrev='L')

# redefine bit to define "bit" as its abbrev, to work with prefixes
bit = Quantity('bit', abbrev='bit')
bit.set_global_dimension(sympy_dimensions.information)

# redefine byte to define "B" as its abbrev, to work with prefixes
byte = Quantity('byte', abbrev='B')
byte.set_global_relative_scale_factor(8, bit)

# define additional units, scale factors taken from LON-CAPA / CAPA / Wikipedia
# https://loncapa04.purdue.edu/adm/help/Physical_Units.hlp

lbf = pound_force = Quantity('pound_force', abbrev='lbf')
pound_force.set_global_relative_scale_factor(Rational('4.44822'), sympy_units.newton)

slug = slugs = Quantity('slug')
slug.set_global_relative_scale_factor(Rational('14.59390'), sympy_units.kilogram)

cal = calories = calorie = Quantity('calorie', abbrev='cal')
calorie.set_global_relative_scale_factor(Rational('4.1868'), sympy_units.joule)

btu = btus = Quantity('Btu', abbrev='btu')
btu.set_global_relative_scale_factor(Rational('1.05506E3'), sympy_units.joule)

degC = celsius = degreesCelsius = degreeCelsius = Quantity('degreeCelsius', abbrev='degC', latex_repr=r'\degree C')

degF = fahrenheit = degreesFahrenheit = degreeFahrenheit = Quantity('degreeFahrenheit', abbrev='degF', latex_repr=r'\degree F')

dB = decibels = decibel = Quantity('decibel', abbrev='dB')

mph = MPH = miles_per_hour = Quantity('miles_per_hour', abbrev='mph')

kn = kt = knots = knot = Quantity('knot', abbrev='kn')

cfm = CFM = cubic_feet_per_minute = Quantity('cubic_feet_per_minute', abbrev='cfm')

cfs = CFS = cubic_feet_per_second = Quantity('cubic_feet_per_second', abbrev='cfs')
cfs.set_global_relative_scale_factor(60, cfm)

rood = roods = Quantity('rood')

acre = acres = Quantity('acre')

sieverts = sievert = Quantity('sievert', abbrev='Sv')

pc = parsecs = parsec = Quantity('parsec', abbrev='pc')
parsec.set_global_relative_scale_factor(648000 / pi, sympy_units.astronomical_unit)

cc = ccs = cubic_centimeter = Quantity('cubic_centimeter', abbrev='cc')

M = molar = Quantity('molar', abbrev='M')

rpm = rpms = rotations_per_minute = Quantity('rotations_per_minute', abbrev='rpm')

lm = lumens = lumen = Quantity('lumen', abbrev='lm')
