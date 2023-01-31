import re
import sympy
import antlr4
from antlr4.error.ErrorListener import ErrorListener
from sympy.core.core import all_classes
from parser.cpp.build.lib.latex2antlrJson import parseToJson
import json

try:
    from parser.python.LATEXParser import LATEXParser
    from parser.python.LATEXLexer import LATEXLexer
except Exception:
    from .parser.python.LATEXParser import LATEXParser
    from .parser.python.LATEXLexer import LATEXLexer

from sympy.printing.str import StrPrinter

from sympy.parsing.sympy_parser import parse_expr

import hashlib


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

        print(json_string)

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

        find any single char sup/sub and wrap them in "{}"
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
        if 'type' in rel and rel.get('type') == LATEXParser.LT:
            return sympy.StrictLessThan(lh, rh, evaluate=False)
        elif 'type' in rel and rel.get('type') == LATEXParser.LTE:
            return sympy.LessThan(lh, rh, evaluate=False)
        elif 'type' in rel and rel.get('type') == LATEXParser.GT:
            return sympy.StrictGreaterThan(lh, rh, evaluate=False)
        elif 'type' in rel and rel.get('type') == LATEXParser.GTE:
            return sympy.GreaterThan(lh, rh, evaluate=False)
        elif 'type' in rel and rel.get('type') == LATEXParser.EQUAL:
            return sympy.Eq(lh, rh, evaluate=False)
        elif 'type' in rel and rel.get('type') == LATEXParser.UNEQUAL:
            return sympy.Ne(lh, rh, evaluate=False)

    def convert_expr(self, expr):
        if 'additive' in expr:
            return self.convert_add(expr.get('additive'))

    def convert_matrix(self, matrix):
        # build matrix
        row = matrix.get('matrix_row')
        tmp = []
        rows = 0
        for r in row:
            tmp.append([])
            for expr in r.get('expr'):
                tmp[rows].append(self.convert_expr(expr))
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

        if type == LATEXParser.ADD:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, rh)
            else:
                return self.add_flat(lh, rh)
        elif type == LATEXParser.SUB:
            lh = self.convert_add(add.get('additive')[0])
            rh = self.convert_add(add.get('additive')[1])

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, self.mat_mul_flat(-1, rh))
            else:
                rh = self.mul_flat(-1, rh)
                return self.add_flat(lh, rh)

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

        if type == LATEXParser.MUL or type == LATEXParser.CMD_TIMES or type == LATEXParser.CMD_CDOT:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_mul_flat(lh, rh)
            else:
                return self.mul_flat(lh, rh)
        elif type == LATEXParser.DIV or type == LATEXParser.CMD_DIV or type == LATEXParser.COLON:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if lh.is_Matrix or rh.is_Matrix:
                return sympy.MatMul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
            else:
                return sympy.Mul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
        elif type == LATEXParser.CMD_MOD:
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if rh.is_Matrix:
                raise Exception("Cannot perform modulo operation with a matrix as an operand")
            else:
                return sympy.Mod(lh, rh, evaluate=False)

    def convert_unary(self, unary):
        if 'postfix_nofunc' in unary:
            first = unary.get('postfix')
            tail = unary.get('postfix_nofunc')
            postfix = [first] + tail
            return self.convert_postfix_list(postfix)
        elif 'postfix' in unary:
            postfix = unary.get('postfix')
            return self.convert_postfix_list(postfix)

        type = unary.get('type')

        if 'unary' in unary:
            nested_unary = unary.get('unary')
        else:
            nested_unary = unary.get('unary_nofunc')

        if type == LATEXParser.ADD:
            return self.convert_unary(nested_unary)
        elif type == LATEXParser.SUB:
            tmp_convert_nested_unary = self.convert_unary(nested_unary)
            if tmp_convert_nested_unary.is_Matrix:
                return self.mat_mul_flat(-1, tmp_convert_nested_unary, evaluate=False)
            else:
                if tmp_convert_nested_unary.func.is_Number:
                    return -tmp_convert_nested_unary
                else:
                    return self.mul_flat(-1, tmp_convert_nested_unary)

    def convert_postfix_list(self, arr, i=0):
        if i >= len(arr):
            raise Exception("Index out of bounds")

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
                raise Exception("Expected expression for derivative")
            else:
                expr = self.convert_postfix_list(arr, i + 1)
                return sympy.Derivative(expr, wrt)

    def do_subs(self, expr, at):
        if 'expr' in at:
            at_expr = self.convert_expr(at.get('expr'))
            syms = at_expr.atoms(sympy.Symbol)
            if len(syms) == 0:
                return expr
            elif len(syms) > 0:
                sym = next(iter(syms))
                return expr.subs(sym, at_expr)
        elif 'equality' in at:
            lh = self.convert_expr(at.get('equality').get('expr')[0])
            rh = self.convert_expr(at.get('equality').get('expr')[1])
            return expr.subs(lh, rh)

    def convert_postfix(self, postfix):
        if 'exp' in postfix:
            exp_nested = postfix.get('exp')
        else:
            exp_nested = postfix.get('exp_nofunc')

        exp = self.convert_exp(exp_nested)
        if 'postfix_op' in postfix:
            for op in postfix.get('postfix_op'):
                if 'type' in op and op.get('type') == LATEXParser.BANG:
                    if isinstance(exp, list):
                        raise Exception("Cannot apply postfix to derivative")
                    exp = sympy.factorial(exp, evaluate=False)
                elif 'eval_at' in op:
                    ev = op.get('eval_at')
                    at_b = None
                    at_a = None
                    if 'eval_at_sup' in ev:
                        at_b = self.do_subs(exp, ev.get('eval_at_sup'))
                    if 'eval_at_sub' in ev:
                        at_a = self.do_subs(exp, ev.get('eval_at_sub'))
                    if at_b is not None and at_a is not None:
                        exp = self.add_flat(at_b, self.mul_flat(at_a, -1))
                    elif at_b is not None:
                        exp = at_b
                    elif at_a is not None:
                        exp = at_a

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

        if exp_nested:
            base = self.convert_exp(exp_nested)
            if isinstance(base, list):
                raise Exception("Cannot raise derivative to power")
            if 'atom' in exp:
                exponent = self.convert_atom(exp.get('atom'))
            elif 'expr' in exp:
                exponent = self.convert_expr(exp.get('expr'))
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

    def convert_atom(self, atom):
        if 'atom_expr' in atom:
            atom_expr = atom.get('atom_expr')
            type = atom_expr.get('type')

            # find the atom's text
            atom_text = ''
            if type == LATEXParser.LETTER_NO_E:
                atom_text = atom_expr.get('text')
                if atom_text == "I":
                    return sympy.I
            elif type == LATEXParser.GREEK_CMD:
                atom_text = atom_expr.get('text')[1:].strip()
            elif type == LATEXParser.accent:
                atom_accent = atom_expr.get('accent')
                # get name for accent
                name = atom_accent.start.text[1:]
                # exception: check if bar or overline which are treated both as bar
                if name in ["bar", "overline"]:
                    name = "bar"
                # get the base (variable)
                base = atom_accent.base.getText()
                # set string to base+name
                atom_text = base + name

            # find atom's subscript, if any
            subscript_text = ''
            if 'subexpr' in atom_expr:
                subexpr = atom_expr.get('subexpr')
                subscript = None
                if 'expr' in subexpr:  # subscript is expr
                    subscript = subexpr.get('expr').get('text').strip()
                elif 'atom' in subexpr:  # subscript is atom
                    subscript = subexpr.get('atom').get('text').strip()
                elif 'args' in subexpr:  # subscript is args
                    subscript = subexpr.get('args').get('text').strip()
                subscript_inner_text = StrPrinter().doprint(subscript)
                if len(subscript_inner_text) > 1:
                    subscript_text = '_{' + subscript_inner_text + '}'
                else:
                    subscript_text = '_' + subscript_inner_text

            # construct the symbol using the text and optional subscript
            atom_symbol = sympy.Symbol(atom_text + subscript_text, real=True, positive=True)

            # find the atom's superscript, and return as a Pow if found
            if 'supexpr' in atom_expr:
                supexpr = atom_expr.get('supexpr')
                func_pow = None
                if 'expr' in supexpr:
                    func_pow = self.convert_expr(supexpr.get('expr'))
                else:
                    func_pow = self.convert_atom(supexpr.get('atom'))
                return sympy.Pow(atom_symbol, func_pow, evaluate=False)

            return atom_symbol
        elif 'type' in atom and atom.get('type') == LATEXParser.SYMBOL:
            s = atom.get('text').replace("\\$", "").replace("\\%", "")
            if s == "\\infty":
                return sympy.oo
            elif s == '\\pi':
                return sympy.pi
            elif s == '\\emptyset':
                return sympy.S.EmptySet
            else:
                raise Exception("Unrecognized symbol")
        elif 'type' in atom and atom.get('type') == LATEXParser.NUMBER:
            s = atom.get('text').replace(",", "")
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):
                return sympy.Number(s)
        elif 'type' in atom and atom.get('type') == LATEXParser.SCI_NOTATION_NUMBER:
            s = atom.get('text')
            s_parts = s.split('\\times 10^')
            s1 = s_parts[0].replace(',', '')
            try:
                n1 = sympy.Rational(s1)
            except (TypeError, ValueError):
                n1 = sympy.Number(s1)
            s2 = s_parts[1].replace('{', '').replace(',', '').replace('}', '')
            try:
                n2 = sympy.Rational(s2)
            except (TypeError, ValueError):
                n2 = sympy.Number(s2)
            n_exp = sympy.Mul(n1, sympy.Pow(10, n2))
            try:
                n = sympy.Rational(n_exp)
            except (TypeError, ValueError):
                n = sympy.Number(n_exp)
            return n
        elif 'type' in atom and atom.get('type') == LATEXParser.FRACTION_NUMBER:
            s = atom.get('text').replace("\\frac{", "").replace("}{", "/").replace("}", "").replace(",", "")
            try:
                sr = sympy.Rational(s)
                return sr
            except ZeroDivisionError:
                # preserve the divide by zero as an expression
                s_parts = s.split('/')
                try:
                    p = sympy.Rational(s_parts[0])
                except (TypeError, ValueError):
                    p = sympy.Number(s_parts[0])
                try:
                    q = sympy.Rational(s_parts[1])
                except (TypeError, ValueError):
                    q = sympy.Number(s_parts[1])
                return sympy.Mul(p, sympy.Pow(q, -1, evaluate=False), evaluate=False)
            except (TypeError, ValueError):
                return sympy.Number(s)
        elif 'type' in atom and atom.get('type') == LATEXParser.E_NOTATION:
            s = atom.get('text').replace(",", "")
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):
                return sympy.Number(s)
        elif 'type' in atom and atom.get('type') == LATEXParser.DIFFERENTIAL:
            var = self.get_differential_var(atom.get('text'))
            return sympy.Symbol('d' + var.name, real=True, positive=True)
        elif 'mathit' in atom:
            text = self.rule2text(atom.get('mathit').get('mathit_text'))
            return sympy.Symbol(text, real=True, positive=True)
        elif 'type' in atom and atom.get('type') == LATEXParser.VARIABLE:
            text = atom.get('text')
            is_percent = text.endswith("\\%")
            trim_amount = 3 if is_percent else 1
            name = text[10:]
            name = name[0:len(name) - trim_amount]

            # revert to the "original" variable name stored from `pre_process_latex`
            # original name might be the same if it already had a wrapped single char sub
            name = self.variable_name_dict[name]

            # add hash to distinguish from regular symbols
            hash = hashlib.md5(name.encode()).hexdigest()
            symbol_name = name + hash

            # replace the variable for already known variable values
            if name in self.variable_values:
                # if a sympy class
                if isinstance(self.variable_values[name], tuple(all_classes)):
                    symbol = self.variable_values[name]

                # if NOT a sympy class
                else:
                    symbol = parse_expr(str(self.variable_values[name]))
            else:
                symbol = sympy.Symbol(symbol_name, real=True)

            if is_percent:
                return sympy.Mul(symbol, sympy.Pow(100, -1, evaluate=False), evaluate=False)

            # return the symbol
            return symbol

        elif 'type' in atom and atom.get('type') == LATEXParser.PERCENT_NUMBER:
            text = atom.get('text').replace("\\%", "").replace(",", "")
            try:
                number = sympy.Rational(text)
            except (TypeError, ValueError):
                number = sympy.Number(text)
            percent = sympy.Rational(number, 100)
            return percent

    def rule2text(self, ctx):
        stream = ctx.start.getInputStream()
        # starting index of starting token
        startIdx = ctx.start.start
        # stopping index of stopping token
        stopIdx = ctx.stop.stop

        return stream.getText(startIdx, stopIdx)

    def convert_frac(self, frac):
        # TODO
        # diff_op = False
        # partial_op = False
        # lower_itv = frac.get('expr')[1].getSourceInterval()
        # lower_itv_len = lower_itv[1] - lower_itv[0] + 1
        # if (frac.lower.start == frac.lower.stop and frac.lower.start.type == LATEXLexer.DIFFERENTIAL):
        #     wrt = self.get_differential_var_str(frac.lower.start.text)
        #     diff_op = True
        # elif (lower_itv_len == 2 and
        #       frac.lower.start.type == LATEXLexer.SYMBOL and
        #       frac.lower.start.text == '\\partial' and
        #       (frac.lower.stop.type == LATEXLexer.LETTER_NO_E or frac.lower.stop.type == LATEXLexer.SYMBOL)):
        #     partial_op = True
        #     wrt = frac.lower.stop.text
        #     if frac.lower.stop.type == LATEXLexer.SYMBOL:
        #         wrt = wrt[1:]

        # if diff_op or partial_op:
        #     wrt = sympy.Symbol(wrt, real=True, positive=True)
        #     if (diff_op and frac.upper.start == frac.upper.stop and
        #         frac.upper.start.type == LATEXLexer.LETTER_NO_E and
        #             frac.upper.start.text == 'd'):
        #         return [wrt]
        #     elif (partial_op and frac.upper.start == frac.upper.stop and
        #           frac.upper.start.type == LATEXLexer.SYMBOL and
        #           frac.upper.start.text == '\\partial'):
        #         return [wrt]
        #     upper_text = self.rule2text(frac.upper)

        #     expr_top = None
        #     if diff_op and upper_text.startswith('d'):
        #         expr_top = process_sympy(upper_text[1:])
        #     elif partial_op and frac.upper.start.text == '\\partial':
        #         expr_top = process_sympy(upper_text[len('\\partial'):])
        #     if expr_top:
        #         return sympy.Derivative(expr_top, wrt)

        expr_top = self.convert_expr(frac.get('upper'))
        expr_bot = self.convert_expr(frac.get('lower'))
        if expr_top.is_Matrix or expr_bot.is_Matrix:
            return sympy.MatMul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)
        else:
            return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

    def convert_binom(self, binom):
        expr_top = self.convert_expr(binom.upper)
        expr_bot = self.convert_expr(binom.lower)
        return sympy.binomial(expr_top, expr_bot)

    def convert_func(self, func):
        if 'func_normal_single_arg' in func:
            if 'func_single_arg' in func:  # function called with parenthesis
                arg = self.convert_func_arg(func.get('func_single_arg'))
            else:
                arg = self.convert_func_arg(func.get('func_single_arg_noparens'))

            if 'tokens' in func.get('func_normal_single_arg'):
                name = func.get('func_normal_single_arg').get('tokens')[0].get('text')[1:]
            else:
                name = func.get('func_normal_single_arg').get('func_normal_functions_single_arg').get('text')[1:]

            # change arc<trig> -> a<trig>
            if name in ["arcsin", "arccos", "arctan", "arccsc", "arcsec",
                        "arccot"]:
                name = "a" + name[3:]
                expr = getattr(sympy.functions, name)(arg, evaluate=False)
            elif name in ["arsinh", "arcosh", "artanh"]:
                name = "a" + name[2:]
                expr = getattr(sympy.functions, name)(arg, evaluate=False)
            elif name in ["arcsinh", "arccosh", "arctanh"]:
                name = "a" + name[3:]
                expr = getattr(sympy.functions, name)(arg, evaluate=False)
            elif name == "operatorname":
                operatorname = func.get('func_normal_single_arg').get('func_operator_names_single_arg').get('text')

                if operatorname in ["arsinh", "arcosh", "artanh"]:
                    operatorname = "a" + operatorname[2:]
                    expr = getattr(sympy.functions, operatorname)(arg, evaluate=False)
                elif operatorname in ["arcsinh", "arccosh", "arctanh"]:
                    operatorname = "a" + operatorname[3:]
                    expr = getattr(sympy.functions, operatorname)(arg, evaluate=False)
                elif operatorname == "floor":
                    expr = self.handle_floor(arg)
                elif operatorname == "ceil":
                    expr = self.handle_ceil(arg)
            elif name in ["log", "ln"]:
                if 'subexpr' in func:
                    if 'atom' in func.get('supexpr'):
                        base = self.convert_atom(func.get('supexpr').get('atom'))
                    else:
                        base = self.convert_expr(func.get('subexpr').get('expr'))
                elif name == "log":
                    base = 10
                elif name == "ln":
                    base = sympy.E
                expr = sympy.log(arg, base, evaluate=False)
            elif name in ["exp", "exponentialE"]:
                expr = sympy.exp(arg)
            elif name == "floor":
                expr = self.handle_floor(arg)
            elif name == "ceil":
                expr = self.handle_ceil(arg)

            func_pow = None
            should_pow = True
            if 'supexpr' in func:
                if 'expr' in func.get('supexpr'):
                    func_pow = self.convert_expr(func.get('supexpr').get('expr'))
                else:
                    func_pow = self.convert_atom(func.get('supexpr').get('atom'))

            if name in ["sin", "cos", "tan", "csc", "sec", "cot", "sinh", "cosh", "tanh"]:
                if func_pow == -1:
                    name = "a" + name
                    should_pow = False
                expr = getattr(sympy.functions, name)(arg, evaluate=False)

            if func_pow and should_pow:
                expr = sympy.Pow(expr, func_pow, evaluate=False)

            return expr

        elif 'func_normal_multi_arg' in func:
            if 'func_multi_arg' in func:  # function called with parenthesis
                args = func.get('func_multi_arg').get('text').split(",")
            else:
                args = func.get('func_multi_arg_noparens').split(",")

            args = list(map(lambda arg: process_sympy(arg, self.variable_values), args))

            if 'tokens' in func.get('func_normal_multi_arg'):
                name = func.get('func_normal_multi_arg').get('tokens')[0].get('text')[1:]
            else:
                name = func.get('func_normal_multi_arg').get('func_normal_functions_multi_arg').get('text')[1:]

            if name == "operatorname":
                operatorname = func.get('func_normal_multi_arg').get('func_operator_names_multi_arg').get('text')
                if operatorname in ["gcd", "lcm"]:
                    expr = self.handle_gcd_lcm(operatorname, args)
            elif name in ["gcd", "lcm"]:
                expr = self.handle_gcd_lcm(name, args)
            elif name in ["max", "min"]:
                name = name[0].upper() + name[1:]
                expr = getattr(sympy.functions, name)(*args, evaluate=False)

            func_pow = None
            should_pow = True
            if 'supexpr' in func:
                if 'expr' in func.get('supexpr'):
                    func_pow = self.convert_expr(func.get('supexpr').get('expr'))
                else:
                    func_pow = self.convert_atom(func.get('supexpr').get('atom'))

            if func_pow and should_pow:
                expr = sympy.Pow(expr, func_pow, evaluate=False)

            return expr

        elif 'type' in func and func.get('type') == LATEXParser.FUNC_INT or 'tokens' in func and func.get('tokens')[0].get('type') == LATEXParser.FUNC_INT:
            return self.handle_integral(func)
        elif 'type' in func and func.get('type') == LATEXParser.FUNC_SQRT or 'tokens' in func and func.get('tokens')[0].get('type') == LATEXParser.FUNC_SQRT:
            expr = self.convert_expr(func.get('base'))
            if func.get('root'):
                r = self.convert_expr(func.get('root'))
                return sympy.Pow(expr, 1 / r, evaluate=False)
            else:
                return sympy.Pow(expr, sympy.S.Half, evaluate=False)
        elif 'type' in func and func.get('type') == LATEXParser.FUNC_SUM:
            return self.handle_sum_or_prod(func, "summation")
        elif 'type' in func and func.get('type') == LATEXParser.FUNC_PROD:
            return self.handle_sum_or_prod(func, "product")
        elif 'type' in func and func.get('type') == LATEXParser.FUNC_LIM:
            return self.handle_limit(func)
        elif 'type' in func and func.get('type') == LATEXParser.EXP_E:
            return self.handle_exp(func)

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
        if 'tokens' in func and func.DIFFERENTIAL():
            int_var = self.get_differential_var(func.DIFFERENTIAL())
        else:
            for sym in integrand.atoms(sympy.Symbol):
                s = str(sym)
                if len(s) > 1 and s[0] == 'd':
                    if s[1] == '\\':
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
            if 'atom' in func.get('subexpr'):
                lower = self.convert_atom(func.get('subexpr').get('atom'))
            else:
                lower = self.convert_expr(func.get('subexpr').get('expr'))
            if 'atom' in func.get('supexpr'):
                upper = self.convert_atom(func.get('supexpr').get('atom'))
            else:
                upper = self.convert_expr(func.get('supexpr').get('expr'))
            return sympy.Integral(integrand, (int_var, lower, upper))
        else:
            return sympy.Integral(integrand, int_var)

    def handle_sum_or_prod(self, func, name):
        val = self.convert_mp(func.get('mp'))
        iter_var = self.convert_expr(func.get('subeq').get('equality').get('expr')[0])
        start = self.convert_expr(func.get('subeq').get('equality').get('expr')[1])
        if 'expr' in func.get('supexpr'):  # ^{expr}
            end = self.convert_expr(func.get('supexpr').get('expr'))
        else:  # ^atom
            end = self.convert_atom(func.get('supexpr').get('atom'))

        if name == "summation":
            return sympy.Sum(val, (iter_var, start, end))
        elif name == "product":
            return sympy.Product(val, (iter_var, start, end))

    def handle_limit(self, func):
        sub = func.get('limit_sub')
        if sub.LETTER_NO_E():
            var = sympy.Symbol(sub.get('text'), real=True, positive=True)
        elif sub.GREEK_CMD():
            var = sympy.Symbol(sub.get('text')[1:].strip(), real=True, positive=True)
        else:
            var = sympy.Symbol('x', real=True, positive=True)
        if sub.SUB():
            direction = "-"
        else:
            direction = "+"
        approaching = self.convert_expr(sub.get('expr'))
        content = self.convert_mp(func.get('mp'))

        return sympy.Limit(content, var, approaching, direction)

    def handle_exp(self, func):
        if 'supexpr' in func:
            if 'expr' in func.get('supexpr'):  # ^{expr}
                exp_arg = self.convert_expr(func.get('supexpr').get('expr'))
            else:  # ^atom
                exp_arg = self.convert_atom(func.get('supexpr').get('atom'))
        else:
            exp_arg = 1
        return sympy.exp(exp_arg)

    def handle_gcd_lcm(self, f, args):
        """
        Return the result of gcd() or lcm(), as UnevaluatedExpr

        f: str - name of function ("gcd" or "lcm")
        args: List[Expr] - list of function arguments
        """

        args = tuple(map(sympy.nsimplify, args))

        # gcd() and lcm() don't support evaluate=False
        return sympy.UnevaluatedExpr(getattr(sympy, f)(args))

    def handle_floor(self, expr):
        """
        Apply floor() then return the floored expression.

        expr: Expr - sympy expression as an argument to floor()
        """
        return sympy.functions.floor(expr, evaluate=False)

    def handle_ceil(self, expr):
        """
        Apply ceil() then return the ceil-ed expression.

        expr: Expr - sympy expression as an argument to ceil()
        """
        return sympy.functions.ceiling(expr, evaluate=False)

    def get_differential_var(self, d):
        text = self.get_differential_var_str(d)
        return sympy.Symbol(text, real=True, positive=True)

    def get_differential_var_str(self, text):
        for i in range(1, len(text)):
            c = text[i]
            if not (c == " " or c == "\r" or c == "\n" or c == "\t"):
                idx = i
                break
        text = text[idx:]
        if text[0] == "\\":
            text = text[1:]
        return text