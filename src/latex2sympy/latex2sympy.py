import hashlib
import json
import re

import sympy

from latex2sympy.lib import LATEXLexerToken, parseToJson
from latex2sympy.utils.differential import DIFFERENTIAL_PREFIX, get_differential_var, is_differential_var
from latex2sympy.utils.expression import (
    add_flat,
    create_ceil,
    create_floor,
    create_gcd_lcm,
    create_rational_or_number,
    mat_add_flat,
    mat_mul_flat,
    mul_flat,
)
from latex2sympy.utils.json import get_token, has_type_or_token

# replacement for `sympy.S.EmptySet` which can be printed to a string, or used in expression comparisons
EmptySet = sympy.Symbol('emptyset')


def process_sympy(latex: str, variable_values: dict = None):
    instance = LatexToSympy(latex, variable_values)
    return instance.process_sympy()


class LatexToSympy:
    def __init__(self, latex: str, variable_values: dict = None):
        self.latex = latex
        if variable_values is None:
            variable_values = {}
        if len(variable_values) > 0:
            self.variable_values = variable_values
        else:
            self.variable_values = {}

    def process_sympy(self):

        # pre-processing
        pre_processed_latex = self.pre_process_latex(self.latex)

        # process the input
        return_data = None
        json_string = parseToJson(pre_processed_latex)

        # print(json_string)

        math = json.loads(json_string)

        # if a list
        if 'relation_list' in math:
            return_data = []

            # go over list items
            relation_list = math.get('relation_list').get('relation_list_content')
            for list_item in relation_list.get('relation'):
                expr = self.convert_relation(list_item)
                return_data.append(expr)

        # if not, do default
        else:
            relation = math.get('relation')
            return_data = self.convert_relation(relation)

        return return_data

    def pre_process_latex(self, latex: str):
        '''
        pre-processing for issues the parser cannot handle

        find any single char sup/sub and wrap them in '{}'
        e.g. `4^26^2` => `4^{2}6^{2}`
        e.g. `x_22` => `x_{2}2`

        NOTE: this DOES MODIFY variable names so they can be parsed,
        but `atom.VARIABLE()` reverts to the original name, if needed, using `self.variable_name_dict`

        '''

        # pattern to find variable commands, with the first group being the name
        variable_regex = r'\\variable{([^}_]+?(_({[^}_]+?}|[^}_]))?)}'

        unwrapped_single_char_sub_sup_regex = r'([\^_])([0-9a-zA-Z])'

        # find all original variable names and make a mapping from new to original name
        variable_name_dict = {}
        variable_matches = re.finditer(variable_regex, latex)
        for match in variable_matches:
            original_name = match.groups()[0]
            new_name = re.sub(unwrapped_single_char_sub_sup_regex, '\\1{\\2}', original_name)
            variable_name_dict[new_name] = original_name
        self.variable_name_dict = variable_name_dict

        pre_processed_latex = re.sub(unwrapped_single_char_sub_sup_regex, '\\1{\\2}', latex)

        return pre_processed_latex

    def convert_relation(self, rel):
        if 'expr' in rel:
            return self.convert_expr(rel.get('expr'))

        relations = rel.get('relation')
        lh = self.convert_relation(relations[0])
        rh = self.convert_relation(relations[1])
        if has_type_or_token(rel, LATEXLexerToken.LT):
            return sympy.StrictLessThan(lh, rh, evaluate=False)
        elif has_type_or_token(rel, LATEXLexerToken.LTE):
            return sympy.LessThan(lh, rh, evaluate=False)
        elif has_type_or_token(rel, LATEXLexerToken.GT):
            return sympy.StrictGreaterThan(lh, rh, evaluate=False)
        elif has_type_or_token(rel, LATEXLexerToken.GTE):
            return sympy.GreaterThan(lh, rh, evaluate=False)
        elif has_type_or_token(rel, LATEXLexerToken.EQUAL):
            return sympy.Eq(lh, rh, evaluate=False)
        elif has_type_or_token(rel, LATEXLexerToken.UNEQUAL):
            return sympy.Ne(lh, rh, evaluate=False)
        else:  # pragma: no cover
            raise Exception('Unrecognized relation')

    def convert_expr(self, expr):
        if 'additive' in expr:
            return self.convert_add(expr.get('additive'))
        else:  # pragma: no cover
            raise Exception('Unrecognized expr')

    def convert_matrix(self, matrix):
        # build matrix
        row = matrix.get('matrix_row')
        tmp = []
        rows = 0
        for r in row:
            tmp.append([])
            if isinstance(r.get('expr'), list):
                for expr in r.get('expr'):
                    tmp[rows].append(self.convert_expr(expr))
            else:
                tmp[rows].append(self.convert_expr(r.get('expr')))
            rows = rows + 1

        # return the matrix
        return sympy.Matrix(tmp)

    def convert_add(self, add):
        if 'mp' in add:
            return self.convert_mp(add.get('mp'))

        type = add.get('type')

        if type == LATEXLexerToken.ADD:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return mat_add_flat(lh, rh)
            else:
                return add_flat(lh, rh)
        elif type == LATEXLexerToken.SUB:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return mat_add_flat(lh, mat_mul_flat(-1, rh))
            else:
                rh = mul_flat(-1, rh)
                return add_flat(lh, rh)
        else:  # pragma: no cover
            raise Exception('Unrecognized add')

    def convert_mp(self, mp):
        if 'unary' in mp:
            return self.convert_unary(mp.get('unary'))
        if 'unary_nofunc' in mp:
            return self.convert_unary(mp.get('unary_nofunc'))

        if 'mp' in mp:
            mp_left = mp.get('mp')[0]
            mp_right = mp.get('mp')[1]
        else:
            mp_left = mp.get('mp_nofunc')[0]
            mp_right = mp.get('mp_nofunc')[1]

        type = mp.get('type')

        if type == LATEXLexerToken.MUL or type == LATEXLexerToken.CMD_TIMES or type == LATEXLexerToken.CMD_CDOT:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)

            if lh.is_Matrix or rh.is_Matrix:
                return mat_mul_flat(lh, rh)
            else:
                return mul_flat(lh, rh)
        elif type == LATEXLexerToken.DIV or type == LATEXLexerToken.CMD_DIV or type == LATEXLexerToken.COLON:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if lh.is_Matrix or rh.is_Matrix:
                return sympy.MatMul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
            else:
                return sympy.Mul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
        elif type == LATEXLexerToken.CMD_MOD:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if rh.is_Matrix:
                raise Exception('Cannot perform modulo operation with a matrix as an operand')
            else:
                return sympy.Mod(lh, rh, evaluate=False)
        else:  # pragma: no cover
            raise Exception('Unrecognized mp')

    def convert_unary(self, unary):
        if 'postfix_nofunc' in unary:
            first = unary.get('postfix')
            tail = unary.get('postfix_nofunc')
            postfix = first + tail
            return self.convert_postfix_list(postfix)
        elif 'postfix' in unary:
            postfix = unary.get('postfix')
            return self.convert_postfix_list(postfix)

        type = unary.get('type')

        if 'unary' in unary:
            nested_unary = unary.get('unary')
        else:
            nested_unary = unary.get('unary_nofunc')

        if type == LATEXLexerToken.ADD:
            return self.convert_unary(nested_unary)
        elif type == LATEXLexerToken.SUB:
            tmp_convert_nested_unary = self.convert_unary(nested_unary)
            if tmp_convert_nested_unary.is_Matrix:
                return mat_mul_flat(-1, tmp_convert_nested_unary)
            else:
                if tmp_convert_nested_unary.func.is_Number:
                    return -tmp_convert_nested_unary
                else:
                    return mul_flat(-1, tmp_convert_nested_unary)
        else:  # pragma: no cover
            raise Exception('Unrecognized unary')

    def convert_postfix_list(self, arr, i=0):
        if i >= len(arr):  # pragma: no cover
            raise Exception('Index out of bounds')

        list_item = arr[i]
        res = self.convert_postfix(list_item)

        if isinstance(res, sympy.Expr) or isinstance(res, sympy.Matrix) or res is EmptySet:
            if i == len(arr) - 1:
                return res  # nothing to multiply by
            else:
                # multiply by next
                rh = self.convert_postfix_list(arr, i + 1)

                if res.is_Matrix or rh.is_Matrix:
                    return mat_mul_flat(res, rh)
                else:
                    return mul_flat(res, rh)
        else:  # must be derivative
            wrt = res[0]
            if i == len(arr) - 1:
                raise Exception('Expected expression for derivative')
            else:
                expr = self.convert_postfix_list(arr, i + 1)
                return sympy.Derivative(expr, wrt)

    def do_eval_at_subs(self, expr, at):
        if 'expr' in at:
            at_expr = self.convert_expr(at.get('expr'))
            syms = at_expr.atoms(sympy.Symbol)
            if len(syms) == 0:
                return expr
            elif len(syms) > 0:
                sym = next(iter(syms))
                return expr.subs(sym, at_expr)
            else:  # pragma: no cover
                raise Exception('Unrecognized eval_at expr')
        elif 'equality' in at:
            lh = self.convert_expr(at.get('equality').get('expr')[0])
            rh = self.convert_expr(at.get('equality').get('expr')[1])
            return expr.subs(lh, rh)
        else:  # pragma: no cover
            raise Exception('Unrecognized eval_at')

    def convert_postfix(self, postfix):
        if 'exp' in postfix:
            exp_nested = postfix.get('exp')
        else:
            exp_nested = postfix.get('exp_nofunc')

        exp = self.convert_exp(exp_nested)
        if 'postfix_op' in postfix:
            for op in postfix.get('postfix_op'):
                if has_type_or_token(op, LATEXLexerToken.BANG):
                    if isinstance(exp, list):
                        raise Exception('Cannot apply postfix to derivative')
                    exp = sympy.factorial(exp, evaluate=False)
                elif 'eval_at' in op:
                    ev = op.get('eval_at')
                    at_b = None
                    at_a = None
                    if 'eval_at_sup' in ev:
                        at_b = self.do_eval_at_subs(exp, ev.get('eval_at_sup'))
                    if 'eval_at_sub' in ev:
                        at_a = self.do_eval_at_subs(exp, ev.get('eval_at_sub'))
                    if at_b is not None and at_a is not None:
                        exp = add_flat(at_b, mul_flat(at_a, -1))
                    elif at_b is not None:
                        exp = at_b
                    elif at_a is not None:
                        exp = at_a
                    else:  # pragma: no cover
                        raise Exception('Unrecognized eval_at')
                else:  # pragma: no cover
                    raise Exception('Unrecognized postfix_op')

        return exp

    def convert_exp(self, exp):
        if 'comp' in exp:
            return self.convert_comp(exp.get('comp'))
        if 'comp_nofunc' in exp:
            return self.convert_comp(exp.get('comp_nofunc'))

        if 'exp' in exp:
            exp_nested = exp.get('exp')
        elif 'exp_nofunc' in exp:
            exp_nested = exp.get('exp_nofunc')
        else:  # pragma: no cover
            raise Exception('Unrecognized exp')

        base = self.convert_exp(exp_nested)
        if isinstance(base, list):
            raise Exception('Cannot raise derivative to power')
        if 'atom' in exp:
            exponent = self.convert_atom(exp.get('atom'))
        elif 'expr' in exp:
            exponent = self.convert_expr(exp.get('expr'))
        else:  # pragma: no cover
            raise Exception('Unrecognized exp')
        return sympy.Pow(base, exponent, evaluate=False)

    def convert_comp(self, comp):
        if 'group' in comp:
            return self.convert_expr(comp.get('group').get('expr'))
        elif 'abs_group' in comp:
            return sympy.Abs(self.convert_expr(comp.get('abs_group').get('expr')), evaluate=False)
        elif 'floor_group' in comp:
            return create_floor(self.convert_expr(comp.get('floor_group').get('expr')))
        elif 'ceil_group' in comp:
            return create_ceil(self.convert_expr(comp.get('ceil_group').get('expr')))
        elif 'atom' in comp:
            return self.convert_atom(comp.get('atom'))
        elif 'frac' in comp:
            return self.convert_frac(comp.get('frac'))
        elif 'binom' in comp:
            return self.convert_binom(comp.get('binom'))
        elif 'matrix' in comp:
            return self.convert_matrix(comp.get('matrix'))
        elif 'func' in comp:
            return self.convert_func(comp.get('func'))
        else:  # pragma: no cover
            raise Exception('Unrecognized comp')

    def convert_atom(self, atom):
        if 'atom_expr' in atom:
            atom_expr = atom.get('atom_expr')
            type = atom_expr.get('type')

            # find the atom's text
            atom_text = ''
            if type == LATEXLexerToken.LETTER:
                atom_text = atom_expr.get('text')
            elif type == LATEXLexerToken.GREEK_CMD:
                atom_text = atom_expr.get('text')[1:].strip()
            elif 'accent' in atom_expr:
                atom_accent = atom_expr.get('accent')
                # get name for accent
                name = atom_accent.get('accent_symbol').get('text')[1:]
                # exception: check if bar or overline which are treated both as bar
                if name in ['bar', 'overline']:
                    name = 'bar'
                else:  # pragma: no cover
                    raise Exception('Unrecognized accent')
                # get the base (variable)
                letter = get_token(atom_accent, LATEXLexerToken.LETTER)
                greek_cmd = get_token(atom_accent, LATEXLexerToken.GREEK_CMD)
                base = letter if letter is not None else greek_cmd
                # set string to base+name
                atom_text = base.get('text') + name
            else:  # pragma: no cover
                raise Exception('Unrecognized atom_expr')

            # find atom's subscript, if any
            subscript_text = ''
            if 'subexpr' in atom_expr:
                subexpr = atom_expr.get('subexpr')
                subscript = None
                if 'atom' in subexpr:  # subscript is atom
                    subscript = subexpr.get('atom').get('text').strip()
                elif 'expr' in subexpr:  # subscript is expr
                    subscript = subexpr.get('expr').get('text').strip()
                elif 'args' in subexpr:  # subscript is args
                    subscript = subexpr.get('args').get('text').strip()
                else:  # pragma: no cover
                    raise Exception('Unrecognized subexpr')
                if len(subscript) > 1:
                    subscript_text = '_{' + subscript + '}'
                else:
                    subscript_text = '_' + subscript

            # construct the symbol using the text and optional subscript
            atom_name = atom_text + subscript_text
            atom_symbol = self.get_atom_symbol_for_atom_expr(atom_name, type)

            # find the atom's superscript, and return as a Pow if found
            if 'supexpr' in atom_expr:
                supexpr = atom_expr.get('supexpr')
                func_pow = None
                if 'atom' in supexpr:
                    func_pow = self.convert_atom(supexpr.get('atom'))
                elif 'expr' in supexpr:
                    func_pow = self.convert_expr(supexpr.get('expr'))
                else:  # pragma: no cover
                    raise Exception('Invalid supexpr')
                return sympy.Pow(atom_symbol, func_pow, evaluate=False)

            return atom_symbol
        elif 'differential_atom_expr' in atom:
            # prefix the nested symbol so that it is handled correctly in `convert_func_integral`
            atom_expr = atom.get('differential_atom_expr').get('atom_expr')
            result = self.convert_atom({'atom_expr': atom_expr})
            atom_symbol = result.args[0] if isinstance(result, sympy.Pow) else result
            diff_atom_symbol = sympy.Symbol(DIFFERENTIAL_PREFIX + atom_symbol.name, real=True, positive=True)
            return (
                sympy.Pow(diff_atom_symbol, result.args[1], evaluate=False)
                if isinstance(result, sympy.Pow)
                else diff_atom_symbol
            )
        elif has_type_or_token(atom, LATEXLexerToken.SYMBOL):
            # remove dollar sign, percentage symbol, and whitespace
            s = atom.get('text').replace('\\$', '').replace('\\%', '').strip()
            if s == '\\infty':
                return sympy.oo
            elif s == '\\pi':
                return sympy.pi
            elif s == '\\emptyset':
                return EmptySet
            elif s == '\\imaginaryI' or s == '\\imaginaryJ':
                return sympy.I
            else:  # pragma: no cover
                raise Exception('Unrecognized symbol')
        elif has_type_or_token(atom, LATEXLexerToken.NUMBER):
            s = atom.get('text').replace(',', '')
            return create_rational_or_number(s)
        elif has_type_or_token(atom, LATEXLexerToken.SCI_NOTATION_NUMBER):
            s = atom.get('text')
            s_parts = s.split('\\times 10^')
            s1 = s_parts[0].replace(',', '')
            n1 = create_rational_or_number(s1)
            s2 = s_parts[1].replace('{', '').replace(',', '').replace('}', '')
            n2 = create_rational_or_number(s2)
            n_exp = sympy.Mul(n1, sympy.Pow(10, n2))
            return create_rational_or_number(n_exp)
        elif has_type_or_token(atom, LATEXLexerToken.FRACTION_NUMBER):
            s = atom.get('text').replace('\\frac{', '').replace('}{', '/').replace('}', '').replace(',', '')
            try:
                sr = sympy.Rational(s)
                return sr
            except ZeroDivisionError:
                # preserve the divide by zero as an expression
                s_parts = s.split('/')
                p = create_rational_or_number(s_parts[0])
                q = create_rational_or_number(s_parts[1])
                return sympy.Mul(p, sympy.Pow(q, -1, evaluate=False), evaluate=False)
            except (TypeError, ValueError):  # pragma: no cover
                return sympy.Number(s)
        elif has_type_or_token(atom, LATEXLexerToken.E_NOTATION):
            text = atom.get('text').replace(',', '')
            parts = text.split('E')

            # parse variables if either part is a variable
            if '\\variable' in parts[0] or '\\variable' in parts[1]:
                v1 = (
                    process_sympy(parts[0], variable_values=self.variable_values)
                    if '\\variable' in parts[0]
                    else create_rational_or_number(parts[0])
                )
                v2 = (
                    process_sympy(parts[1], variable_values=self.variable_values)
                    if '\\variable' in parts[1]
                    else create_rational_or_number(parts[1])
                )
                return sympy.Mul(v1, sympy.Pow(10, v2, evaluate=False), evaluate=False)

            return create_rational_or_number(text)
        elif 'mathit' in atom:
            text = atom.get('mathit').get('mathit_text').get('text')
            return sympy.Symbol(text, real=True, positive=True)
        elif has_type_or_token(atom, LATEXLexerToken.VARIABLE):
            text = atom.get('text')
            is_percent = text.endswith('\\%')
            trim_amount = 3 if is_percent else 1
            name = text[10:]
            name = name[0 : len(name) - trim_amount]

            # revert to the 'original' variable name stored from `pre_process_latex`
            # original name might be the same if it already had a wrapped single char sub
            name = self.variable_name_dict[name]

            # add hash to distinguish from regular symbols
            hash = hashlib.md5(name.encode()).hexdigest()
            symbol_name = name + hash

            # replace the variable for already known variable values
            if name in self.variable_values:
                symbol = self.variable_values[name]
            else:
                symbol = sympy.Symbol(symbol_name, real=True)

            if is_percent:
                return sympy.Mul(symbol, sympy.Pow(100, -1, evaluate=False), evaluate=False)

            # return the symbol
            return symbol
        elif has_type_or_token(atom, LATEXLexerToken.PERCENT_NUMBER):
            text = atom.get('text').replace('\\%', '').replace(',', '')
            number = create_rational_or_number(text)
            percent = sympy.Rational(number, 100)
            return percent
        elif has_type_or_token(atom, LATEXLexerToken.COMPLEX_NUMBER_POLAR_ANGLE):
            angle_str = atom.get('text').replace('\\angle ', '')
            if '\\degree' in angle_str:
                angle_str = angle_str.replace('\\degree', '').strip()
                angle_degrees = process_sympy(angle_str, variable_values=self.variable_values)
                # convert angle from degrees to radians
                angle = sympy.Mul(angle_degrees, sympy.Pow(180, -1, evaluate=False), sympy.pi, evaluate=False)
            else:
                angle = process_sympy(angle_str, variable_values=self.variable_values)
            # represent the polar complex number in exponential form, so that angle is not duplicated
            # polar form: r * (cos(angle) + i * sin(angle))
            # exponential form: r * e^{i * angle}
            return sympy.exp(sympy.Mul(sympy.I, angle, evaluate=False), evaluate=False)
        else:  # pragma: no cover
            raise Exception('Unrecognized atom')

    def convert_frac(self, frac):
        frac_upper = frac.get('upper')
        frac_lower = frac.get('lower')

        expr_lower = self.convert_expr(frac_lower)

        if frac_upper.get('start').get('type') == LATEXLexerToken.DIFFERENTIAL_D and is_differential_var(expr_lower):
            wrt = get_differential_var(expr_lower)
            # fraction upper only contains `\differentialD`, don't call `convert_expr`
            if frac_upper.get('start') == frac_upper.get('stop'):
                return [wrt]
            expr_upper = self.convert_expr(frac_upper)
            if is_differential_var(expr_upper):
                diff_var = get_differential_var(expr_upper)
            else:  # pragma: no cover
                raise Exception('Unrecognized differential')
            return sympy.Derivative(diff_var, wrt)

        expr_upper = self.convert_expr(frac_upper)
        if expr_upper.is_Matrix or expr_lower.is_Matrix:
            return sympy.MatMul(expr_upper, sympy.Pow(expr_lower, -1, evaluate=False), evaluate=False)
        else:
            return sympy.Mul(expr_upper, sympy.Pow(expr_lower, -1, evaluate=False), evaluate=False)

    def convert_binom(self, binom):
        expr_top = self.convert_expr(binom.get('expr')[0])
        expr_bot = self.convert_expr(binom.get('expr')[1])
        return sympy.binomial(expr_top, expr_bot)

    def convert_func(self, func):
        if 'func_single_arg' in func or 'func_multi_arg' in func:
            func_single_arg = func.get('func_single_arg')
            func_multi_arg = func.get('func_multi_arg')
            sub_func = func_single_arg if func_single_arg is not None else func_multi_arg

            # get name
            if 'func_cmd_single_arg' in sub_func:
                name = sub_func.get('func_cmd_single_arg').get('text')[1:]
            elif 'func_cmd_multi_arg' in sub_func:
                name = sub_func.get('func_cmd_multi_arg').get('text')[1:]
            else:
                name = sub_func.get('tokens')[0].get('text')[1:]

            # handle operatorname cmds
            if name == 'operatorname':
                operator_name_key = 'func_name_single_arg' if func_single_arg is not None else 'func_name_multi_arg'
                name = sub_func.get(operator_name_key).get('text')

            # get single arg or multiple args
            if 'func_arg_noparens' in func:
                # handle a single arg with no parentheses
                arg = self.convert_func_arg(func.get('func_arg_noparens'))
            elif 'func_arg' in func:
                arg = self.convert_func_arg(func.get('func_arg'))
            else:  # 'func_args'
                # commas are **always** used to split args for multi-arg functions
                args = func.get('func_args').get('text').split(',')
                args = list(map(lambda arg: process_sympy(arg, self.variable_values), args))

            # single arg functions
            # change arc<trig> -> a<trig>
            if name in ['arcsin', 'arccos', 'arctan', 'arccsc', 'arcsec', 'arccot', 'arcsinh', 'arccosh', 'arctanh']:
                name = 'a' + name[3:]
                expr = getattr(sympy.functions, name)(arg, evaluate=False)
            # change ar<trig> -> a<trig>
            elif name in ['arsinh', 'arcosh', 'artanh']:
                name = 'a' + name[2:]
                expr = getattr(sympy.functions, name)(arg, evaluate=False)
            elif name in ['log', 'ln']:
                if 'subexpr' in func:
                    subexpr = func.get('subexpr')
                    if 'atom' in subexpr:
                        base = self.convert_atom(subexpr.get('atom'))
                    elif 'expr' in subexpr:
                        base = self.convert_expr(subexpr.get('expr'))
                    else:  # pragma: no cover
                        raise Exception('Invalid log/ln subexpr')
                elif name == 'log':
                    base = 10
                elif name == 'ln':
                    base = sympy.E
                else:  # pragma: no cover
                    raise Exception('Unrecognized log/ln')
                expr = sympy.log(arg, base, evaluate=False)
            elif name == 'exp':
                expr = sympy.exp(arg, evaluate=False)
            elif name == 'floor':
                expr = create_floor(arg)
            elif name == 'ceil':
                expr = create_ceil(arg)
            # complex functions
            elif name == 'Re':
                expr = sympy.re(arg, evaluate=False)
            elif name == 'Im':
                expr = sympy.im(arg, evaluate=False)
            elif name == 'Abs':
                expr = sympy.Abs(arg, evaluate=False)
            elif name == 'Arg':
                expr = sympy.arg(arg, evaluate=False)
            elif name == 'conj':
                expr = sympy.conjugate(arg, evaluate=False)

            # multi-arg functions
            if name in ['gcd', 'lcm']:
                expr = create_gcd_lcm(name, args)
            elif name in ['max', 'min']:
                name = name[0].upper() + name[1:]
                expr = getattr(sympy.functions, name)(*args, evaluate=False)

            # handle exponents on the func
            func_pow = None
            should_pow = True
            if 'supexpr' in func:
                supexpr = func.get('supexpr')
                if 'atom' in supexpr:
                    func_pow = self.convert_atom(supexpr.get('atom'))
                elif 'expr' in supexpr:
                    func_pow = self.convert_expr(supexpr.get('expr'))
                else:  # pragma: no cover
                    raise Exception('Invalid supexpr')

            # handle <trig> methods after parsing `supexpr`
            if name in ['sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'sinh', 'cosh', 'tanh']:
                # change <trig> -> a<trig> if exponent is -1
                if func_pow == -1:
                    name = 'a' + name
                    should_pow = False
                expr = getattr(sympy.functions, name)(arg, evaluate=False)

            # apply exponent `supexpr`
            if func_pow and should_pow:
                expr = sympy.Pow(expr, func_pow, evaluate=False)

            return expr

        elif has_type_or_token(func, LATEXLexerToken.FUNC_INT):
            return self.convert_func_integral(func)
        elif has_type_or_token(func, LATEXLexerToken.FUNC_SQRT):
            exprs = func.get('expr')
            expr = self.convert_expr(exprs[1]) if isinstance(exprs, list) else self.convert_expr(exprs)
            if isinstance(exprs, list):
                r = self.convert_expr(exprs[0])
                return sympy.Pow(expr, 1 / r, evaluate=False)
            else:
                return sympy.Pow(expr, sympy.S.Half, evaluate=False)
        elif has_type_or_token(func, LATEXLexerToken.FUNC_SUM):
            return self.convert_func_sum_or_prod(func, 'summation')
        elif has_type_or_token(func, LATEXLexerToken.FUNC_PROD):
            return self.convert_func_sum_or_prod(func, 'product')
        elif has_type_or_token(func, LATEXLexerToken.FUNC_LIM):
            return self.convert_func_limit(func)
        elif has_type_or_token(func, LATEXLexerToken.EXP_E):
            return self.convert_func_exp_e(func)
        else:  # pragma: no cover
            raise Exception('Unrecognized func')

    def convert_func_arg(self, arg):
        if 'expr' in arg:
            return self.convert_expr(arg.get('expr'))
        else:
            return self.convert_mp(arg.get('mp_nofunc'))

    def convert_func_integral(self, func):
        if 'additive' in func:
            integrand = self.convert_add(func.get('additive'))
        elif 'frac' in func:
            integrand = self.convert_frac(func.get('frac'))
        else:
            integrand = 1

        int_var = None
        if 'differential_atom_expr' in func:
            atom_expr = func.get('differential_atom_expr').get('atom_expr')
            int_var = self.convert_atom({'atom_expr': atom_expr})
        else:
            for sym in integrand.atoms(sympy.Symbol):
                if is_differential_var(sym):
                    int_var = get_differential_var(sym)
                    int_sym = sym
            if int_var:
                integrand = integrand.subs(int_sym, 1)
            else:
                # Assume dx by default
                int_var = sympy.Symbol('x', real=True, positive=True)

        if 'subexpr' in func:
            subexpr = func.get('subexpr')
            supexpr = func.get('supexpr')

            if 'atom' in subexpr:
                lower = self.convert_atom(subexpr.get('atom'))
            elif 'expr' in subexpr:
                lower = self.convert_expr(subexpr.get('expr'))
            else:  # pragma: no cover
                raise Exception('Invalid subexpr')
            if 'atom' in func.get('supexpr'):
                upper = self.convert_atom(supexpr.get('atom'))
            elif 'expr' in supexpr:
                upper = self.convert_expr(supexpr.get('expr'))
            else:  # pragma: no cover
                raise Exception('Invalid supexpr')
            return sympy.Integral(integrand, (int_var, lower, upper))
        else:
            return sympy.Integral(integrand, int_var)

    def convert_func_sum_or_prod(self, func, name):
        val = self.convert_mp(func.get('mp'))
        iter_var = self.convert_expr(func.get('subeq').get('equality').get('expr')[0])
        start = self.convert_expr(func.get('subeq').get('equality').get('expr')[1])

        supexpr = func.get('supexpr')
        if 'atom' in func.get('supexpr'):  # ^atom
            end = self.convert_atom(supexpr.get('atom'))
        elif 'expr' in supexpr:  # ^{expr}
            end = self.convert_expr(supexpr.get('expr'))
        else:  # pragma: no cover
            raise Exception('Invalid supexpr')

        if name == 'summation':
            return sympy.Sum(val, (iter_var, start, end))
        elif name == 'product':
            return sympy.Product(val, (iter_var, start, end))
        else:  # pragma: no cover
            raise Exception('Unrecognized sum/prod')

    def convert_func_limit(self, func):
        sub = func.get('limit_sub')
        letter = get_token(sub, LATEXLexerToken.LETTER)
        greek_cmd = get_token(sub, LATEXLexerToken.GREEK_CMD)
        if letter is not None:
            var = sympy.Symbol(letter.get('text'), real=True, positive=True)
        elif greek_cmd is not None:
            var = sympy.Symbol(greek_cmd.get('text')[1:].strip(), real=True, positive=True)
        else:  # pragma: no cover
            raise Exception('Unrecognized limit')
        if get_token(sub, LATEXLexerToken.SUB) is not None:
            direction = '-'
        else:
            direction = '+'
        approaching = self.convert_expr(sub.get('expr'))
        content = self.convert_mp(func.get('mp'))

        return sympy.Limit(content, var, approaching, direction)

    def convert_func_exp_e(self, func):
        if 'supexpr' in func:
            supexpr = func.get('supexpr')
            if 'atom' in func.get('supexpr'):  # ^atom
                exp_arg = self.convert_atom(supexpr.get('atom'))
            elif 'expr' in supexpr:  # ^{expr}
                exp_arg = self.convert_expr(supexpr.get('expr'))
            else:  # pragma: no cover
                raise Exception('Invalid supexpr')
            return sympy.exp(exp_arg, evaluate=False)
        else:
            return sympy.E

    def get_atom_symbol_for_atom_expr(self, atom_name, type):
        # subclassed in LatexToSympyAsUnit to handle unit parsing
        return sympy.Symbol(atom_name, real=True, positive=True)
