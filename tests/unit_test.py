import pytest
from sympy import Rational, pi
from sympy.physics.units.definitions.unit_definitions import (
    # MKS - "meter, kilogram, second"
    meter, gram, kilogram, second, joule, newton, watt, pascal, hertz, speed_of_light,
    # MKSA - based on MKS, "meter, kilogram, second, ampere"
    ampere, volt, ohm, siemens, farad, henry, coulomb, tesla, weber,
    # SI - based on MKSA, added kelvin, candela and mole
    mole, kelvin, lux,
    candela, becquerel,
    katal,
    # Derived
    kilometer, centimeter, millimeter, nanometer,
    milligram, microgram,
    millisecond, microsecond,
    # Other
    percent, permille,
    degree, rad, steradian, angular_mil,
    minute, hour, day, year,
    foot, inch, pound, yard,
    curie,
    atomic_mass_constant,
    atmosphere,
    electronvolt,
    bar, psi,
    astronomical_unit, elementary_charge,
    dioptre
)
from latex2sympy.latex2sympyAsUnit import process_sympy_as_unit
from latex2sympy.units.prefixes import SI_PREFIXES, BIN_PREFIXES
from latex2sympy.units.unit_definitions import (
    liter,
    gray,
    bit,
    byte,
    lbf,
    slug,
    cal,
    btu,
    degC, degF,
    dB,
    mph, knot,
    lumen,
    cfm, cfs,
    rood, acre,
    sievert,
    parsec,
    cc,
    molar,
    rpm
)
from latex2sympy.units import UNIT_ALIASES, create_prefixed_unit, convert_to
from .context import _Mul, _Pow, _Add, assert_equal, compare

# create local vars for prefixed units for convenience
millivolt = UNIT_ALIASES['millivolt']
microohm = UNIT_ALIASES['microohm']
milliliter = UNIT_ALIASES['milliliter']
kcal = UNIT_ALIASES['kcal']

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
    ('sr', steradian),

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
    ('Gs', create_prefixed_unit(second, SI_PREFIXES['G'])),
    ('MHz', create_prefixed_unit(hertz, SI_PREFIXES['M'])),
    ('MN', create_prefixed_unit(newton, SI_PREFIXES['M'])),
    ('kHz', create_prefixed_unit(hertz, SI_PREFIXES['k'])),
    ('kJ', create_prefixed_unit(joule, SI_PREFIXES['k'])),
    ('kN', create_prefixed_unit(newton, SI_PREFIXES['k'])),
    ('kPa', create_prefixed_unit(pascal, SI_PREFIXES['k'])),
    ('ks', create_prefixed_unit(second, SI_PREFIXES['k'])),
    ('kW', create_prefixed_unit(watt, SI_PREFIXES['k'])),
    ('mA', create_prefixed_unit(ampere, SI_PREFIXES['m'])),
    ('mH', create_prefixed_unit(henry, SI_PREFIXES['m'])),
    ('mV', create_prefixed_unit(volt, SI_PREFIXES['m'])),
    ('mW', create_prefixed_unit(watt, SI_PREFIXES['m'])),
    ('uA', create_prefixed_unit(ampere, SI_PREFIXES['mu'])),
    ('uF', create_prefixed_unit(farad, SI_PREFIXES['mu'])),
    ('uH', create_prefixed_unit(henry, SI_PREFIXES['mu'])),
    ('uS', create_prefixed_unit(siemens, SI_PREFIXES['mu'])),
    ('nF', create_prefixed_unit(farad, SI_PREFIXES['n'])),
    ('nL', create_prefixed_unit(liter, SI_PREFIXES['n'])),
    ('pF', create_prefixed_unit(farad, SI_PREFIXES['p'])),
    ('fF', create_prefixed_unit(farad, SI_PREFIXES['f'])),

    # prefixed units by full name
    ('millivolt', millivolt),
    ('millivolts', millivolt),
    ('Millivolt', millivolt),
    ('Millivolts', millivolt),

    ('Megajoules', create_prefixed_unit(joule, SI_PREFIXES['M'])),

    # prefix latex + unit abbrev
    ('\\mu g', microgram),
    ('\\mu s', microsecond),
    ('\\mu A', create_prefixed_unit(ampere, SI_PREFIXES['mu'])),
    ('\\mu V', create_prefixed_unit(volt, SI_PREFIXES['mu'])),
    ('\\mu C', create_prefixed_unit(coulomb, SI_PREFIXES['mu'])),
    ('\\mu F', create_prefixed_unit(farad, SI_PREFIXES['mu'])),
    ('\\mu H', create_prefixed_unit(henry, SI_PREFIXES['mu'])),

    # prefix latex + unit latex
    ('\\mu \\Omega ', microohm),

    # prefix abbrev + unit latex
    ('M\\Omega ', create_prefixed_unit(ohm, SI_PREFIXES['M'])),
    ('k\\Omega ', create_prefixed_unit(ohm, SI_PREFIXES['k'])),
    ('mu\\Omega ', microohm),
    ('u\\Omega ', microohm),

    # only allow certain constants
    ('c', speed_of_light),
    ('amu', atomic_mass_constant),
    ('eV', electronvolt),
    ('e', elementary_charge),

    # additional prefixed units (not defined in sympy)
    ('MeV', create_prefixed_unit(electronvolt, SI_PREFIXES['M'])),
    ('mCi', create_prefixed_unit(curie, SI_PREFIXES['m'])),
    ('mbar', create_prefixed_unit(bar, SI_PREFIXES['m'])),
    ('mM', create_prefixed_unit(molar, SI_PREFIXES['m'])),
    ('\\mu M', create_prefixed_unit(molar, SI_PREFIXES['mu'])),
    ('mcal', create_prefixed_unit(cal, SI_PREFIXES['m'])),
    ('mGy', create_prefixed_unit(gray, SI_PREFIXES['m'])),
    # binary prefixed units
    ('pebibit', create_prefixed_unit(bit, BIN_PREFIXES['Pi'])),
    ('Pibit', create_prefixed_unit(bit, BIN_PREFIXES['Pi'])),
    ('Pib', create_prefixed_unit(bit, BIN_PREFIXES['Pi'])),
    # new binary prefixes
    ('zebibyte', create_prefixed_unit(byte, BIN_PREFIXES['Zi'])),
    ('yobibit', create_prefixed_unit(bit, BIN_PREFIXES['Yi'])),
    # si prefixed information units
    ('megabit', create_prefixed_unit(bit, SI_PREFIXES['M'])),
    ('Mbit', create_prefixed_unit(bit, SI_PREFIXES['M'])),
    ('Mb', create_prefixed_unit(bit, SI_PREFIXES['M'])),
    ('gigabyte', create_prefixed_unit(byte, SI_PREFIXES['G'])),
    ('GB', create_prefixed_unit(byte, SI_PREFIXES['G'])),
    # new si prefixes
    ('Qg', create_prefixed_unit(gram, SI_PREFIXES['Q'])),
    ('Rm', create_prefixed_unit(meter, SI_PREFIXES['R'])),
    ('rg', create_prefixed_unit(gram, SI_PREFIXES['r'])),
    ('qm', create_prefixed_unit(meter, SI_PREFIXES['q'])),

    # additional aliases
    ('\\degree ', degree),
    ('\\%', percent),
    ('amp', ampere),
    ('amps', ampere),
    ('Amp', ampere),
    ('Amps', ampere),
    ('sec', second),
    ('secs', second),
    ('Sec', second),
    ('Secs', second),
    ('min', minute),
    ('mins', minute),
    ('Min', minute),
    ('Mins', minute),
    ('hr', hour),
    ('hrs', hour),
    ('Hr', hour),
    ('Hrs', hour),
    ('yr', year),
    ('yrs', year),
    ('Yr', year),
    ('Yrs', year),
    ('lb', pound),
    ('lbs', pound),
    ('in', inch),
    ('mcg', microgram),
    ('u', atomic_mass_constant),

    ('litre', liter),
    ('Litre', liter),
    ('litres', liter),
    ('Litres', liter),
    ('millilitre', create_prefixed_unit(liter, SI_PREFIXES['m'])),
    ('millilitres', create_prefixed_unit(liter, SI_PREFIXES['m'])),
    ('Millilitre', create_prefixed_unit(liter, SI_PREFIXES['m'])),
    ('Millilitres', create_prefixed_unit(liter, SI_PREFIXES['m'])),

    ('metre', meter),
    ('Metre', meter),
    ('metres', meter),
    ('Metres', meter),
    ('millimetre', create_prefixed_unit(meter, SI_PREFIXES['m'])),
    ('millimetres', create_prefixed_unit(meter, SI_PREFIXES['m'])),
    ('Millimetre', create_prefixed_unit(meter, SI_PREFIXES['m'])),
    ('Millimetres', create_prefixed_unit(meter, SI_PREFIXES['m'])),

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
    ('lm', lumen),
    ('rood', rood),
    ('acre', acre),
    ('Sv', sievert),
    ('pc', parsec),
    ('cc', cc),
    ('M', molar),
    ('rpm', rpm),

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
    ('\\frac{kJ}{mol}', _Mul(create_prefixed_unit(joule, SI_PREFIXES['k']), _Pow(mole, -1))),
    ('\\frac{lbf}{ft^{2}}', _Mul(lbf, _Pow(_Pow(foot, 2), -1))),
    ('\\frac{m}{s}', _Mul(meter, _Pow(second, -1))),
    ('\\frac{m}{s^{2}}', _Mul(meter, _Pow(_Pow(second, 2), -1))),
    ('\\frac{m^{3}}{s}', _Mul(_Pow(meter, 3), _Pow(second, -1))),
    ('\\frac{mV}{\\mu s}', _Mul(create_prefixed_unit(volt, SI_PREFIXES['m']), _Pow(microsecond, -1))),
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
    ('kJ/mol', _Mul(create_prefixed_unit(joule, SI_PREFIXES['k']), _Pow(mole, -1))),
    ('kN/m', _Mul(create_prefixed_unit(newton, SI_PREFIXES['k']), _Pow(meter, -1))),
    ('molar*ohm', _Mul(molar, ohm)),
    ('M*\\Omega', _Mul(molar, ohm)),
]


@pytest.mark.parametrize('input, output', unit_examples)
def test_parse_as_unit_should_succeed(input, output):
    parsed = process_sympy_as_unit(input)
    compare(parsed, output)


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

    # prefix after a compound Quantity
    '\\frac{m}{s}d',

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

    # unsupported CGS units
    'dyne',
    'erg',
    'statampere',
    'statcoulomb',
    'statvolt',
    'gauss',
    'maxwell',
    'debye',
    'oersted',

    # other unsupported units
    'quart',
    'planck',

    'ounce',
    'oz',
    'gallon',
    'decade',
    'octave',
    'R',
    'dbV',
    'gpm',
    'hp',

    'lbf⋅ft',
    'lbf.ft',
    'lb⋅in',
    'lb.in',
    'ft⋅lbf',
    'ft.lbf',
    'ft⋅lb',
    'ft.lb',

    'psia',

    'PPS',  # pulses per second
    'kN.m',

    '.',
    '..',
    'gram\\: .'
]


@pytest.mark.parametrize('input', bad_unit_examples)
def test_parse_as_unit_should_fail(input):
    with pytest.raises(Exception):
        process_sympy_as_unit(input)


convert_to_unit_examples = [
    # sympy included units
    ('kg', 'g', _Mul(1000, gram)),
    ('hertz', 'second', _Pow(second, -1)),
    ('s^{-1}', 'Hz', hertz),
    ('m^{-1}', 'dioptre', dioptre),
    ('percent', 'permille', _Mul(10, permille)),
    ('hectare', 'm', _Mul(10000, _Pow(meter, 2))),

    # added rad to angular_mil conversion
    ('rad', 'mil', _Mul(1000, angular_mil)),

    # conversion for fixed liter unit with abbrev
    ('L', 'mL', _Mul(1000, milliliter)),
    ('m^{3}', 'L', _Mul(1000, liter)),
    ('mGy', 'Gy', _Mul(Rational(1, 1000), gray)),
    ('\\frac{m^{2}}{s^{2}}', 'Gy', gray),

    # information - bit and byte
    ('mebibit', 'bit', _Mul(1048576, bit)),
    ('kb', 'bit', _Mul(1000, bit)),
    ('Mb/s', 'MB/s', _Mul(Rational(1, 8), _Pow(second, -1), create_prefixed_unit(byte, SI_PREFIXES['M']))),

    # added lumen - conversions with lux, candela, steradian
    ('lumen', 'sr*cd', _Mul(steradian, candela)),
    ('sr*cd', 'lumen', lumen),
    ('\\frac{cd*sr}{m^{2}}', 'lux', lux),
    ('lux*m^{2}', 'lumen', lumen),
    ('lux', '\\frac{lumen}{m^{2}}', _Mul(lumen, _Pow(_Pow(meter, 2), -1))),

    # additional units
    ('\\frac{mile}{hour}', 'mph', mph),
    ('\\frac{feet}{second}', 'mph', _Mul(mph, Rational(15, 22))),
    ('\\frac{nmi}{hour}', 'knot', knot),
    ('\\frac{foot^{3}}{minute}', 'cfm', cfm),
    ('\\frac{foot^{3}}{second}', 'cfs', cfs),
    ('cfs', 'cfm', _Mul(60, cfm)),
    ('rood', 'yard', _Mul(1210, _Pow(yard, 2))),
    ('acre', 'yard', _Mul(4840, _Pow(yard, 2))),
    ('\\frac{J}{kg}', 'Sv', sievert),
    ('parsec', 'AU', _Mul(648000, _Pow(pi, -1), astronomical_unit)),
    ('cm^{3}', 'cc', cc),
    ('mol/L', 'M', molar),
    ('mmol/L', 'M', _Mul(Rational(1, 1000), molar))
]


@pytest.mark.parametrize('src, dest, expected', convert_to_unit_examples)
def test_covert_to_unit_should_succeed(src, dest, expected):
    src_unit = process_sympy_as_unit(src)
    dest_unit = process_sympy_as_unit(dest)
    src_unit_converted = convert_to(src_unit, dest_unit)
    compare(src_unit_converted, expected)


convert_to_unit_incompatible_examples = [
    # basic - different dimensions
    ('kg', 'm'),
    # explicit gray != sievert
    ('Gy', 'Sv'),
    # rpm cannot convert
    ('rpm', 'Hz'),
    ('rpm', 'rad/s'),
    # cannot convert degC or degF
    ('degC', 'K'),
    ('degF', 'K'),
    ('degC', 'degF'),
]


@pytest.mark.parametrize('src, dest', convert_to_unit_incompatible_examples)
def test_covert_to_unit_should_fail(src, dest):
    src_unit = process_sympy_as_unit(src)
    dest_unit = process_sympy_as_unit(dest)
    with pytest.raises(Exception):
        convert_to(src_unit, dest_unit)
