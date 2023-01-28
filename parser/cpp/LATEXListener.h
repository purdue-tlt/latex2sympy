
// Generated from LATEX.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"
#include "LATEXParser.h"


namespace latex2antlr {

/**
 * This interface defines an abstract listener for a parse tree produced by LATEXParser.
 */
class  LATEXListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterAccent_symbol(LATEXParser::Accent_symbolContext *ctx) = 0;
  virtual void exitAccent_symbol(LATEXParser::Accent_symbolContext *ctx) = 0;

  virtual void enterMath(LATEXParser::MathContext *ctx) = 0;
  virtual void exitMath(LATEXParser::MathContext *ctx) = 0;

  virtual void enterMatrix(LATEXParser::MatrixContext *ctx) = 0;
  virtual void exitMatrix(LATEXParser::MatrixContext *ctx) = 0;

  virtual void enterMatrix_row(LATEXParser::Matrix_rowContext *ctx) = 0;
  virtual void exitMatrix_row(LATEXParser::Matrix_rowContext *ctx) = 0;

  virtual void enterRelation(LATEXParser::RelationContext *ctx) = 0;
  virtual void exitRelation(LATEXParser::RelationContext *ctx) = 0;

  virtual void enterRelation_list(LATEXParser::Relation_listContext *ctx) = 0;
  virtual void exitRelation_list(LATEXParser::Relation_listContext *ctx) = 0;

  virtual void enterRelation_list_content(LATEXParser::Relation_list_contentContext *ctx) = 0;
  virtual void exitRelation_list_content(LATEXParser::Relation_list_contentContext *ctx) = 0;

  virtual void enterEquality(LATEXParser::EqualityContext *ctx) = 0;
  virtual void exitEquality(LATEXParser::EqualityContext *ctx) = 0;

  virtual void enterExpr(LATEXParser::ExprContext *ctx) = 0;
  virtual void exitExpr(LATEXParser::ExprContext *ctx) = 0;

  virtual void enterAdditive(LATEXParser::AdditiveContext *ctx) = 0;
  virtual void exitAdditive(LATEXParser::AdditiveContext *ctx) = 0;

  virtual void enterMp(LATEXParser::MpContext *ctx) = 0;
  virtual void exitMp(LATEXParser::MpContext *ctx) = 0;

  virtual void enterMp_nofunc(LATEXParser::Mp_nofuncContext *ctx) = 0;
  virtual void exitMp_nofunc(LATEXParser::Mp_nofuncContext *ctx) = 0;

  virtual void enterUnary(LATEXParser::UnaryContext *ctx) = 0;
  virtual void exitUnary(LATEXParser::UnaryContext *ctx) = 0;

  virtual void enterUnary_nofunc(LATEXParser::Unary_nofuncContext *ctx) = 0;
  virtual void exitUnary_nofunc(LATEXParser::Unary_nofuncContext *ctx) = 0;

  virtual void enterPostfix(LATEXParser::PostfixContext *ctx) = 0;
  virtual void exitPostfix(LATEXParser::PostfixContext *ctx) = 0;

  virtual void enterPostfix_nofunc(LATEXParser::Postfix_nofuncContext *ctx) = 0;
  virtual void exitPostfix_nofunc(LATEXParser::Postfix_nofuncContext *ctx) = 0;

  virtual void enterPostfix_op(LATEXParser::Postfix_opContext *ctx) = 0;
  virtual void exitPostfix_op(LATEXParser::Postfix_opContext *ctx) = 0;

  virtual void enterEval_at(LATEXParser::Eval_atContext *ctx) = 0;
  virtual void exitEval_at(LATEXParser::Eval_atContext *ctx) = 0;

  virtual void enterEval_at_sub(LATEXParser::Eval_at_subContext *ctx) = 0;
  virtual void exitEval_at_sub(LATEXParser::Eval_at_subContext *ctx) = 0;

  virtual void enterEval_at_sup(LATEXParser::Eval_at_supContext *ctx) = 0;
  virtual void exitEval_at_sup(LATEXParser::Eval_at_supContext *ctx) = 0;

  virtual void enterExp(LATEXParser::ExpContext *ctx) = 0;
  virtual void exitExp(LATEXParser::ExpContext *ctx) = 0;

  virtual void enterExp_nofunc(LATEXParser::Exp_nofuncContext *ctx) = 0;
  virtual void exitExp_nofunc(LATEXParser::Exp_nofuncContext *ctx) = 0;

  virtual void enterComp(LATEXParser::CompContext *ctx) = 0;
  virtual void exitComp(LATEXParser::CompContext *ctx) = 0;

  virtual void enterComp_nofunc(LATEXParser::Comp_nofuncContext *ctx) = 0;
  virtual void exitComp_nofunc(LATEXParser::Comp_nofuncContext *ctx) = 0;

  virtual void enterGroup(LATEXParser::GroupContext *ctx) = 0;
  virtual void exitGroup(LATEXParser::GroupContext *ctx) = 0;

  virtual void enterAbs_group(LATEXParser::Abs_groupContext *ctx) = 0;
  virtual void exitAbs_group(LATEXParser::Abs_groupContext *ctx) = 0;

  virtual void enterFloor_group(LATEXParser::Floor_groupContext *ctx) = 0;
  virtual void exitFloor_group(LATEXParser::Floor_groupContext *ctx) = 0;

  virtual void enterCeil_group(LATEXParser::Ceil_groupContext *ctx) = 0;
  virtual void exitCeil_group(LATEXParser::Ceil_groupContext *ctx) = 0;

  virtual void enterAccent(LATEXParser::AccentContext *ctx) = 0;
  virtual void exitAccent(LATEXParser::AccentContext *ctx) = 0;

  virtual void enterAtom_expr(LATEXParser::Atom_exprContext *ctx) = 0;
  virtual void exitAtom_expr(LATEXParser::Atom_exprContext *ctx) = 0;

  virtual void enterAtom(LATEXParser::AtomContext *ctx) = 0;
  virtual void exitAtom(LATEXParser::AtomContext *ctx) = 0;

  virtual void enterMathit(LATEXParser::MathitContext *ctx) = 0;
  virtual void exitMathit(LATEXParser::MathitContext *ctx) = 0;

  virtual void enterMathit_text(LATEXParser::Mathit_textContext *ctx) = 0;
  virtual void exitMathit_text(LATEXParser::Mathit_textContext *ctx) = 0;

  virtual void enterFrac(LATEXParser::FracContext *ctx) = 0;
  virtual void exitFrac(LATEXParser::FracContext *ctx) = 0;

  virtual void enterBinom(LATEXParser::BinomContext *ctx) = 0;
  virtual void exitBinom(LATEXParser::BinomContext *ctx) = 0;

  virtual void enterFunc_normal_functions_single_arg(LATEXParser::Func_normal_functions_single_argContext *ctx) = 0;
  virtual void exitFunc_normal_functions_single_arg(LATEXParser::Func_normal_functions_single_argContext *ctx) = 0;

  virtual void enterFunc_normal_functions_multi_arg(LATEXParser::Func_normal_functions_multi_argContext *ctx) = 0;
  virtual void exitFunc_normal_functions_multi_arg(LATEXParser::Func_normal_functions_multi_argContext *ctx) = 0;

  virtual void enterFunc_operator_names_single_arg(LATEXParser::Func_operator_names_single_argContext *ctx) = 0;
  virtual void exitFunc_operator_names_single_arg(LATEXParser::Func_operator_names_single_argContext *ctx) = 0;

  virtual void enterFunc_operator_names_multi_arg(LATEXParser::Func_operator_names_multi_argContext *ctx) = 0;
  virtual void exitFunc_operator_names_multi_arg(LATEXParser::Func_operator_names_multi_argContext *ctx) = 0;

  virtual void enterFunc_normal_single_arg(LATEXParser::Func_normal_single_argContext *ctx) = 0;
  virtual void exitFunc_normal_single_arg(LATEXParser::Func_normal_single_argContext *ctx) = 0;

  virtual void enterFunc_normal_multi_arg(LATEXParser::Func_normal_multi_argContext *ctx) = 0;
  virtual void exitFunc_normal_multi_arg(LATEXParser::Func_normal_multi_argContext *ctx) = 0;

  virtual void enterFunc(LATEXParser::FuncContext *ctx) = 0;
  virtual void exitFunc(LATEXParser::FuncContext *ctx) = 0;

  virtual void enterArgs(LATEXParser::ArgsContext *ctx) = 0;
  virtual void exitArgs(LATEXParser::ArgsContext *ctx) = 0;

  virtual void enterLimit_sub(LATEXParser::Limit_subContext *ctx) = 0;
  virtual void exitLimit_sub(LATEXParser::Limit_subContext *ctx) = 0;

  virtual void enterFunc_single_arg(LATEXParser::Func_single_argContext *ctx) = 0;
  virtual void exitFunc_single_arg(LATEXParser::Func_single_argContext *ctx) = 0;

  virtual void enterFunc_single_arg_noparens(LATEXParser::Func_single_arg_noparensContext *ctx) = 0;
  virtual void exitFunc_single_arg_noparens(LATEXParser::Func_single_arg_noparensContext *ctx) = 0;

  virtual void enterFunc_multi_arg(LATEXParser::Func_multi_argContext *ctx) = 0;
  virtual void exitFunc_multi_arg(LATEXParser::Func_multi_argContext *ctx) = 0;

  virtual void enterFunc_multi_arg_noparens(LATEXParser::Func_multi_arg_noparensContext *ctx) = 0;
  virtual void exitFunc_multi_arg_noparens(LATEXParser::Func_multi_arg_noparensContext *ctx) = 0;

  virtual void enterSubexpr(LATEXParser::SubexprContext *ctx) = 0;
  virtual void exitSubexpr(LATEXParser::SubexprContext *ctx) = 0;

  virtual void enterSupexpr(LATEXParser::SupexprContext *ctx) = 0;
  virtual void exitSupexpr(LATEXParser::SupexprContext *ctx) = 0;

  virtual void enterSubeq(LATEXParser::SubeqContext *ctx) = 0;
  virtual void exitSubeq(LATEXParser::SubeqContext *ctx) = 0;


};

}  // namespace latex2antlr
