from sympy import Rational, pi
import sympy.physics.units.definitions.unit_definitions as sympy_units
import sympy.physics.units.prefixes as sympy_prefixes
import sympy.physics.units.definitions.dimension_definitions as sympy_dimensions
from sympy.physics.units.quantities import Quantity, PhysicalConstant
from sympy.physics.units.systems.si import SI
from latex2sympy.units.prefixes import create_prefixed_unit

# the default liter unit does not correctly define "L" as its abbrev
liter = Quantity('liter', abbrev='L')
# scale factor not set in sympy
SI.set_quantity_dimension(liter, sympy_dimensions.volume)
SI.set_quantity_scale_factor(liter, 1000 * sympy_units.centimeter**3)

# define additional units, scale factors taken from LON-CAPA / CAPA / Wikipedia
# https://loncapa04.purdue.edu/adm/help/Physical_Units.hlp

lbf = pound_force = Quantity('pound_force', abbrev='lbf')
pound_force.set_global_relative_scale_factor(Rational('4.44822'), sympy_units.newton)

slug = slugs = Quantity('slug')
slug.set_global_relative_scale_factor(Rational('14.59390'), sympy_units.kilogram)

cal = calories = calorie = Quantity('calorie', abbrev='cal')
calorie.set_global_relative_scale_factor(Rational('4.1868'), sympy_units.joule)

# TODO: other SI prefixes for calorie?
kcal = create_prefixed_unit(cal, sympy_prefixes.kilo)

btu = btus = Quantity('Btu', abbrev='btu')
btu.set_global_relative_scale_factor(Rational('1.05506E3'), sympy_units.joule)

degC = celsius = degreesCelsius = degreeCelsius = Quantity('degreeCelsius', abbrev='degC', latex_repr=r'\degree C')

degF = fahrenheit = degreesFahrenheit = degreeFahrenheit = Quantity('degreeFahrenheit', abbrev='degF', latex_repr=r'\degree F')

dB = decibels = decibel = Quantity('decibel', abbrev='dB')

mph = MPH = miles_per_hour = Quantity('miles_per_hour', abbrev='mph')
SI.set_quantity_dimension(mph, sympy_dimensions.velocity)
SI.set_quantity_scale_factor(mph, sympy_units.mile / sympy_units.hour)

kn = kt = knots = knot = Quantity('knot', abbrev='kn')
SI.set_quantity_dimension(knot, sympy_dimensions.velocity)
SI.set_quantity_scale_factor(knot, sympy_units.nautical_mile / sympy_units.hour)

cfm = CFM = cubic_feet_per_minute = Quantity('cubic_feet_per_minute', abbrev='cfm')
SI.set_quantity_dimension(cfm, sympy_dimensions.volume / sympy_dimensions.time)
SI.set_quantity_scale_factor(cfm, sympy_units.foot**3 / sympy_units.minute)

cfs = CFS = cubic_feet_per_second = Quantity('cubic_feet_per_second', abbrev='cfs')
cfs.set_global_relative_scale_factor(60, cfm)

rood = roods = Quantity('rood')
SI.set_quantity_dimension(rood, sympy_dimensions.area)
SI.set_quantity_scale_factor(rood, 1210 * sympy_units.yard**2)

acre = acres = Quantity('acre')
SI.set_quantity_dimension(acre, sympy_dimensions.area)
SI.set_quantity_scale_factor(acre, 4840 * sympy_units.yard**2)

# sievert is similar to gray, but they are not equatable
sieverts = sievert = Quantity('sievert', abbrev='Sv')
SI.set_quantity_dimension(sievert, sympy_dimensions.energy / sympy_dimensions.mass)
SI.set_quantity_scale_factor(sievert, sympy_units.meter**2 / sympy_units.second**2)

oz = ounces = ounce = Quantity('ounce', abbrev='oz')
ounce.set_global_relative_scale_factor(Rational(1, 16), sympy_units.pound)

# TODO: lumen, can't get scale factor to work
# SI.set_quantity_scale_factor(sympy_units.steradian, sympy_units.meter**2 / sympy_units.meter**2)

# lm = lumen = Quantity('lumen', abbrev='lm')
# SI.set_quantity_dimension(lumen, sympy_dimensions.luminous_intensity)
# SI.set_quantity_scale_factor(lumen, sympy_units.steradian * sympy_units.candela)

# SI.set_quantity_dimension(sympy_units.lux, sympy_dimensions.luminous_intensity / sympy_dimensions.length**2)
# SI.set_quantity_scale_factor(sympy_units.lux, lumen / sympy_units.meter**2)

pc = parsecs = parsec = Quantity('parsec', abbrev='pc')
parsec.set_global_relative_scale_factor(648000 / pi, sympy_units.astronomical_unit)

cc = ccs = cubic_centimeter = Quantity('cubic_centimeter', abbrev='cc')
SI.set_quantity_dimension(cc, sympy_dimensions.volume)
SI.set_quantity_scale_factor(cc, sympy_units.cm**3)

M = molar = Quantity('molar', abbrev='M')
SI.set_quantity_dimension(molar, sympy_dimensions.amount_of_substance / sympy_dimensions.volume)
SI.set_quantity_scale_factor(molar, sympy_units.mole / liter)
