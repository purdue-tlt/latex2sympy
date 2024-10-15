"""
SI Extended unit system.
Based on SI.
Added solid_angle and luminous_flux dimensions, plus other additional quantities.

"""

from sympy import Rational
from sympy.physics.units.definitions.dimension_definitions import (
    amount_of_substance,
    area,
    energy,
    length,
    mass,
    time,
    velocity,
    volume,
)
from sympy.physics.units.definitions.unit_definitions import (
    angular_mil,
    candela,
    cm,
    foot,
    hour,
    lux,
    meter,
    mile,
    minute,
    mole,
    nautical_mile,
    rad,
    second,
    steradian,
    yard,
)
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems.si import dimsys_SI, SI

from latex2sympy.units.dimensions import luminous_flux, solid_angle
from latex2sympy.units.prefixed_unit_definitions import additional_prefixed_units
from latex2sympy.units.unit_definitions import (
    acre,
    bit,
    btu,
    byte,
    calorie,
    cc,
    cfm,
    cfs,
    dB,
    degC,
    degF,
    gray,
    knot,
    lbf,
    liter,
    lumen,
    molar,
    mph,
    pc,
    rood,
    rpm,
    sievert,
    slug,
)

# define units to include in SIE that are not in SI, or are new versions
all_units: list[Quantity] = [
    steradian,
    lumen,
    liter,
    gray,
    bit,
    byte,
    lbf,
    slug,
    calorie,
    btu,
    degC,
    degF,
    dB,
    mph,
    knot,
    cfm,
    cfs,
    rood,
    acre,
    sievert,
    pc,
    cc,
    molar,
    rpm,
]
all_units.extend(additional_prefixed_units)

dimsys_SIE = dimsys_SI.extend(
    [solid_angle],
    new_derived_dims=[luminous_flux],
    new_dim_deps={'luminous_flux': {'luminous_intensity': 1, 'solid_angle': 1}},
)

SIE = SI.extend(
    base=(steradian,), units=all_units, name='SIE', dimension_system=dimsys_SIE, derived_units={luminous_flux: lumen}
)

# steradian
SIE.set_quantity_dimension(steradian, solid_angle)

# lumen
SIE.set_quantity_dimension(lumen, luminous_flux)
SIE.set_quantity_scale_factor(lumen, steradian * candela)

# redefine lux to use lumen
SIE.set_quantity_dimension(lux, luminous_flux / length**2)
SIE.set_quantity_scale_factor(lux, lumen / meter**2)

# define new fixed version of liter
SIE.set_quantity_dimension(liter, volume)
SIE.set_quantity_scale_factor(liter, 1000 * cm**3)

# define new fixed version of gray
SIE.set_quantity_dimension(gray, energy / mass)
SIE.set_quantity_scale_factor(gray, meter**2 / second**2)

# define angular_mil/mil/mrad to rad conversion
angular_mil.set_global_relative_scale_factor(Rational(1, 1000), rad)

# mph
SIE.set_quantity_dimension(mph, velocity)
SIE.set_quantity_scale_factor(mph, mile / hour)

# knot
SIE.set_quantity_dimension(knot, velocity)
SIE.set_quantity_scale_factor(knot, nautical_mile / hour)

# cfm
SIE.set_quantity_dimension(cfm, volume / time)
SIE.set_quantity_scale_factor(cfm, foot**3 / minute)

# rood
SIE.set_quantity_dimension(rood, area)
SIE.set_quantity_scale_factor(rood, 1210 * yard**2)

# acre
SIE.set_quantity_dimension(acre, area)
SIE.set_quantity_scale_factor(acre, 4840 * yard**2)

# sievert
# sievert is similar to gray, but they are not equatable (see convert_to in units/utils)
SIE.set_quantity_dimension(sievert, energy / mass)
SIE.set_quantity_scale_factor(sievert, meter**2 / second**2)

# cc
SIE.set_quantity_dimension(cc, volume)
SIE.set_quantity_scale_factor(cc, cm**3)

# molar
SIE.set_quantity_dimension(molar, amount_of_substance / volume)
SIE.set_quantity_scale_factor(molar, mole / liter)
