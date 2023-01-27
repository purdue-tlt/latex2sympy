
// Generated from PS.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"
#include "PSParser.h"


namespace latex2sympy {

/**
 * This interface defines an abstract listener for a parse tree produced by PSParser.
 */
class  PSListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterAccent_symbol(PSParser::Accent_symbolContext *ctx) = 0;
  virtual void exitAccent_symbol(PSParser::Accent_symbolContext *ctx) = 0;

  virtual void enterMath(PSParser::MathContext *ctx) = 0;
  virtual void exitMath(PSParser::MathContext *ctx) = 0;

  virtual void enterMatrix(PSParser::MatrixContext *ctx) = 0;
  virtual void exitMatrix(PSParser::MatrixContext *ctx) = 0;

  virtual void enterMatrix_row(PSParser::Matrix_rowContext *ctx) = 0;
  virtual void exitMatrix_row(PSParser::Matrix_rowContext *ctx) = 0;

  virtual void enterRelation(PSParser::RelationContext *ctx) = 0;
  virtual void exitRelation(PSParser::RelationContext *ctx) = 0;

  virtual void enterRelation_list(PSParser::Relation_listContext *ctx) = 0;
  virtual void exitRelation_list(PSParser::Relation_listContext *ctx) = 0;

  virtual void enterRelation_list_content(PSParser::Relation_list_contentContext *ctx) = 0;
  virtual void exitRelation_list_content(PSParser::Relation_list_contentContext *ctx) = 0;

  virtual void enterEquality(PSParser::EqualityContext *ctx) = 0;
  virtual void exitEquality(PSParser::EqualityContext *ctx) = 0;

  virtual void enterExpr(PSParser::ExprContext *ctx) = 0;
  virtual void exitExpr(PSParser::ExprContext *ctx) = 0;

  virtual void enterAdditive(PSParser::AdditiveContext *ctx) = 0;
  virtual void exitAdditive(PSParser::AdditiveContext *ctx) = 0;

  virtual void enterMp(PSParser::MpContext *ctx) = 0;
  virtual void exitMp(PSParser::MpContext *ctx) = 0;

  virtual void enterMp_nofunc(PSParser::Mp_nofuncContext *ctx) = 0;
  virtual void exitMp_nofunc(PSParser::Mp_nofuncContext *ctx) = 0;

  virtual void enterUnary(PSParser::UnaryContext *ctx) = 0;
  virtual void exitUnary(PSParser::UnaryContext *ctx) = 0;

  virtual void enterUnary_nofunc(PSParser::Unary_nofuncContext *ctx) = 0;
  virtual void exitUnary_nofunc(PSParser::Unary_nofuncContext *ctx) = 0;

  virtual void enterPostfix(PSParser::PostfixContext *ctx) = 0;
  virtual void exitPostfix(PSParser::PostfixContext *ctx) = 0;

  virtual void enterPostfix_nofunc(PSParser::Postfix_nofuncContext *ctx) = 0;
  virtual void exitPostfix_nofunc(PSParser::Postfix_nofuncContext *ctx) = 0;

  virtual void enterPostfix_op(PSParser::Postfix_opContext *ctx) = 0;
  virtual void exitPostfix_op(PSParser::Postfix_opContext *ctx) = 0;

  virtual void enterEval_at(PSParser::Eval_atContext *ctx) = 0;
  virtual void exitEval_at(PSParser::Eval_atContext *ctx) = 0;

  virtual void enterEval_at_sub(PSParser::Eval_at_subContext *ctx) = 0;
  virtual void exitEval_at_sub(PSParser::Eval_at_subContext *ctx) = 0;

  virtual void enterEval_at_sup(PSParser::Eval_at_supContext *ctx) = 0;
  virtual void exitEval_at_sup(PSParser::Eval_at_supContext *ctx) = 0;

  virtual void enterExp(PSParser::ExpContext *ctx) = 0;
  virtual void exitExp(PSParser::ExpContext *ctx) = 0;

  virtual void enterExp_nofunc(PSParser::Exp_nofuncContext *ctx) = 0;
  virtual void exitExp_nofunc(PSParser::Exp_nofuncContext *ctx) = 0;

  virtual void enterComp(PSParser::CompContext *ctx) = 0;
  virtual void exitComp(PSParser::CompContext *ctx) = 0;

  virtual void enterComp_nofunc(PSParser::Comp_nofuncContext *ctx) = 0;
  virtual void exitComp_nofunc(PSParser::Comp_nofuncContext *ctx) = 0;

  virtual void enterGroup(PSParser::GroupContext *ctx) = 0;
  virtual void exitGroup(PSParser::GroupContext *ctx) = 0;

  virtual void enterAbs_group(PSParser::Abs_groupContext *ctx) = 0;
  virtual void exitAbs_group(PSParser::Abs_groupContext *ctx) = 0;

  virtual void enterFloor_group(PSParser::Floor_groupContext *ctx) = 0;
  virtual void exitFloor_group(PSParser::Floor_groupContext *ctx) = 0;

  virtual void enterCeil_group(PSParser::Ceil_groupContext *ctx) = 0;
  virtual void exitCeil_group(PSParser::Ceil_groupContext *ctx) = 0;

  virtual void enterAccent(PSParser::AccentContext *ctx) = 0;
  virtual void exitAccent(PSParser::AccentContext *ctx) = 0;

  virtual void enterAtom_expr(PSParser::Atom_exprContext *ctx) = 0;
  virtual void exitAtom_expr(PSParser::Atom_exprContext *ctx) = 0;

  virtual void enterAtom(PSParser::AtomContext *ctx) = 0;
  virtual void exitAtom(PSParser::AtomContext *ctx) = 0;

  virtual void enterMathit(PSParser::MathitContext *ctx) = 0;
  virtual void exitMathit(PSParser::MathitContext *ctx) = 0;

  virtual void enterMathit_text(PSParser::Mathit_textContext *ctx) = 0;
  virtual void exitMathit_text(PSParser::Mathit_textContext *ctx) = 0;

  virtual void enterFrac(PSParser::FracContext *ctx) = 0;
  virtual void exitFrac(PSParser::FracContext *ctx) = 0;

  virtual void enterBinom(PSParser::BinomContext *ctx) = 0;
  virtual void exitBinom(PSParser::BinomContext *ctx) = 0;

  virtual void enterFunc_normal_functions_single_arg(PSParser::Func_normal_functions_single_argContext *ctx) = 0;
  virtual void exitFunc_normal_functions_single_arg(PSParser::Func_normal_functions_single_argContext *ctx) = 0;

  virtual void enterFunc_normal_functions_multi_arg(PSParser::Func_normal_functions_multi_argContext *ctx) = 0;
  virtual void exitFunc_normal_functions_multi_arg(PSParser::Func_normal_functions_multi_argContext *ctx) = 0;

  virtual void enterFunc_operator_names_single_arg(PSParser::Func_operator_names_single_argContext *ctx) = 0;
  virtual void exitFunc_operator_names_single_arg(PSParser::Func_operator_names_single_argContext *ctx) = 0;

  virtual void enterFunc_operator_names_multi_arg(PSParser::Func_operator_names_multi_argContext *ctx) = 0;
  virtual void exitFunc_operator_names_multi_arg(PSParser::Func_operator_names_multi_argContext *ctx) = 0;

  virtual void enterFunc_normal_single_arg(PSParser::Func_normal_single_argContext *ctx) = 0;
  virtual void exitFunc_normal_single_arg(PSParser::Func_normal_single_argContext *ctx) = 0;

  virtual void enterFunc_normal_multi_arg(PSParser::Func_normal_multi_argContext *ctx) = 0;
  virtual void exitFunc_normal_multi_arg(PSParser::Func_normal_multi_argContext *ctx) = 0;

  virtual void enterFunc(PSParser::FuncContext *ctx) = 0;
  virtual void exitFunc(PSParser::FuncContext *ctx) = 0;

  virtual void enterArgs(PSParser::ArgsContext *ctx) = 0;
  virtual void exitArgs(PSParser::ArgsContext *ctx) = 0;

  virtual void enterLimit_sub(PSParser::Limit_subContext *ctx) = 0;
  virtual void exitLimit_sub(PSParser::Limit_subContext *ctx) = 0;

  virtual void enterFunc_single_arg(PSParser::Func_single_argContext *ctx) = 0;
  virtual void exitFunc_single_arg(PSParser::Func_single_argContext *ctx) = 0;

  virtual void enterFunc_single_arg_noparens(PSParser::Func_single_arg_noparensContext *ctx) = 0;
  virtual void exitFunc_single_arg_noparens(PSParser::Func_single_arg_noparensContext *ctx) = 0;

  virtual void enterFunc_multi_arg(PSParser::Func_multi_argContext *ctx) = 0;
  virtual void exitFunc_multi_arg(PSParser::Func_multi_argContext *ctx) = 0;

  virtual void enterFunc_multi_arg_noparens(PSParser::Func_multi_arg_noparensContext *ctx) = 0;
  virtual void exitFunc_multi_arg_noparens(PSParser::Func_multi_arg_noparensContext *ctx) = 0;

  virtual void enterSubexpr(PSParser::SubexprContext *ctx) = 0;
  virtual void exitSubexpr(PSParser::SubexprContext *ctx) = 0;

  virtual void enterSupexpr(PSParser::SupexprContext *ctx) = 0;
  virtual void exitSupexpr(PSParser::SupexprContext *ctx) = 0;

  virtual void enterSubeq(PSParser::SubeqContext *ctx) = 0;
  virtual void exitSubeq(PSParser::SubeqContext *ctx) = 0;


};

}  // namespace latex2sympy
