import pytest
from sympy import Rational, pi
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
    # Other
    percent,
    degree,
    rad,
    minute, hour, day, year,
    foot, inch, mile, pound, yard,
    curie, gauss,
    atomic_mass_constant,
    atmosphere,
    electronvolt,
    bar, psi, bit, nmi,
    hbar,
    dyne,
    astronomical_unit, elementary_charge
)
from latex2sympy.latex2sympy import process_sympy
from latex2sympy.units.additional_units import (
    liter,
    lbf,
    slug,
    cal, kcal,
    btu,
    degC, degF,
    dB,
    mph, knot,
    # lumen,
    cfm, cfs,
    rood, acre,
    sievert,
    ounce,
    parsec,
    cc,
    molar
)
from latex2sympy.units import UNIT_ALIASES, create_prefixed_unit, convert_to
from .context import _Mul, _Pow, _Add, assert_equal, compare

# create local vars for prefixed units for convenience
millivolt = UNIT_ALIASES['millivolt']
microohm = UNIT_ALIASES['microohm']
milliliter = UNIT_ALIASES['milliliter']

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
    ('mu\\Omega ', microohm),
    ('u\\Omega ', microohm),

    # only allow certain constants
    ('c', speed_of_light),
    ('amu', atomic_mass_constant),
    ('eV', electronvolt),
    ('e', elementary_charge),

    # additional prefixed units (not defined in sympy)
    ('mCi', create_prefixed_unit(curie, PREFIXES['m'])),
    ('MeV', create_prefixed_unit(electronvolt, PREFIXES['M'])),
    ('mbar', create_prefixed_unit(bar, PREFIXES['m'])),
    # binary prefixed unit
    ('pebibit', create_prefixed_unit(bit, BIN_PREFIXES['Pi'])),
    ('mM', create_prefixed_unit(molar, PREFIXES['m'])),
    ('\\mu M', create_prefixed_unit(molar, PREFIXES['mu'])),

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
    ('mcg', microgram),
    ('dyn', dyne),
    ('u', atomic_mass_constant),

    # additional units
    ('lbf', lbf),
    ('slug', slug),
    ('cal', cal),
    ('kcal', kcal),
    ('btu', btu),
    ('\\degree C', degC),
    ('degC', degC),
    ('celsius', degC),
    ('\\degree F', degF),
    ('degF', degF),
    ('fahrenheit', degF),
    ('dB', dB),
    ('mph', mph),
    ('knot', knot),
    ('cfm', cfm),
    ('cfs', cfs),
    # ('lm', lumen),
    ('rood', rood),
    ('acre', acre),
    ('Sv', sievert),
    ('oz', ounce),
    ('pc', parsec),
    ('cc', cc),
    ('M', molar),

    # TODO: LON-CAPA units
    # 'hbar',  # conflicts with hectobar
    # 'lm',  # lumen
    # 'rpm', 'rpms',  # rounds per minute

    # TODO: additional units (from suffixes)
    # 'decade',
    # 'octave',
    # 'Gs',  # for gauss - conflicts with gigasecond
    # 'R',  # legacy unit for radiation - https://en.wikipedia.org/wiki/Roentgen_(unit)
    # 'mR',
    # 'rad', 'Rad',  # conflicts with radians, CGS unit
    # 'dBV',
    # 'gpm',  # multiple versions exist, gallons per minute
    # 'hp',  # multiple versions exist, horse power
    # 'lbf.ft', 'lb-ft,  # "pound-foot" (torque), sometimes still called a "foot-pound"
    # 'lbf-in',  # "pound-inch" 1/12 of "pound-foot"
    # 'ft⋅lbf', 'ft⋅lb'  # "foot-pound" (energy)
    # 'psia',

    # trailing spaces are stripped
    ('\\degree C\\: ', degC),
    ('years\\: ', year),

    # compound unit expressions
    ('kg\\times \\frac{m}{s^{2}}', _Mul(kilogram, meter, _Pow(_Pow(second, 2), -1))),
    ('kg*m^{2}s^{-3}', _Mul(kilogram, _Pow(meter, 2), _Pow(second, -3))),

    # space as multiplication
    ('kg\\: m', _Mul(kilogram, meter)),

    # assorted compound unit expressions (from suffixes)
    ('deg\\: C', _Mul(degree, coulomb)),
    ('\\degree \\: C', _Mul(degree, coulomb)),
    ('degrees\\: Celsius', _Mul(degree, degC)),

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
    ('molar*ohm', _Mul(molar, ohm)),
    ('M*\\Omega', _Mul(molar, ohm)),
]


@pytest.mark.parametrize('input, output', unit_examples)
def test_parse_as_unit_should_succeed(input, output):
    assert_equal(input, output, parse_as_unit=True)


bad_unit_examples = [
    # non-Quantity, numeric value or symbols
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

    # invalid prefix + quantity
    '\\mu slug',

    # unsupported constant or prefix w/o Quantity
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

    # unit phrases
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
    '\\degree s',  # plural degrees w/ latex
    'o',  # meant to be \degree
    'msec',  # ms

    # other unsupported units
    'PPS',  # pulses per second
    'kN.m',
]


@pytest.mark.parametrize('input', bad_unit_examples)
def test_parse_as_unit_should_fail(input):
    with pytest.raises(Exception):
        process_sympy(input, parse_as_unit=True)


convert_to_unit_examples = [
    ('kg', 'g', _Mul(1000, gram)),
    ('L', 'mL', _Mul(1000, milliliter)),
    ('m^{3}', 'L', _Mul(1000, liter)),
    # additional units
    ('\\frac{mile}{hour}', 'mph', mph),
    ('\\frac{feet}{second}', 'mph', _Mul(mph, Rational(15, 22))),
    ('\\frac{nmi}{hour}', 'knot', knot),
    # ('sr*cd', 'lm', lumen),
    ('\\frac{foot^{3}}{minute}', 'cfm', cfm),
    ('\\frac{foot^{3}}{second}', 'cfs', cfs),
    ('cfs', 'cfm', _Mul(60, cfm)),
    ('rood', 'yard', _Mul(1210, _Pow(yard, 2))),
    ('acre', 'yard', _Mul(4840, _Pow(yard, 2))),
    ('\\frac{J}{kg}', 'Sv', sievert),
    ('lb', 'oz', _Mul(ounce, 16)),
    ('parsec', 'AU', _Mul(648000, _Pow(pi, -1), astronomical_unit)),
    ('cm^{3}', 'cc', cc),
    ('mol/L', 'M', molar),
    ('mmol/L', 'M', _Mul(Rational(1, 1000), molar))
]


@pytest.mark.parametrize('src, dest, expected', convert_to_unit_examples)
def test_covert_to_unit_should_succeed(src, dest, expected):
    src_unit = process_sympy(src, parse_as_unit=True)
    dest_unit = process_sympy(dest, parse_as_unit=True)
    src_unit_converted = convert_to(src_unit, dest_unit)
    compare(src_unit_converted, expected)


convert_to_unit_incompatible_examples = [
    ('kg', 'm'),
    ('Gy', 'Sv')
]


@pytest.mark.parametrize('src, dest', convert_to_unit_incompatible_examples)
def test_covert_to_unit_should_fail(src, dest):
    src_unit = process_sympy(src, parse_as_unit=True)
    dest_unit = process_sympy(dest, parse_as_unit=True)
    src_unit_converted = convert_to(src_unit, dest_unit)
    # if units are incompatible, the src unit will not change
    compare(src_unit, src_unit_converted)