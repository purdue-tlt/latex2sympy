from sympy import latex
from sympy.physics.units.prefixes import Prefix, PREFIXES, micro, prefix_unit

kibi = Prefix('kibi', 'Ki', 10, 2)
mebi = Prefix('mebi', 'Mi', 20, 2)
gibi = Prefix('gibi', 'Gi', 30, 2)
tebi = Prefix('tebi', 'Ti', 40, 2)
pebi = Prefix('pebi', 'Pi', 50, 2)
exbi = Prefix('exbi', 'Ei', 60, 2)

# https://physics.nist.gov/cuu/Units/binary.html
BIN_PREFIXES = {
    'Ki': kibi,
    'Mi': mebi,
    'Gi': gibi,
    'Ti': tebi,
    'Pi': pebi,
    'Ei': exbi,
}

ALL_PREFIXES = {**PREFIXES, **BIN_PREFIXES}

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
