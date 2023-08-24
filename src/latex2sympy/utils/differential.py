from sympy import Symbol

DIFFERENTIAL_PREFIX = 'differentialD-'


def is_differential_var(expr):
    prefix_len = len(DIFFERENTIAL_PREFIX)
    return isinstance(expr, Symbol) and len(expr.name) > prefix_len and expr.name[:prefix_len] == DIFFERENTIAL_PREFIX


def get_differential_var(expr):
    symbol_name = expr.name[14:]
    return Symbol(symbol_name, real=True, positive=True)
