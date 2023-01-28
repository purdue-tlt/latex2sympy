# Generated from LATEX.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LATEXParser import LATEXParser
else:
    from LATEXParser import LATEXParser

# This class defines a complete listener for a parse tree produced by LATEXParser.


class LATEXListener(ParseTreeListener):

    # Enter a parse tree produced by LATEXParser#accent_symbol.
    def enterAccent_symbol(self, ctx: LATEXParser.Accent_symbolContext):
        pass

    # Exit a parse tree produced by LATEXParser#accent_symbol.
    def exitAccent_symbol(self, ctx: LATEXParser.Accent_symbolContext):
        pass

    # Enter a parse tree produced by LATEXParser#math.
    def enterMath(self, ctx: LATEXParser.MathContext):
        pass

    # Exit a parse tree produced by LATEXParser#math.
    def exitMath(self, ctx: LATEXParser.MathContext):
        pass

    # Enter a parse tree produced by LATEXParser#matrix.
    def enterMatrix(self, ctx: LATEXParser.MatrixContext):
        pass

    # Exit a parse tree produced by LATEXParser#matrix.
    def exitMatrix(self, ctx: LATEXParser.MatrixContext):
        pass

    # Enter a parse tree produced by LATEXParser#matrix_row.
    def enterMatrix_row(self, ctx: LATEXParser.Matrix_rowContext):
        pass

    # Exit a parse tree produced by LATEXParser#matrix_row.
    def exitMatrix_row(self, ctx: LATEXParser.Matrix_rowContext):
        pass

    # Enter a parse tree produced by LATEXParser#relation.
    def enterRelation(self, ctx: LATEXParser.RelationContext):
        pass

    # Exit a parse tree produced by LATEXParser#relation.
    def exitRelation(self, ctx: LATEXParser.RelationContext):
        pass

    # Enter a parse tree produced by LATEXParser#relation_list.
    def enterRelation_list(self, ctx: LATEXParser.Relation_listContext):
        pass

    # Exit a parse tree produced by LATEXParser#relation_list.
    def exitRelation_list(self, ctx: LATEXParser.Relation_listContext):
        pass

    # Enter a parse tree produced by LATEXParser#relation_list_content.
    def enterRelation_list_content(self, ctx: LATEXParser.Relation_list_contentContext):
        pass

    # Exit a parse tree produced by LATEXParser#relation_list_content.
    def exitRelation_list_content(self, ctx: LATEXParser.Relation_list_contentContext):
        pass

    # Enter a parse tree produced by LATEXParser#equality.
    def enterEquality(self, ctx: LATEXParser.EqualityContext):
        pass

    # Exit a parse tree produced by LATEXParser#equality.
    def exitEquality(self, ctx: LATEXParser.EqualityContext):
        pass

    # Enter a parse tree produced by LATEXParser#expr.
    def enterExpr(self, ctx: LATEXParser.ExprContext):
        pass

    # Exit a parse tree produced by LATEXParser#expr.
    def exitExpr(self, ctx: LATEXParser.ExprContext):
        pass

    # Enter a parse tree produced by LATEXParser#additive.
    def enterAdditive(self, ctx: LATEXParser.AdditiveContext):
        pass

    # Exit a parse tree produced by LATEXParser#additive.
    def exitAdditive(self, ctx: LATEXParser.AdditiveContext):
        pass

    # Enter a parse tree produced by LATEXParser#mp.
    def enterMp(self, ctx: LATEXParser.MpContext):
        pass

    # Exit a parse tree produced by LATEXParser#mp.
    def exitMp(self, ctx: LATEXParser.MpContext):
        pass

    # Enter a parse tree produced by LATEXParser#mp_nofunc.
    def enterMp_nofunc(self, ctx: LATEXParser.Mp_nofuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#mp_nofunc.
    def exitMp_nofunc(self, ctx: LATEXParser.Mp_nofuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#unary.
    def enterUnary(self, ctx: LATEXParser.UnaryContext):
        pass

    # Exit a parse tree produced by LATEXParser#unary.
    def exitUnary(self, ctx: LATEXParser.UnaryContext):
        pass

    # Enter a parse tree produced by LATEXParser#unary_nofunc.
    def enterUnary_nofunc(self, ctx: LATEXParser.Unary_nofuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#unary_nofunc.
    def exitUnary_nofunc(self, ctx: LATEXParser.Unary_nofuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#postfix.
    def enterPostfix(self, ctx: LATEXParser.PostfixContext):
        pass

    # Exit a parse tree produced by LATEXParser#postfix.
    def exitPostfix(self, ctx: LATEXParser.PostfixContext):
        pass

    # Enter a parse tree produced by LATEXParser#postfix_nofunc.
    def enterPostfix_nofunc(self, ctx: LATEXParser.Postfix_nofuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#postfix_nofunc.
    def exitPostfix_nofunc(self, ctx: LATEXParser.Postfix_nofuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#postfix_op.
    def enterPostfix_op(self, ctx: LATEXParser.Postfix_opContext):
        pass

    # Exit a parse tree produced by LATEXParser#postfix_op.
    def exitPostfix_op(self, ctx: LATEXParser.Postfix_opContext):
        pass

    # Enter a parse tree produced by LATEXParser#eval_at.
    def enterEval_at(self, ctx: LATEXParser.Eval_atContext):
        pass

    # Exit a parse tree produced by LATEXParser#eval_at.
    def exitEval_at(self, ctx: LATEXParser.Eval_atContext):
        pass

    # Enter a parse tree produced by LATEXParser#eval_at_sub.
    def enterEval_at_sub(self, ctx: LATEXParser.Eval_at_subContext):
        pass

    # Exit a parse tree produced by LATEXParser#eval_at_sub.
    def exitEval_at_sub(self, ctx: LATEXParser.Eval_at_subContext):
        pass

    # Enter a parse tree produced by LATEXParser#eval_at_sup.
    def enterEval_at_sup(self, ctx: LATEXParser.Eval_at_supContext):
        pass

    # Exit a parse tree produced by LATEXParser#eval_at_sup.
    def exitEval_at_sup(self, ctx: LATEXParser.Eval_at_supContext):
        pass

    # Enter a parse tree produced by LATEXParser#exp.
    def enterExp(self, ctx: LATEXParser.ExpContext):
        pass

    # Exit a parse tree produced by LATEXParser#exp.
    def exitExp(self, ctx: LATEXParser.ExpContext):
        pass

    # Enter a parse tree produced by LATEXParser#exp_nofunc.
    def enterExp_nofunc(self, ctx: LATEXParser.Exp_nofuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#exp_nofunc.
    def exitExp_nofunc(self, ctx: LATEXParser.Exp_nofuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#comp.
    def enterComp(self, ctx: LATEXParser.CompContext):
        pass

    # Exit a parse tree produced by LATEXParser#comp.
    def exitComp(self, ctx: LATEXParser.CompContext):
        pass

    # Enter a parse tree produced by LATEXParser#comp_nofunc.
    def enterComp_nofunc(self, ctx: LATEXParser.Comp_nofuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#comp_nofunc.
    def exitComp_nofunc(self, ctx: LATEXParser.Comp_nofuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#group.
    def enterGroup(self, ctx: LATEXParser.GroupContext):
        pass

    # Exit a parse tree produced by LATEXParser#group.
    def exitGroup(self, ctx: LATEXParser.GroupContext):
        pass

    # Enter a parse tree produced by LATEXParser#abs_group.
    def enterAbs_group(self, ctx: LATEXParser.Abs_groupContext):
        pass

    # Exit a parse tree produced by LATEXParser#abs_group.
    def exitAbs_group(self, ctx: LATEXParser.Abs_groupContext):
        pass

    # Enter a parse tree produced by LATEXParser#floor_group.
    def enterFloor_group(self, ctx: LATEXParser.Floor_groupContext):
        pass

    # Exit a parse tree produced by LATEXParser#floor_group.
    def exitFloor_group(self, ctx: LATEXParser.Floor_groupContext):
        pass

    # Enter a parse tree produced by LATEXParser#ceil_group.
    def enterCeil_group(self, ctx: LATEXParser.Ceil_groupContext):
        pass

    # Exit a parse tree produced by LATEXParser#ceil_group.
    def exitCeil_group(self, ctx: LATEXParser.Ceil_groupContext):
        pass

    # Enter a parse tree produced by LATEXParser#accent.
    def enterAccent(self, ctx: LATEXParser.AccentContext):
        pass

    # Exit a parse tree produced by LATEXParser#accent.
    def exitAccent(self, ctx: LATEXParser.AccentContext):
        pass

    # Enter a parse tree produced by LATEXParser#atom_expr.
    def enterAtom_expr(self, ctx: LATEXParser.Atom_exprContext):
        pass

    # Exit a parse tree produced by LATEXParser#atom_expr.
    def exitAtom_expr(self, ctx: LATEXParser.Atom_exprContext):
        pass

    # Enter a parse tree produced by LATEXParser#atom.
    def enterAtom(self, ctx: LATEXParser.AtomContext):
        pass

    # Exit a parse tree produced by LATEXParser#atom.
    def exitAtom(self, ctx: LATEXParser.AtomContext):
        pass

    # Enter a parse tree produced by LATEXParser#mathit.
    def enterMathit(self, ctx: LATEXParser.MathitContext):
        pass

    # Exit a parse tree produced by LATEXParser#mathit.
    def exitMathit(self, ctx: LATEXParser.MathitContext):
        pass

    # Enter a parse tree produced by LATEXParser#mathit_text.
    def enterMathit_text(self, ctx: LATEXParser.Mathit_textContext):
        pass

    # Exit a parse tree produced by LATEXParser#mathit_text.
    def exitMathit_text(self, ctx: LATEXParser.Mathit_textContext):
        pass

    # Enter a parse tree produced by LATEXParser#frac.
    def enterFrac(self, ctx: LATEXParser.FracContext):
        pass

    # Exit a parse tree produced by LATEXParser#frac.
    def exitFrac(self, ctx: LATEXParser.FracContext):
        pass

    # Enter a parse tree produced by LATEXParser#binom.
    def enterBinom(self, ctx: LATEXParser.BinomContext):
        pass

    # Exit a parse tree produced by LATEXParser#binom.
    def exitBinom(self, ctx: LATEXParser.BinomContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_normal_functions_single_arg.
    def enterFunc_normal_functions_single_arg(self, ctx: LATEXParser.Func_normal_functions_single_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_normal_functions_single_arg.
    def exitFunc_normal_functions_single_arg(self, ctx: LATEXParser.Func_normal_functions_single_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_normal_functions_multi_arg.
    def enterFunc_normal_functions_multi_arg(self, ctx: LATEXParser.Func_normal_functions_multi_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_normal_functions_multi_arg.
    def exitFunc_normal_functions_multi_arg(self, ctx: LATEXParser.Func_normal_functions_multi_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_operator_names_single_arg.
    def enterFunc_operator_names_single_arg(self, ctx: LATEXParser.Func_operator_names_single_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_operator_names_single_arg.
    def exitFunc_operator_names_single_arg(self, ctx: LATEXParser.Func_operator_names_single_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_operator_names_multi_arg.
    def enterFunc_operator_names_multi_arg(self, ctx: LATEXParser.Func_operator_names_multi_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_operator_names_multi_arg.
    def exitFunc_operator_names_multi_arg(self, ctx: LATEXParser.Func_operator_names_multi_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_normal_single_arg.
    def enterFunc_normal_single_arg(self, ctx: LATEXParser.Func_normal_single_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_normal_single_arg.
    def exitFunc_normal_single_arg(self, ctx: LATEXParser.Func_normal_single_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_normal_multi_arg.
    def enterFunc_normal_multi_arg(self, ctx: LATEXParser.Func_normal_multi_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_normal_multi_arg.
    def exitFunc_normal_multi_arg(self, ctx: LATEXParser.Func_normal_multi_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func.
    def enterFunc(self, ctx: LATEXParser.FuncContext):
        pass

    # Exit a parse tree produced by LATEXParser#func.
    def exitFunc(self, ctx: LATEXParser.FuncContext):
        pass

    # Enter a parse tree produced by LATEXParser#args.
    def enterArgs(self, ctx: LATEXParser.ArgsContext):
        pass

    # Exit a parse tree produced by LATEXParser#args.
    def exitArgs(self, ctx: LATEXParser.ArgsContext):
        pass

    # Enter a parse tree produced by LATEXParser#limit_sub.
    def enterLimit_sub(self, ctx: LATEXParser.Limit_subContext):
        pass

    # Exit a parse tree produced by LATEXParser#limit_sub.
    def exitLimit_sub(self, ctx: LATEXParser.Limit_subContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_single_arg.
    def enterFunc_single_arg(self, ctx: LATEXParser.Func_single_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_single_arg.
    def exitFunc_single_arg(self, ctx: LATEXParser.Func_single_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_single_arg_noparens.
    def enterFunc_single_arg_noparens(self, ctx: LATEXParser.Func_single_arg_noparensContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_single_arg_noparens.
    def exitFunc_single_arg_noparens(self, ctx: LATEXParser.Func_single_arg_noparensContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_multi_arg.
    def enterFunc_multi_arg(self, ctx: LATEXParser.Func_multi_argContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_multi_arg.
    def exitFunc_multi_arg(self, ctx: LATEXParser.Func_multi_argContext):
        pass

    # Enter a parse tree produced by LATEXParser#func_multi_arg_noparens.
    def enterFunc_multi_arg_noparens(self, ctx: LATEXParser.Func_multi_arg_noparensContext):
        pass

    # Exit a parse tree produced by LATEXParser#func_multi_arg_noparens.
    def exitFunc_multi_arg_noparens(self, ctx: LATEXParser.Func_multi_arg_noparensContext):
        pass

    # Enter a parse tree produced by LATEXParser#subexpr.
    def enterSubexpr(self, ctx: LATEXParser.SubexprContext):
        pass

    # Exit a parse tree produced by LATEXParser#subexpr.
    def exitSubexpr(self, ctx: LATEXParser.SubexprContext):
        pass

    # Enter a parse tree produced by LATEXParser#supexpr.
    def enterSupexpr(self, ctx: LATEXParser.SupexprContext):
        pass

    # Exit a parse tree produced by LATEXParser#supexpr.
    def exitSupexpr(self, ctx: LATEXParser.SupexprContext):
        pass

    # Enter a parse tree produced by LATEXParser#subeq.
    def enterSubeq(self, ctx: LATEXParser.SubeqContext):
        pass

    # Exit a parse tree produced by LATEXParser#subeq.
    def exitSubeq(self, ctx: LATEXParser.SubeqContext):
        pass


del LATEXParser
