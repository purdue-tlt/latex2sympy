import sympy.physics.units.prefixes as sympy_prefixes
from sympy import latex, Symbol
from sympy.physics.units.prefixes import micro, Prefix, prefix_unit

# correctly define the binary prefix abbreviations
# sympy had them all defined as 'Y' in the `Prefix` classes (but were correct in `BIN_PREFIXES`)
kibi = Prefix('kibi', 'Ki', 10, 2)
mebi = Prefix('mebi', 'Mi', 20, 2)
gibi = Prefix('gibi', 'Gi', 30, 2)
tebi = Prefix('tebi', 'Ti', 40, 2)
pebi = Prefix('pebi', 'Pi', 50, 2)
exbi = Prefix('exbi', 'Ei', 60, 2)
# define additional IEC prefixes
zebi = Prefix('zebi', 'Zi', 70, 2)
yobi = Prefix('yobi', 'Yi', 80, 2)

# https://physics.nist.gov/cuu/Units/binary.html
# https://en.wikipedia.org/wiki/Byte#Multiple-byte_units
BIN_PREFIXES = {'Ki': kibi, 'Mi': mebi, 'Gi': gibi, 'Ti': tebi, 'Pi': pebi, 'Ei': exbi, 'Zi': zebi, 'Yi': yobi}

# define addtional SI / Metric prefixes, added in 2022
# https://www.nist.gov/pml/owm/metric-si-prefixes
quetta = Prefix('quetta', Symbol('Q'), 30)  # wrap abbrev in `Symbol` to avoid issue in `Prefix` ctor calling `sympify`
ronna = Prefix('ronna', 'R', 27)
ronto = Prefix('ronto', 'r', -27)
quecto = Prefix('quecto', 'q', -30)

NEW_SI_PREFIXES = {'Q': quetta, 'R': ronna, 'r': ronto, 'q': quecto}

SI_PREFIXES = {**sympy_prefixes.PREFIXES, **NEW_SI_PREFIXES}

# filter si prefixes to the subset allowed for information (bit, byte)
INFORMATION_SI_PREFIXES = {}
for abbrev, prefix in SI_PREFIXES.items():
    if prefix.args[2] > 2:
        INFORMATION_SI_PREFIXES[abbrev] = prefix

ALL_PREFIXES = {**SI_PREFIXES, **BIN_PREFIXES}

# construct a dict of every allowed string alias of each prefix
# store every prefix’s name, abbrev, and latex repr as an alias
PREFIX_ALIASES = {}

for abbrev, prefix in ALL_PREFIXES.items():
    # abbrev
    PREFIX_ALIASES[abbrev] = prefix
    # name
    prefix_name = str(prefix.name)
    PREFIX_ALIASES[prefix_name] = prefix
    # latex
    prefix_latex = latex(prefix)
    if '\\text' not in prefix_latex:
        PREFIX_ALIASES[prefix_latex] = prefix

# add additional custom prefix alias
PREFIX_ALIASES['u'] = micro


def create_prefixed_unit(unit, prefix):
    '''
    combine the prefix and unit into a new `Quantity`
    '''
    # `prefix_unit` accepts a dict of prefixes, so construct one
    prefixes = {}
    prefixes[prefix.abbrev] = prefix
    prefixed_units = prefix_unit(unit, prefixes)
    return prefixed_units[0]
