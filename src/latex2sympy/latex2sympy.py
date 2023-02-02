import antlr4
from antlr4.error.ErrorListener import ErrorListener
import hashlib
from latex2sympy.parser.python.LATEXParser import LATEXParser
from latex2sympy.parser.python.LATEXLexer import LATEXLexer
import re
import sympy
from sympy.core.core import all_classes
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.str import StrPrinter


def process_sympy(latex, variable_values={}):
    instance = LatexToSympy(latex, variable_values)
    return instance.process_sympy()


class MathErrorListener(ErrorListener):
    def __init__(self, src):
        super(ErrorListener, self).__init__()
        self.src = src

    def syntaxError(self, recog, symbol, line, col, msg, e):
        fmt = "%s\n%s\n%s"
        marker = "~" * col + "^"

        if msg.startswith("missing"):
            err = fmt % (msg, self.src, marker)
        elif msg.startswith("no viable"):
            err = fmt % ("I expected something else here", self.src, marker)
        elif msg.startswith("mismatched"):
            names = LATEXParser.literalNames
            expected = [names[i] for i in e.getExpectedTokens() if i < len(names)]
            if len(expected) < 10:
                expected = " ".join(expected)
                err = (fmt % ("I expected one of these: " + expected, self.src, marker))
            else:
                err = (fmt % ("I expected something else here", self.src, marker))
        else:
            err = fmt % ("I don't understand this", self.src, marker)
        raise Exception(err)


class LatexToSympy:
    def __init__(self, latex, variable_values={}):
        self.latex = latex
        if len(variable_values) > 0:
            self.variable_values = variable_values
        else:
            self.variable_values = {}

    def process_sympy(self):

        # pre-processing
        pre_processed_latex = self.pre_process_latex(self.latex)

        # setup listener
        matherror = MathErrorListener(pre_processed_latex)

        # stream input
        stream = antlr4.InputStream(pre_processed_latex)
        lex = LATEXLexer(stream)
        lex.removeErrorListeners()
        lex.addErrorListener(matherror)

        tokens = antlr4.CommonTokenStream(lex)
        parser = LATEXParser(tokens)

        # remove default console error listener
        parser.removeErrorListeners()
        parser.addErrorListener(matherror)

        # process the input
        return_data = None
        math = parser.math()

        # if a list
        if math.relation_list():
            return_data = []

            # go over list items
            relation_list = math.relation_list().relation_list_content()
            for list_item in relation_list.relation():
                expr = self.convert_relation(list_item)
                return_data.append(expr)

        # if not, do default
        else:
            relation = math.relation()
            return_data = self.convert_relation(relation)

        return return_data

    def pre_process_latex(self, latex):
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
        if rel.expr():
            return self.convert_expr(rel.expr())

        lh = self.convert_relation(rel.relation(0))
        rh = self.convert_relation(rel.relation(1))
        if rel.LT():
            return sympy.StrictLessThan(lh, rh, evaluate=False)
        elif rel.LTE():
            return sympy.LessThan(lh, rh, evaluate=False)
        elif rel.GT():
            return sympy.StrictGreaterThan(lh, rh, evaluate=False)
        elif rel.GTE():
            return sympy.GreaterThan(lh, rh, evaluate=False)
        elif rel.EQUAL():
            return sympy.Eq(lh, rh, evaluate=False)
        elif rel.UNEQUAL():
            return sympy.Ne(lh, rh, evaluate=False)

    def convert_expr(self, expr):
        if expr.additive():
            return self.convert_add(expr.additive())

    def convert_matrix(self, matrix):
        # build matrix
        row = matrix.matrix_row()
        tmp = []
        rows = 0
        for r in row:
            tmp.append([])
            for expr in r.expr():
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
        if add.ADD():
            lh = self.convert_add(add.additive(0))
            rh = self.convert_add(add.additive(1))

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, rh)
            else:
                return self.add_flat(lh, rh)
        elif add.SUB():
            lh = self.convert_add(add.additive(0))
            rh = self.convert_add(add.additive(1))

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_add_flat(lh, self.mat_mul_flat(-1, rh))
            else:
                rh = self.mul_flat(-1, rh)
                return self.add_flat(lh, rh)
        else:
            return self.convert_mp(add.mp())

    def convert_mp(self, mp):
        if hasattr(mp, 'mp'):
            mp_left = mp.mp(0)
            mp_right = mp.mp(1)
        else:
            mp_left = mp.mp_nofunc(0)
            mp_right = mp.mp_nofunc(1)

        if mp.MUL() or mp.CMD_TIMES() or mp.CMD_CDOT():
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)

            if lh.is_Matrix or rh.is_Matrix:
                return self.mat_mul_flat(lh, rh)
            else:
                return self.mul_flat(lh, rh)
        elif mp.DIV() or mp.CMD_DIV() or mp.COLON():
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if lh.is_Matrix or rh.is_Matrix:
                return sympy.MatMul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
            else:
                return sympy.Mul(lh, sympy.Pow(rh, -1, evaluate=False), evaluate=False)
        elif mp.CMD_MOD():
            lh = self.convert_mp(mp_left)
            rh = self.convert_mp(mp_right)
            if rh.is_Matrix:
                raise Exception("Cannot perform modulo operation with a matrix as an operand")
            else:
                return sympy.Mod(lh, rh, evaluate=False)
        else:
            if hasattr(mp, 'unary'):
                return self.convert_unary(mp.unary())
            else:
                return self.convert_unary(mp.unary_nofunc())

    def convert_unary(self, unary):
        if hasattr(unary, 'unary'):
            nested_unary = unary.unary()
        else:
            nested_unary = unary.unary_nofunc()
        if hasattr(unary, 'postfix_nofunc'):
            first = unary.postfix()
            tail = unary.postfix_nofunc()
            postfix = [first] + tail
        else:
            postfix = unary.postfix()

        if unary.ADD():
            return self.convert_unary(nested_unary)
        elif unary.SUB():
            tmp_convert_nested_unary = self.convert_unary(nested_unary)
            if tmp_convert_nested_unary.is_Matrix:
                return self.mat_mul_flat(-1, tmp_convert_nested_unary, evaluate=False)
            else:
                if tmp_convert_nested_unary.func.is_Number:
                    return -tmp_convert_nested_unary
                else:
                    return self.mul_flat(-1, tmp_convert_nested_unary)
        elif postfix:
            return self.convert_postfix_list(postfix)

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
        if at.expr():
            at_expr = self.convert_expr(at.expr())
            syms = at_expr.atoms(sympy.Symbol)
            if len(syms) == 0:
                return expr
            elif len(syms) > 0:
                sym = next(iter(syms))
                return expr.subs(sym, at_expr)
        elif at.equality():
            lh = self.convert_expr(at.equality().expr(0))
            rh = self.convert_expr(at.equality().expr(1))
            return expr.subs(lh, rh)

    def convert_postfix(self, postfix):
        if hasattr(postfix, 'exp'):
            exp_nested = postfix.exp()
        else:
            exp_nested = postfix.exp_nofunc()

        exp = self.convert_exp(exp_nested)
        for op in postfix.postfix_op():
            if op.BANG():
                if isinstance(exp, list):
                    raise Exception("Cannot apply postfix to derivative")
                exp = sympy.factorial(exp, evaluate=False)
            elif op.eval_at():
                ev = op.eval_at()
                at_b = None
                at_a = None
                if ev.eval_at_sup():
                    at_b = self.do_subs(exp, ev.eval_at_sup())
                if ev.eval_at_sub():
                    at_a = self.do_subs(exp, ev.eval_at_sub())
                if at_b is not None and at_a is not None:
                    exp = self.add_flat(at_b, self.mul_flat(at_a, -1))
                elif at_b is not None:
                    exp = at_b
                elif at_a is not None:
                    exp = at_a

        return exp

    def convert_exp(self, exp):
        if hasattr(exp, 'exp'):
            exp_nested = exp.exp()
        else:
            exp_nested = exp.exp_nofunc()

        if exp_nested:
            base = self.convert_exp(exp_nested)
            if isinstance(base, list):
                raise Exception("Cannot raise derivative to power")
            if exp.atom():
                exponent = self.convert_atom(exp.atom())
            elif exp.expr():
                exponent = self.convert_expr(exp.expr())
            return sympy.Pow(base, exponent, evaluate=False)
        else:
            if hasattr(exp, 'comp'):
                return self.convert_comp(exp.comp())
            else:
                return self.convert_comp(exp.comp_nofunc())

    def convert_comp(self, comp):
        if comp.group():
            return self.convert_expr(comp.group().expr())
        elif comp.abs_group():
            return sympy.Abs(self.convert_expr(comp.abs_group().expr()), evaluate=False)
        elif comp.floor_group():
            return self.handle_floor(self.convert_expr(comp.floor_group().expr()))
        elif comp.ceil_group():
            return self.handle_ceil(self.convert_expr(comp.ceil_group().expr()))
        elif comp.atom():
            return self.convert_atom(comp.atom())
        elif comp.frac():
            return self.convert_frac(comp.frac())
        elif comp.binom():
            return self.convert_binom(comp.binom())
        elif comp.matrix():
            return self.convert_matrix(comp.matrix())
        elif comp.func():
            return self.convert_func(comp.func())

    def convert_atom(self, atom):
        if atom.atom_expr():
            atom_expr = atom.atom_expr()

            # find the atom's text
            atom_text = ''
            if atom_expr.LETTER_NO_E():
                atom_text = atom_expr.LETTER_NO_E().getText()
                if atom_text == "I":
                    return sympy.I
            elif atom_expr.GREEK_CMD():
                atom_text = atom_expr.GREEK_CMD().getText()[1:].strip()
            elif atom_expr.accent():
                atom_accent = atom_expr.accent()
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
            if atom_expr.subexpr():
                subexpr = atom_expr.subexpr()
                subscript = None
                if subexpr.expr():  # subscript is expr
                    subscript = subexpr.expr().getText().strip()
                elif subexpr.atom():  # subscript is atom
                    subscript = subexpr.atom().getText().strip()
                elif subexpr.args():  # subscript is args
                    subscript = subexpr.args().getText().strip()
                subscript_inner_text = StrPrinter().doprint(subscript)
                if len(subscript_inner_text) > 1:
                    subscript_text = '_{' + subscript_inner_text + '}'
                else:
                    subscript_text = '_' + subscript_inner_text

            # construct the symbol using the text and optional subscript
            atom_symbol = sympy.Symbol(atom_text + subscript_text, real=True, positive=True)

            # find the atom's superscript, and return as a Pow if found
            if atom_expr.supexpr():
                supexpr = atom_expr.supexpr()
                func_pow = None
                if supexpr.expr():
                    func_pow = self.convert_expr(supexpr.expr())
                else:
                    func_pow = self.convert_atom(supexpr.atom())
                return sympy.Pow(atom_symbol, func_pow, evaluate=False)

            return atom_symbol
        elif atom.SYMBOL():
            s = atom.SYMBOL().getText().replace("\\$", "").replace("\\%", "")
            if s == "\\infty":
                return sympy.oo
            elif s == '\\pi':
                return sympy.pi
            elif s == '\\emptyset':
                return sympy.S.EmptySet
            else:
                raise Exception("Unrecognized symbol")
        elif atom.NUMBER():
            s = atom.NUMBER().getText().replace(",", "")
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):
                return sympy.Number(s)
        elif atom.SCI_NOTATION_NUMBER():
            s = atom.SCI_NOTATION_NUMBER().getText()
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
        elif atom.FRACTION_NUMBER():
            s = atom.FRACTION_NUMBER().getText().replace("\\frac{", "").replace("}{", "/").replace("}", "").replace(",", "")
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
        elif atom.E_NOTATION():
            s = atom.E_NOTATION().getText().replace(",", "")
            try:
                sr = sympy.Rational(s)
                return sr
            except (TypeError, ValueError):
                return sympy.Number(s)
        elif atom.DIFFERENTIAL():
            var = self.get_differential_var(atom.DIFFERENTIAL())
            return sympy.Symbol('d' + var.name, real=True, positive=True)
        elif atom.mathit():
            text = self.rule2text(atom.mathit().mathit_text())
            return sympy.Symbol(text, real=True, positive=True)
        elif atom.VARIABLE():
            text = atom.VARIABLE().getText()
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

        elif atom.PERCENT_NUMBER():
            text = atom.PERCENT_NUMBER().getText().replace("\\%", "").replace(",", "")
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
        diff_op = False
        partial_op = False
        lower_itv = frac.lower.getSourceInterval()
        lower_itv_len = lower_itv[1] - lower_itv[0] + 1
        if (frac.lower.start == frac.lower.stop and frac.lower.start.type == LATEXLexer.DIFFERENTIAL):
            wrt = self.get_differential_var_str(frac.lower.start.text)
            diff_op = True
        elif (lower_itv_len == 2 and
              frac.lower.start.type == LATEXLexer.SYMBOL and
              frac.lower.start.text == '\\partial' and
              (frac.lower.stop.type == LATEXLexer.LETTER_NO_E or frac.lower.stop.type == LATEXLexer.SYMBOL)):
            partial_op = True
            wrt = frac.lower.stop.text
            if frac.lower.stop.type == LATEXLexer.SYMBOL:
                wrt = wrt[1:]

        if diff_op or partial_op:
            wrt = sympy.Symbol(wrt, real=True, positive=True)
            if (diff_op and frac.upper.start == frac.upper.stop and
                frac.upper.start.type == LATEXLexer.LETTER_NO_E and
                    frac.upper.start.text == 'd'):
                return [wrt]
            elif (partial_op and frac.upper.start == frac.upper.stop and
                  frac.upper.start.type == LATEXLexer.SYMBOL and
                  frac.upper.start.text == '\\partial'):
                return [wrt]
            upper_text = self.rule2text(frac.upper)

            expr_top = None
            if diff_op and upper_text.startswith('d'):
                expr_top = process_sympy(upper_text[1:])
            elif partial_op and frac.upper.start.text == '\\partial':
                expr_top = process_sympy(upper_text[len('\\partial'):])
            if expr_top:
                return sympy.Derivative(expr_top, wrt)

        expr_top = self.convert_expr(frac.upper)
        expr_bot = self.convert_expr(frac.lower)
        if expr_top.is_Matrix or expr_bot.is_Matrix:
            return sympy.MatMul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)
        else:
            return sympy.Mul(expr_top, sympy.Pow(expr_bot, -1, evaluate=False), evaluate=False)

    def convert_binom(self, binom):
        expr_top = self.convert_expr(binom.upper)
        expr_bot = self.convert_expr(binom.lower)
        return sympy.binomial(expr_top, expr_bot)

    def convert_func(self, func):
        if func.func_normal_single_arg():
            if func.L_PAREN():  # function called with parenthesis
                arg = self.convert_func_arg(func.func_single_arg())
            else:
                arg = self.convert_func_arg(func.func_single_arg_noparens())

            name = func.func_normal_single_arg().start.text[1:]

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
                operatorname = func.func_normal_single_arg().func_operator_name.getText()

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
                if func.subexpr():
                    if func.subexpr().atom():
                        base = self.convert_atom(func.subexpr().atom())
                    else:
                        base = self.convert_expr(func.subexpr().expr())
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
            if func.supexpr():
                if func.supexpr().expr():
                    func_pow = self.convert_expr(func.supexpr().expr())
                else:
                    func_pow = self.convert_atom(func.supexpr().atom())

            if name in ["sin", "cos", "tan", "csc", "sec", "cot", "sinh", "cosh", "tanh"]:
                if func_pow == -1:
                    name = "a" + name
                    should_pow = False
                expr = getattr(sympy.functions, name)(arg, evaluate=False)

            if func_pow and should_pow:
                expr = sympy.Pow(expr, func_pow, evaluate=False)

            return expr

        elif func.func_normal_multi_arg():
            if func.L_PAREN():  # function called with parenthesis
                args = func.func_multi_arg().getText().split(",")
            else:
                args = func.func_multi_arg_noparens().split(",")

            args = list(map(lambda arg: process_sympy(arg, self.variable_values), args))
            name = func.func_normal_multi_arg().start.text[1:]

            if name == "operatorname":
                operatorname = func.func_normal_multi_arg().func_operator_name.getText()
                if operatorname in ["gcd", "lcm"]:
                    expr = self.handle_gcd_lcm(operatorname, args)
            elif name in ["gcd", "lcm"]:
                expr = self.handle_gcd_lcm(name, args)
            elif name in ["max", "min"]:
                name = name[0].upper() + name[1:]
                expr = getattr(sympy.functions, name)(*args, evaluate=False)

            func_pow = None
            should_pow = True
            if func.supexpr():
                if func.supexpr().expr():
                    func_pow = self.convert_expr(func.supexpr().expr())
                else:
                    func_pow = self.convert_atom(func.supexpr().atom())

            if func_pow and should_pow:
                expr = sympy.Pow(expr, func_pow, evaluate=False)

            return expr

        elif func.FUNC_INT():
            return self.handle_integral(func)
        elif func.FUNC_SQRT():
            expr = self.convert_expr(func.base)
            if func.root:
                r = self.convert_expr(func.root)
                return sympy.Pow(expr, 1 / r, evaluate=False)
            else:
                return sympy.Pow(expr, sympy.S.Half, evaluate=False)
        elif func.FUNC_SUM():
            return self.handle_sum_or_prod(func, "summation")
        elif func.FUNC_PROD():
            return self.handle_sum_or_prod(func, "product")
        elif func.FUNC_LIM():
            return self.handle_limit(func)
        elif func.EXP_E():
            return self.handle_exp(func)

    def convert_func_arg(self, arg):
        if hasattr(arg, 'expr'):
            return self.convert_expr(arg.expr())
        else:
            return self.convert_mp(arg.mp_nofunc())

    def handle_integral(self, func):
        if func.additive():
            integrand = self.convert_add(func.additive())
        elif func.frac():
            integrand = self.convert_frac(func.frac())
        else:
            integrand = 1

        int_var = None
        if func.DIFFERENTIAL():
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

        if func.subexpr():
            if func.subexpr().atom():
                lower = self.convert_atom(func.subexpr().atom())
            else:
                lower = self.convert_expr(func.subexpr().expr())
            if func.supexpr().atom():
                upper = self.convert_atom(func.supexpr().atom())
            else:
                upper = self.convert_expr(func.supexpr().expr())
            return sympy.Integral(integrand, (int_var, lower, upper))
        else:
            return sympy.Integral(integrand, int_var)

    def handle_sum_or_prod(self, func, name):
        val = self.convert_mp(func.mp())
        iter_var = self.convert_expr(func.subeq().equality().expr(0))
        start = self.convert_expr(func.subeq().equality().expr(1))
        if func.supexpr().expr():  # ^{expr}
            end = self.convert_expr(func.supexpr().expr())
        else:  # ^atom
            end = self.convert_atom(func.supexpr().atom())

        if name == "summation":
            return sympy.Sum(val, (iter_var, start, end))
        elif name == "product":
            return sympy.Product(val, (iter_var, start, end))

    def handle_limit(self, func):
        sub = func.limit_sub()
        if sub.LETTER_NO_E():
            var = sympy.Symbol(sub.LETTER_NO_E().getText(), real=True, positive=True)
        elif sub.GREEK_CMD():
            var = sympy.Symbol(sub.GREEK_CMD().getText()[1:].strip(), real=True, positive=True)
        else:
            var = sympy.Symbol('x', real=True, positive=True)
        if sub.SUB():
            direction = "-"
        else:
            direction = "+"
        approaching = self.convert_expr(sub.expr())
        content = self.convert_mp(func.mp())

        return sympy.Limit(content, var, approaching, direction)

    def handle_exp(self, func):
        if func.supexpr():
            if func.supexpr().expr():  # ^{expr}
                exp_arg = self.convert_expr(func.supexpr().expr())
            else:  # ^atom
                exp_arg = self.convert_atom(func.supexpr().atom())
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
        text = self.get_differential_var_str(d.getText())
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