import sympy


def is_or_contains_instance(expr, type):
    '''
    Determine if the expression `expr` is or contains an instance of `type`
    '''
    if expr is None:  # pragma: no cover
        return False
    if isinstance(expr, type):
        return True
    if not hasattr(expr, 'args') or len(expr.args) <= 0:  # pragma: no cover
        return False

    for arg in expr.args:
        if is_or_contains_instance(arg, type):
            return True

    return False


def create_rational_or_number(text):
    try:
        return sympy.Rational(text)
    except (TypeError, ValueError):  # pragma: no cover
        return sympy.Number(text)


def add_flat(lh, rh):
    if hasattr(lh, 'is_Add') and lh.is_Add or hasattr(rh, 'is_Add') and rh.is_Add:
        args = []
        if hasattr(lh, 'is_Add') and lh.is_Add:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_Add') and rh.is_Add:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.Add(*args, evaluate=False)
    else:
        return sympy.Add(lh, rh, evaluate=False)


def mat_add_flat(lh, rh):
    if hasattr(lh, 'is_MatAdd') and lh.is_MatAdd or hasattr(rh, 'is_MatAdd') and rh.is_MatAdd:
        args = []
        if hasattr(lh, 'is_MatAdd') and lh.is_MatAdd:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_MatAdd') and rh.is_MatAdd:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.MatAdd(*args, evaluate=False)
    else:
        return sympy.MatAdd(lh, rh, evaluate=False)


def mul_flat(lh, rh):
    if hasattr(lh, 'is_Mul') and lh.is_Mul or hasattr(rh, 'is_Mul') and rh.is_Mul:
        args = []
        if hasattr(lh, 'is_Mul') and lh.is_Mul:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_Mul') and rh.is_Mul:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.Mul(*args, evaluate=False)
    else:
        return sympy.Mul(lh, rh, evaluate=False)


def mat_mul_flat(lh, rh):
    if hasattr(lh, 'is_MatMul') and lh.is_MatMul or hasattr(rh, 'is_MatMul') and rh.is_MatMul:
        args = []
        if hasattr(lh, 'is_MatMul') and lh.is_MatMul:
            args += list(lh.args)
        else:
            args += [lh]
        if hasattr(rh, 'is_MatMul') and rh.is_MatMul:
            args = args + list(rh.args)
        else:
            args += [rh]
        return sympy.MatMul(*args, evaluate=False)
    else:
        return sympy.MatMul(lh, rh, evaluate=False)


def create_gcd_lcm(f, args):
    '''
    Return the result of gcd() or lcm(), as UnevaluatedExpr

    f: str - name of function ('gcd' or 'lcm')
    args: List[Expr] - list of function arguments
    '''

    args = tuple(map(sympy.nsimplify, args))

    # gcd() and lcm() don't support evaluate=False
    return sympy.UnevaluatedExpr(getattr(sympy, f)(args))


def create_floor(expr):
    '''
    Apply floor() then return the floored expression.

    expr: Expr - sympy expression as an argument to floor()
    '''
    return sympy.functions.floor(expr, evaluate=False)


def create_ceil(expr):
    '''
    Apply ceil() then return the ceil-ed expression.

    expr: Expr - sympy expression as an argument to ceil()
    '''
    return sympy.functions.ceiling(expr, evaluate=False)
