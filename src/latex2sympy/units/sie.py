"""
SI Extended unit system.
Based on SI.
Added lumen, steradian and dimensions.

"""

from sympy import Rational
from sympy.physics.units import Dimension
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems.si import SI, dimsys_SI
from sympy.physics.units.definitions.dimension_definitions import (
    mass, length, time, velocity, energy, area, volume, frequency, amount_of_substance
)
from sympy.physics.units.definitions.unit_definitions import (
    meter, cm, foot, mile, nautical_mile,
    yard, hectare,
    steradian, candela, lux,
    second, minute, hour,
    mole,
    hertz
)
from latex2sympy.units.additional_units import (
    liter, lumen, mph, knot, cfm, rood, acre, sievert, cc, molar, rpm
)
from latex2sympy.units.prefixes import SI_PREFIXES, prefix_unit, create_prefixed_unit

# define new dimensions
solid_angle = Dimension("solid_angle")
luminous_flux = Dimension("luminous_flux")

units = [lumen]

all_units: list[Quantity] = []
for u in units:
    all_units.extend(prefix_unit(u, SI_PREFIXES))

all_units.extend([
    create_prefixed_unit(steradian, SI_PREFIXES['m']),
    create_prefixed_unit(steradian, SI_PREFIXES['mu'])
])
all_units.extend(units)
all_units.extend([steradian, lumen])


dimsys_SIE = dimsys_SI.extend(
    [
        solid_angle
    ],
    new_derived_dims=[
        luminous_flux
    ],
    new_dim_deps={
        'luminous_flux': {'luminous_intensity': 1, 'solid_angle': 1}
    })

SIE = SI.extend(base=(steradian,), units=all_units, name='SIE', dimension_system=dimsys_SIE, derived_units={
    luminous_flux: lumen
})

# steradian
SIE.set_quantity_dimension(steradian, solid_angle)

# lumen
SIE.set_quantity_dimension(lumen, luminous_flux)
SIE.set_quantity_scale_factor(lumen, steradian * candela)

# redefine lux from the original in SI
SIE.set_quantity_dimension(lux, luminous_flux / length**2)
SIE.set_quantity_scale_factor(lux, lumen / meter**2)

# liter scale factor not set in sympy
SIE.set_quantity_dimension(liter, volume)
SIE.set_quantity_scale_factor(liter, 1000 * cm**3)

# add hectare scale factor and dimension
SIE.set_quantity_dimension(hectare, area)
SIE.set_quantity_scale_factor(hectare, 10000 * meter**2)

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
SIE.set_quantity_dimension(sievert, energy / mass)
SIE.set_quantity_scale_factor(sievert, meter**2 / second**2)

# cc
SIE.set_quantity_dimension(cc, volume)
SIE.set_quantity_scale_factor(cc, cm**3)

# molar
SIE.set_quantity_dimension(molar, amount_of_substance / volume)
SIE.set_quantity_scale_factor(molar, mole / liter)

# rpm
# allow rpm conversion to Hz for frequency
SIE.set_quantity_dimension(rpm, frequency)
SIE.set_quantity_scale_factor(rpm, Rational(1, 60) * hertz)

# TODO: conversion to rad/s for angular velocity doesn't work
# SI.set_quantity_scale_factor(rpm, Rational(1, 30) * pi * rad / second)
# SI.set_quantity_scale_factor(hertz, 2 * pi * rad / second)
