import hashlib
import json
import re
import sympy
import sympy.physics.units as sympy_physics_units
from sympy.physics.units.prefixes import PREFIXES, prefix_unit
from latex2sympy.lib import parseToJson, LATEXLexerToken


def process_sympy(latex: str, variable_values={}):
    instance = LatexToSympy(latex, variable_values)
    return instance.process_sympy()


class LatexToSympy:
    def __init__(self, latex: str, variable_values: dict = {}):
        self.latex = latex
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
        if self.has_type_or_token(rel, LATEXLexerToken.LT):
            return sympy.StrictLessThan(lh, rh, evaluate=False)
        elif self.has_type_or_token(rel, LATEXLexerToken.LTE):
            return sympy.LessThan(lh, rh, evaluate=False)
        elif self.has_type_or_token(rel, LATEXLexerToken.GT):
            return sympy.StrictGreaterThan(lh, rh, evaluate=False)
        elif self.has_type_or_token(rel, LATEXLexerToken.GTE):
            return sympy.GreaterThan(lh, rh, evaluate=False)
        elif self.has_type_or_token(rel, LATEXLexerToken.EQUAL):
            return sympy.Eq(lh, rh, evaluate=False)
        elif self.has_type_or_token(rel, LATEXLexerToken.UNEQUAL):
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

    def add_flat(self, lh, rh):
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

    def mat_add_flat(self, lh, rh):
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

    def mul_flat(self, lh, rh):
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

    def mat_mul_flat(self, lh, rh):
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

    def convert_add(self, add):
        if 'mp' in add:
            return self.convert_mp(add.get('mp'))

        type = add.get('type')

        if type == LATEXLexerToken.ADD:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, rh)
            else:
                return self.add_flat(lh, rh)
        elif type == LATEXLexerToken.SUB:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, self.mat_mul_flat(-1, rh))
            else:
                rh = self.mul_flat(-1, rh)
                return self.add_flat(lh, rh)
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
                return self.mat_mul_flat(lh, rh)
            else:
                return self.mul_flat(lh, rh)
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
                return self.mat_mul_flat(-1, tmp_convert_nested_unary)
            else:
                if tmp_convert_nested_unary.func.is_Number:
                    return -tmp_convert_nested_unary
                else:
                    return self.mul_flat(-1, tmp_convert_nested_unary)
        else:  # pragma: no cover
            raise Exception('Unrecognized unary')

    def convert_postfix_list(self, arr, i=0):
        if i >= len(arr):  # pragma: no cover
            raise Exception('Index out of bounds')

        res = self.convert_postfix(arr[i])

        if isinstance(res, sympy.Expr) or isinstance(res, sympy.Matrix) or res is sympy.S.EmptySet:
            if i == len(arr) - 1:
                return res  # nothing to multiply by
            else:
                # multiply by next
                rh = self.convert_postfix_list(arr, i + 1)

                if res.is_Matrix or rh.is_Matrix:
                    return self.mat_mul_flat(res, rh)
                else:
                    return self.mul_flat(res, rh)
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
                if self.has_type_or_token(op, LATEXLexerToken.BANG):
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
                        exp = self.add_flat(at_b, self.mul_flat(at_a, -1))
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
            return self.handle_floor(self.convert_expr(comp.get('floor_group').get('expr')))
        elif 'ceil_group' in comp:
            return self.handle_ceil(self.convert_expr(comp.get('ceil_group').get('expr')))
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
                base = atom_accent.get('expr').get('text')
                # set string to base+name
                atom_text = base + name
            else:  # pragma: no cover
                raise Exception('Unrecognized atom_expr')

            if 'subexpr' not in atom_expr and 'supexpr' not in atom_expr:
                # check if the text is a unit, and return if matches
                unit = self.convert_unit(atom_text)
                if unit is not None:
                    return unit

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
            atom_symbol = sympy.Symbol(atom_text + subscript_text, real=True, positive=True)

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
        elif self.has_type_or_token(atom, LATEXLexerToken.SYMBOL):
            # remove dollar sign, percentage symbol, and whitespace
            s = atom.get('text').replace('\\$', '').replace('\\%', '').strip()
            if s == '\\infty':
                return sympy.oo
            elif s == '\\pi':
                return sympy.pi
            elif s == '\\emptyset':
                return sympy.S.EmptySet
            elif s == '\\imaginaryI' or s == '\\imaginaryJ':
                return sympy.I
            else:  # pragma: no cover
                raise Exception('Unrecognized symbol')
        elif self.has_type_or_token(atom, LATEXLexerToken.NUMBER):
            s = atom.get('text').replace(',', '')
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):  # pragma: no cover
                return sympy.Number(s)
        elif self.has_type_or_token(atom, LATEXLexerToken.SCI_NOTATION_NUMBER):
            s = atom.get('text')
            s_parts = s.split('\\times 10^')
            s1 = s_parts[0].replace(',', '')
            try:
                n1 = sympy.Rational(s1)
            except (TypeError, ValueError):  # pragma: no cover
                n1 = sympy.Number(s1)
            s2 = s_parts[1].replace('{', '').replace(',', '').replace('}', '')
            try:
                n2 = sympy.Rational(s2)
            except (TypeError, ValueError):  # pragma: no cover
                n2 = sympy.Number(s2)
            n_exp = sympy.Mul(n1, sympy.Pow(10, n2))
            try:
                n = sympy.Rational(n_exp)
            except (TypeError, ValueError):  # pragma: no cover
                n = sympy.Number(n_exp)
            return n
        elif self.has_type_or_token(atom, LATEXLexerToken.FRACTION_NUMBER):
            s = atom.get('text').replace('\\frac{', '').replace('}{', '/').replace('}', '').replace(',', '')
            try:
                sr = sympy.Rational(s)
                return sr
            except ZeroDivisionError:
                # preserve the divide by zero as an expression
                s_parts = s.split('/')
                try:
                    p = sympy.Rational(s_parts[0])
                except (TypeError, ValueError):  # pragma: no cover
                    p = sympy.Number(s_parts[0])
                try:
                    q = sympy.Rational(s_parts[1])
                except (TypeError, ValueError):  # pragma: no cover
                    q = sympy.Number(s_parts[1])
                return sympy.Mul(p, sympy.Pow(q, -1, evaluate=False), evaluate=False)
            except (TypeError, ValueError):  # pragma: no cover
                return sympy.Number(s)
        elif self.has_type_or_token(atom, LATEXLexerToken.E_NOTATION):
            s = atom.get('text').replace(',', '')
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):  # pragma: no cover
                return sympy.Number(s)
        elif self.has_type_or_token(atom, LATEXLexerToken.DIFFERENTIAL):
            var = self.get_differential_var(atom.get('text'))
            return sympy.Symbol('d' + var.name, real=True, positive=True)
        elif 'mathit' in atom:
            text = atom.get('mathit').get('mathit_text').get('text')
            return sympy.Symbol(text, real=True, positive=True)
        elif self.has_type_or_token(atom, LATEXLexerToken.VARIABLE):
            text = atom.get('text')
            is_percent = text.endswith('\\%')
            trim_amount = 3 if is_percent else 1
            name = text[10:]
            name = name[0:len(name) - trim_amount]

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
        elif self.has_type_or_token(atom, LATEXLexerToken.PERCENT_NUMBER):
            text = atom.get('text').replace('\\%', '').replace(',', '')
            try:
                number = sympy.Rational(text)
            except (TypeError, ValueError):  # pragma: no cover
                number = sympy.Number(text)
            percent = sympy.Rational(number, 100)
            return percent
        elif self.has_type_or_token(atom, LATEXLexerToken.COMPLEX_NUMBER_POLAR_ANGLE):
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
        elif self.has_type_or_token(atom, LATEXLexerToken.LETTERS):
            atom_text = atom.get('text')
            unit = self.convert_unit(atom_text)
            if unit is not None:
                return unit
            else:
                # TODO: make each letter a separate symbol?
                args = [self.convert_atom({'atom_expr': {'text': t, 'type': LATEXLexerToken.LETTER}}) for t in list(atom_text)]
                return sympy.Mul(*args, evaluate=False)
        else:  # pragma: no cover
            raise Exception('Unrecognized atom')

    def convert_unit(self, text):
        # TODO: ignore speed_of_light, figure out better way to define constants vs. units vs. symbols
        if text == 'c':
            return None
        # check if a unit matches the given text
        try:
            unit_matches = sympy_physics_units.find_unit(text)
        except AttributeError as e:
            # no matches will throw an AttributeError
            # check if the first letter of the text is a prefix
            prefix_text = text[:1]
            if prefix_text not in PREFIXES:
                return None
            prefix = PREFIXES[prefix_text]
            # check if the remaining text after the prefix is a valid unit
            unit = self.convert_unit(text[1:])
            if unit is None:
                return None
            # combine the prefix and unit into a new `Quantity`
            # prefix_unit accepts a dict of prefixes, so construct one
            prefixes = {}
            prefixes[prefix_text] = prefix
            prefixed_units = prefix_unit(unit, prefixes)
            return prefixed_units[0]
        # if matches are found, return the first matching unit
        if len(unit_matches) > 0:
            unit_key = unit_matches[0]
            unit = getattr(sympy_physics_units, unit_key)
            return unit
        return None

    def convert_frac(self, frac):
        frac_upper = frac.get('upper')
        frac_lower = frac.get('lower')

        if (frac_lower.get('start') == frac_lower.get('stop') and frac_lower.get('start').get('type') == LATEXLexerToken.DIFFERENTIAL):
            wrt_text = self.get_differential_var_str(frac_lower.get('start').get('text'))
            wrt = sympy.Symbol(wrt_text, real=True, positive=True)
            if (frac_upper.get('start') == frac_upper.get('stop') and
                    frac_upper.get('start').get('type') == LATEXLexerToken.DIFFERENTIAL_D):
                return [wrt]

            upper_text = frac_upper.get('text')
            expr_top = process_sympy(upper_text[15:])
            return sympy.Derivative(expr_top, wrt)

        expr_top = self.convert_expr(frac.get('upper'))
        expr_bot = self.convert_expr(frac.get('lower'))
        if expr_top.is_Matrix or expr_bot.is_Matrix:
            return sympy.MatMul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)
        else:
            return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

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
                expr = self.handle_floor(arg)
            elif name == 'ceil':
                expr = self.handle_ceil(arg)
            # complex functions
            elif name == 'Re':
                expr = sympy.re(arg, evaluate=False)
            elif name == 'Im':
                expr = sympy.im(arg, evaluate=False)
            elif name == 'Abs':
                expr = sympy.Abs(arg, evaluate=False)
            elif name == 'Arg':
                expr = sympy.arg(arg, evaluate=False)

            # multi-arg functions
            if name in ['gcd', 'lcm']:
                expr = self.handle_gcd_lcm(name, args)
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

        elif self.has_type_or_token(func, LATEXLexerToken.FUNC_INT):
            return self.handle_integral(func)
        elif self.has_type_or_token(func, LATEXLexerToken.FUNC_SQRT):
            exprs = func.get('expr')
            expr = self.convert_expr(exprs[1]) if isinstance(exprs, list) else self.convert_expr(exprs)
            if isinstance(exprs, list):
                r = self.convert_expr(exprs[0])
                return sympy.Pow(expr, 1 / r, evaluate=False)
            else:
                return sympy.Pow(expr, sympy.S.Half, evaluate=False)
        elif self.has_type_or_token(func, LATEXLexerToken.FUNC_SUM):
            return self.handle_sum_or_prod(func, 'summation')
        elif self.has_type_or_token(func, LATEXLexerToken.FUNC_PROD):
            return self.handle_sum_or_prod(func, 'product')
        elif self.has_type_or_token(func, LATEXLexerToken.FUNC_LIM):
            return self.handle_limit(func)
        elif self.has_type_or_token(func, LATEXLexerToken.EXP_E):
            return self.handle_exp(func)
        else:  # pragma: no cover
            raise Exception('Unrecognized func')

    def convert_func_arg(self, arg):
        if 'expr' in arg:
            return self.convert_expr(arg.get('expr'))
        else:
            return self.convert_mp(arg.get('mp_nofunc'))

    def handle_integral(self, func):
        if 'additive' in func:
            integrand = self.convert_add(func.get('additive'))
        elif 'frac' in func:
            integrand = self.convert_frac(func.get('frac'))
        else:
            integrand = 1

        int_var = None
        differential = self.get_token(func, LATEXLexerToken.DIFFERENTIAL)
        if differential is not None:
            int_var = self.get_differential_var(differential.get('text'))
        else:
            for sym in integrand.atoms(sympy.Symbol):
                s = str(sym)
                if len(s) > 1 and s[0] == 'd':
                    if s[1] == '\\':  # pragma: no cover
                        int_var = sympy.Symbol(s[2:], real=True, positive=True)
                    else:
                        int_var = sympy.Symbol(s[1:], real=True, positive=True)
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

    def handle_sum_or_prod(self, func, name):
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

    def handle_limit(self, func):
        sub = func.get('limit_sub')
        letter = self.get_token(sub, LATEXLexerToken.LETTER)
        greek_cmd = self.get_token(sub, LATEXLexerToken.GREEK_CMD)
        if letter is not None:
            var = sympy.Symbol(letter.get('text'), real=True, positive=True)
        elif greek_cmd is not None:
            var = sympy.Symbol(greek_cmd.get('text')[1:].strip(), real=True, positive=True)
        else:  # pragma: no cover
            raise Exception('Unrecognized limit')
        if self.get_token(sub, LATEXLexerToken.SUB) is not None:
            direction = '-'
        else:
            direction = '+'
        approaching = self.convert_expr(sub.get('expr'))
        content = self.convert_mp(func.get('mp'))

        return sympy.Limit(content, var, approaching, direction)

    def handle_exp(self, func):
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

    def handle_gcd_lcm(self, f, args):
        '''
        Return the result of gcd() or lcm(), as UnevaluatedExpr

        f: str - name of function ('gcd' or 'lcm')
        args: List[Expr] - list of function arguments
        '''

        args = tuple(map(sympy.nsimplify, args))

        # gcd() and lcm() don't support evaluate=False
        return sympy.UnevaluatedExpr(getattr(sympy, f)(args))

    def handle_floor(self, expr):
        '''
        Apply floor() then return the floored expression.

        expr: Expr - sympy expression as an argument to floor()
        '''
        return sympy.functions.floor(expr, evaluate=False)

    def handle_ceil(self, expr):
        '''
        Apply ceil() then return the ceil-ed expression.

        expr: Expr - sympy expression as an argument to ceil()
        '''
        return sympy.functions.ceiling(expr, evaluate=False)

    def get_differential_var(self, d):
        text = self.get_differential_var_str(d)
        return sympy.Symbol(text, real=True, positive=True)

    def get_differential_var_str(self, text):
        for i in range(15, len(text)):  # pragma: no cover - loop break not recognized correctly
            c = text[i]
            if not (c == ' ' or c == '\r' or c == '\n' or c == '\t'):
                idx = i
                break
        text = text[idx:]
        if text[0] == '\\':
            text = text[1:].strip()
        return text

    def get_token(self, node, type):
        tokens = node.get('tokens') if 'tokens' in node else None
        token = next((t for t in node.get('tokens') if t.get('type') == type), None) if tokens is not None else None
        return token

    def has_type_or_token(self, node, type):
        if 'type' in node and node.get('type') == type:
            return True
        token = self.get_token(node, type)
        return token is not None
