import pytest
from sympy import Symbol
from sympy.physics.units import Quantity
from sympy.physics.units.prefixes import PREFIXES, BIN_PREFIXES
from sympy.physics.units.definitions.unit_definitions import (
    # MKS - "meter, kilogram, second"
    meter, gram, kilogram, second, joule, newton, watt, pascal, hertz, speed_of_light,
    # MKSA - based on MKS, "meter, kilogram, second, ampere"
    ampere, volt, ohm, siemens, farad, henry, coulomb, tesla, weber,
    # SI - based on MKSA, added kelvin, candela and mole
    mole, kelvin, lux,
    candela, becquerel,
    gray, katal,
    # Derived
    kilometer, centimeter, millimeter, nanometer,
    milligram, microgram,
    millisecond, microsecond,
    liter, milliliter,
    # Other
    percent,
    degree,
    rad,
    minute, hour, day, year,
    foot, inch, mile, pound,
    curie, gauss,
    atomic_mass_constant,
    atmosphere,
    electronvolt,
    bar, psi, bit
)
from latex2sympy.latex2sympy import process_sympy
from latex2sympy.units.additional_units import cal, kcal, lbf, slug, degC, degF, dB, btu
from latex2sympy.units import create_prefixed_unit, UNIT_ALIASES
from .context import _Mul, _Pow, assert_equal, is_or_contains_instance

# create local vars for prefixed units for convenience
millivolt = UNIT_ALIASES['millivolt']
microohm = UNIT_ALIASES['microohm']

unit_examples = [
    # units by abbrev
    ('m', meter),
    ('g', gram),
    ('s', second),
    ('J', joule),
    ('N', newton),
    ('W', watt),
    ('Pa', pascal),
    ('Hz', hertz),
    ('A', ampere),
    ('V', volt),
    ('\\Omega', ohm),
    ('S', siemens),
    ('F', farad),
    ('H', henry),
    ('C', coulomb),
    ('T', tesla),
    ('Wb', weber),
    ('mol', mole),
    ('cd', candela),
    ('K', kelvin),
    ('Bq', becquerel),
    ('lx', lux),
    ('Gy', gray),
    ('kat', katal),
    ('bar', bar),
    ('deg', degree),
    ('atm', atmosphere),
    ('ft', foot),
    ('L', liter),

    # units by names
    ('gram', gram),
    ('grams', gram),
    ('Gram', gram),
    ('Grams', gram),

    # assorted unit names (from suffixes)
    ('days', day),
    ('Degrees', degree),
    ('Farads', farad),
    ('hours', hour),
    ('moles', mole),
    ('ohms', ohm),
    ('percent', percent),
    ('pounds', pound),
    ('psi', psi),
    ('Seconds', second),
    ('Watts', watt),
    ('years', year),

    # prefixed si units
    ('cm', centimeter),
    ('mm', millimeter),
    ('nm', nanometer),
    ('kg', kilogram),
    ('mg', milligram),
    ('ug', microgram),
    ('ms', millisecond),
    ('mV', millivolt),
    ('mL', milliliter),

    # assorted prefixed si units (from suffixes)
    ('Gs', create_prefixed_unit(second, PREFIXES['G'])),
    ('MHz', create_prefixed_unit(hertz, PREFIXES['M'])),
    ('MN', create_prefixed_unit(newton, PREFIXES['M'])),
    ('kHz', create_prefixed_unit(hertz, PREFIXES['k'])),
    ('kJ', create_prefixed_unit(joule, PREFIXES['k'])),
    ('kN', create_prefixed_unit(newton, PREFIXES['k'])),
    ('kPa', create_prefixed_unit(pascal, PREFIXES['k'])),
    ('ks', create_prefixed_unit(second, PREFIXES['k'])),
    ('kW', create_prefixed_unit(watt, PREFIXES['k'])),
    ('mA', create_prefixed_unit(ampere, PREFIXES['m'])),
    ('mH', create_prefixed_unit(henry, PREFIXES['m'])),
    ('mV', create_prefixed_unit(volt, PREFIXES['m'])),
    ('mW', create_prefixed_unit(watt, PREFIXES['m'])),
    ('uA', create_prefixed_unit(ampere, PREFIXES['mu'])),
    ('uF', create_prefixed_unit(farad, PREFIXES['mu'])),
    ('uH', create_prefixed_unit(henry, PREFIXES['mu'])),
    ('uS', create_prefixed_unit(siemens, PREFIXES['mu'])),
    ('nF', create_prefixed_unit(farad, PREFIXES['n'])),
    ('nL', create_prefixed_unit(liter, PREFIXES['n'])),
    ('pF', create_prefixed_unit(farad, PREFIXES['p'])),
    ('fF', create_prefixed_unit(farad, PREFIXES['f'])),

    # prefixed units by full name
    ('millivolt', millivolt),
    ('millivolts', millivolt),
    ('Millivolt', millivolt),
    ('Millivolts', millivolt),

    ('Megajoules', create_prefixed_unit(joule, PREFIXES['M'])),

    # prefix latex + unit abbrev
    ('\\mu g', microgram),
    ('\\mu s', microsecond),
    ('\\mu A', create_prefixed_unit(ampere, PREFIXES['mu'])),
    ('\\mu V', create_prefixed_unit(volt, PREFIXES['mu'])),
    ('\\mu C', create_prefixed_unit(coulomb, PREFIXES['mu'])),
    ('\\mu F', create_prefixed_unit(farad, PREFIXES['mu'])),
    ('\\mu H', create_prefixed_unit(henry, PREFIXES['mu'])),

    # prefix latex + unit latex
    ('\\mu \\Omega ', microohm),

    # prefix abbrev + unit latex
    ('M\\Omega ', create_prefixed_unit(ohm, PREFIXES['M'])),
    ('k\\Omega ', create_prefixed_unit(ohm, PREFIXES['k'])),
    ('mu \\Omega ', microohm),

    # only allow certain constants
    ('c', speed_of_light),
    ('amu', atomic_mass_constant),
    ('eV', electronvolt),

    # additional prefixed units (not defined in sympy)
    ('mCi', create_prefixed_unit(curie, PREFIXES['m'])),
    ('MeV', create_prefixed_unit(electronvolt, PREFIXES['M'])),
    ('mbar', create_prefixed_unit(bar, PREFIXES['m'])),
    # binary prefixed unit
    ('pebibit', create_prefixed_unit(bit, BIN_PREFIXES['Pi'])),

    # additional aliases
    ('\\degree ', degree),
    ('\\%', percent),
    ('amp', ampere),
    ('amps', ampere),
    ('Amp', ampere),
    ('Amps', ampere),
    ('sec', second),
    ('secs', second),
    ('min', minute),
    ('mins', minute),
    ('hr', hour),
    ('hrs', hour),
    ('yr', year),
    ('yrs', year),
    ('lb', pound),
    ('lbs', pound),
    ('in', inch),

    # additional units
    ('lbf', lbf),
    ('slug', slug),
    ('cal', cal),
    ('kcal', kcal),
    ('btu', btu),
    ('\\degree C', degC),
    ('degC', degC),
    ('\\degree F', degF),
    ('degF', degF),
    ('dB', dB),

    # trailing spaces are stripped
    ('\\degree C\\: ', degC),
    ('years\\: ', year),

    # compound unit expressions
    ('kg\\times \\frac{m}{s^{2}}', _Mul(kilogram, meter, _Pow(_Pow(second, 2), -1))),
    ('kg*m^{2}s^{-3}', _Mul(kilogram, _Pow(meter, 2), _Pow(second, -3))),

    # space as multiplication
    ('kg\\: m', _Mul(kilogram, meter)),

    # assorted compound unit expressions (from suffixes)
    ('degC/W', _Mul(degC, _Pow(watt, -1))),
    ('\\degree C/W', _Mul(degC, _Pow(watt, -1))),
    ('\\frac{\\degree C}{W}', _Mul(degC, _Pow(watt, -1))),
    ('\\frac{\\mu g}{m^{3}}', _Mul(microgram, _Pow(_Pow(meter, 3), -1))),
    ('\\frac{kg}{m^{3}}', _Mul(kilogram, _Pow(_Pow(meter, 3), -1))),
    ('\\frac{kg}{s}', _Mul(kilogram, _Pow(second, -1))),
    ('\\frac{kg\\: m}{s}', _Mul(_Mul(kilogram, meter), _Pow(second, -1))),
    ('\\frac{km}{hr}', _Mul(kilometer, _Pow(hour, -1))),
    ('\\frac{1}{\\degree C}', _Mul(1, _Pow(degC, -1))),
    ('\\frac{1}{m}', _Mul(1, _Pow(meter, -1))),
    ('\\frac{1}{s}', _Mul(1, _Pow(second, -1))),
    ('\\frac{A}{\\mu s}', _Mul(ampere, _Pow(microsecond, -1))),
    ('\\frac{ft}{s}', _Mul(foot, _Pow(second, -1))),
    ('\\frac{ft^{3}}{s}', _Mul(_Pow(foot, 3), _Pow(second, -1))),
    ('\\frac{g}{mol}', _Mul(gram, _Pow(mole, -1))),
    ('\\frac{J}{kg\\: K}', _Mul(joule, _Pow(_Mul(kilogram, kelvin), -1))),
    ('\\frac{kJ}{mol}', _Mul(create_prefixed_unit(joule, PREFIXES['k']), _Pow(mole, -1))),
    ('\\frac{lbf}{ft^{2}}', _Mul(lbf, _Pow(_Pow(foot, 2), -1))),
    ('\\frac{m}{s}', _Mul(meter, _Pow(second, -1))),
    ('\\frac{m}{s^{2}}', _Mul(meter, _Pow(_Pow(second, 2), -1))),
    ('\\frac{m^{3}}{s}', _Mul(_Pow(meter, 3), _Pow(second, -1))),
    ('\\frac{mV}{\\mu s}', _Mul(create_prefixed_unit(volt, PREFIXES['m']), _Pow(microsecond, -1))),
    ('\\frac{N}{m}', _Mul(newton, _Pow(meter, -1))),
    ('\\frac{N}{m^{2}}', _Mul(newton, _Pow(_Pow(meter, 2), -1))),
    ('\\frac{rad}{sec}', _Mul(rad, _Pow(second, -1))),
    ('\\frac{T}{A}', _Mul(tesla, _Pow(ampere, -1))),
    ('\\frac{V}{\\mu s}', _Mul(volt, _Pow(microsecond, -1))),
    ('\\frac{V}{m}', _Mul(volt, _Pow(meter, -1))),
    ('\\left(\\frac{W}{m^{2}}\\right)', _Mul(watt, _Pow(_Pow(meter, 2), -1))),
    ('kg\\cdot m', _Mul(kilogram, meter)),
    ('kg\\cdot m^{2}', _Mul(kilogram, _Pow(meter, 2))),
    ('kg\\: m^{2}', _Mul(kilogram, _Pow(meter, 2))),
    ('mm^{2}', _Pow(millimeter, 2)),
    ('1/hr', _Mul(1, _Pow(hour, -1))),
    ('ft/s', _Mul(foot, _Pow(second, -1))),
    ('ft^{3}/s', _Mul(_Pow(foot, 3), _Pow(second, -1))),
    ('ft3/s', _Mul(_Mul(foot, 3), _Pow(second, -1))),
    ('g/mol', _Mul(gram, _Pow(mole, -1))),
    ('in^{2}', _Pow(inch, 2)),
    ('in^{3}', _Pow(inch, 3)),
    ('hr^{-1}', _Pow(hour, -1)),
    ('L/day', _Mul(liter, _Pow(day, -1))),
    ('L/hr', _Mul(liter, _Pow(hour, -1))),
    ('lb/ft2', _Mul(pound, _Pow(_Mul(foot, 2), -1))),
    ('m/s', _Mul(meter, _Pow(second, -1))),
    ('m/s^{2}', _Mul(meter, _Pow(_Pow(second, 2), -1))),
    ('m^{2}', _Pow(meter, 2)),
    ('m^{2}/s^{2}', _Mul(_Pow(meter, 2), _Pow(_Pow(second, 2), -1))),
    ('m^{3}', _Pow(meter, 3)),
    ('m^{3}/s', _Mul(_Pow(meter, 3), _Pow(second, -1))),
    ('m3/s', _Mul(_Mul(meter, 3), _Pow(second, -1))),
    ('mg/hr', _Mul(milligram, _Pow(hour, -1))),
    ('mL/day', _Mul(milliliter, _Pow(day, -1))),
    ('mL/hr', _Mul(milliliter, _Pow(hour, -1))),
    ('N/m^{2}', _Mul(newton, _Pow(_Pow(meter, 2), -1))),
    ('N\\: s\\: /\\: m^{2}', _Mul(_Mul(newton, second), _Pow(_Pow(meter, 2), -1))),
    ('N\\cdot m', _Mul(newton, meter)),
    ('N\\cdot m^{2}', _Mul(newton, _Pow(meter, 2))),
    ('nm^{-1}', _Pow(nanometer, -1)),
    ('rad/s', _Mul(rad, _Pow(second, -1))),
    ('rad/sec', _Mul(rad, _Pow(second, -1))),
    ('rad\\: /\\: sec', _Mul(rad, _Pow(second, -1))),
    ('s^{-1}', _Pow(second, -1)),
    ('slugs/ft3', _Mul(slug, _Pow(_Mul(foot, 3), -1))),
    ('V/us', _Mul(volt, _Pow(microsecond, -1))),
    ('V\\cdot m', _Mul(volt, meter)),
    ('kJ/mol', _Mul(create_prefixed_unit(joule, PREFIXES['k']), _Pow(mole, -1))),
    ('kN/m', _Mul(create_prefixed_unit(newton, PREFIXES['k']), _Pow(meter, -1))),
]


@pytest.mark.parametrize('input, output', unit_examples)
def test_covert_unit_should_succeed(input, output):
    assert_equal(input, output, parse_letters_as_units=True)


bad_unit_examples = [
    # non-Quantity, numeric or symbols
    '1',
    'E-9',
    'E3',
    'x+y',
    '\\frac{L_{1}}{R_{total}}',
    'apples',
    'apples\\times grams',
    'pen\\times pineapple\\times apple\\times pen',
    'red\\: delicious',
    'carbon\\: atoms',
    'Pokeballs\\: with\\: her\\: income',
    'year\\left(s\\right)\\: of\\: her\\: life\\: due\\: to\\: bickering',

    # prefix + non-Quantity
    '\\mu 1',
    '\\mu x',

    # unsupported constant / prefix w/o Quantity
    'G',
    'giga',
    'pico',

    # combined prefix with non-abbreviated name
    'Mohms',  # megaohms or M\\Omega
    'kohms',  # killiohms or k\\Omega
    'kg/kmole',  # kmol
    'mb',  # millibar or mbar

    # operatorname and other latex cmds
    '\\$',
    '\\operatorname{cm}',
    '\\operatorname{kg}',
    '\\frac{J}{\\operatorname{kg}K}',
    '\\sec ',
    '\\min ',

    # letters or subscripts after valid units
    'A\\: peak',
    'ADC',
    'Ap',
    'Hz\\: \\left(10\\%\\: tolerance\\: for\\: this\\: answer\\right)',
    'V_{pp}',
    'V_{RMS}',
    'Vpeak',
    'Vrms',

    # unit sentences
    'cubic\\: inches',
    'meters\\: per\\: second',
    'meters\\: per\\: second\\: squared',
    'miles\\: per\\: hour',
    'square\\: inches',

    # unicode
    'kΩ',
    'º',
    '°C\\: ',
    'Ω',

    # valid unit combined with invalid unit
    'MeV/nucleon',

    # assorted invalid units
    '\\degree s',  # plural degrees
    '\\degree \\: C',  # invalid space
    'deg\\: C',
    'degrees\\: Celsius',
    'o',  # meant to be \degree
    'msec',

    # other unsupported units
    'PPS',  # pulses per second
    'ft.lbf',  # lbf⋅ft, lb-ft, "pound-foot", lb-ft or ft-lb
    'kN.m',
]


@pytest.mark.parametrize('input', bad_unit_examples)
def test_covert_unit_should_fail(input):
    did_fail = False
    try:
        result = process_sympy(input, parse_letters_as_units=True)
        did_fail = is_or_contains_instance(result, Symbol) or not is_or_contains_instance(result, Quantity)
    except Exception as e:
        did_fail = True
    assert did_fail


# TODO: define additional units, if needed
unsupported_unit_examples = [
    ('\\frac{dB}{decade}', _Mul(gram, _Pow(gram, -1))),
    ('\\frac{dB}{octave}', _Mul(gram, _Pow(gram, -1))),
    ('\\frac{Gs}{A}', _Mul(gauss, _Pow(ampere, -1))),
    # R - https://en.wikipedia.org/wiki/Roentgen_(unit)
    ('\\frac{R}{hr}', _Mul(gram, _Pow(hour, -1))),
    ('\\frac{mR}{hr}', _Mul(gram, _Pow(hour, -1))),
    ('\\frac{Rad}{s}', _Mul(gram, _Pow(second, -1))),
    ('cfm', gram),
    ('ft/(cfm)^{2}', _Mul(foot, _Pow(gram, -1))),
    ('cfs', gram),
    ('dBV', gram),
    ('gpm', gram),
    ('Hp', gram),
    ('mph', _Mul(mile, _Pow(hour, -1))),
    ('knot', gram),
    ('lbf-in', gram),
    ('lbf.ft', gram),
    # M (mol/L) - conflicts with mega prefix
    ('M', gram),
    ('psia', gram),
    ('rpm', gram),
    ('mcg', microgram),
]
