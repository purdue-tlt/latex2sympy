
// Generated from LATEX.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"
#include "LATEXListener.h"


namespace latex2antlr {

/**
 * This class provides an empty implementation of LATEXListener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  LATEXBaseListener : public LATEXListener {
public:

  virtual void enterAccent_symbol(LATEXParser::Accent_symbolContext * /*ctx*/) override { }
  virtual void exitAccent_symbol(LATEXParser::Accent_symbolContext * /*ctx*/) override { }

  virtual void enterMath(LATEXParser::MathContext * /*ctx*/) override { }
  virtual void exitMath(LATEXParser::MathContext * /*ctx*/) override { }

  virtual void enterMatrix(LATEXParser::MatrixContext * /*ctx*/) override { }
  virtual void exitMatrix(LATEXParser::MatrixContext * /*ctx*/) override { }

  virtual void enterMatrix_row(LATEXParser::Matrix_rowContext * /*ctx*/) override { }
  virtual void exitMatrix_row(LATEXParser::Matrix_rowContext * /*ctx*/) override { }

  virtual void enterRelation(LATEXParser::RelationContext * /*ctx*/) override { }
  virtual void exitRelation(LATEXParser::RelationContext * /*ctx*/) override { }

  virtual void enterRelation_list(LATEXParser::Relation_listContext * /*ctx*/) override { }
  virtual void exitRelation_list(LATEXParser::Relation_listContext * /*ctx*/) override { }

  virtual void enterRelation_list_content(LATEXParser::Relation_list_contentContext * /*ctx*/) override { }
  virtual void exitRelation_list_content(LATEXParser::Relation_list_contentContext * /*ctx*/) override { }

  virtual void enterEquality(LATEXParser::EqualityContext * /*ctx*/) override { }
  virtual void exitEquality(LATEXParser::EqualityContext * /*ctx*/) override { }

  virtual void enterExpr(LATEXParser::ExprContext * /*ctx*/) override { }
  virtual void exitExpr(LATEXParser::ExprContext * /*ctx*/) override { }

  virtual void enterAdditive(LATEXParser::AdditiveContext * /*ctx*/) override { }
  virtual void exitAdditive(LATEXParser::AdditiveContext * /*ctx*/) override { }

  virtual void enterMp(LATEXParser::MpContext * /*ctx*/) override { }
  virtual void exitMp(LATEXParser::MpContext * /*ctx*/) override { }

  virtual void enterMp_nofunc(LATEXParser::Mp_nofuncContext * /*ctx*/) override { }
  virtual void exitMp_nofunc(LATEXParser::Mp_nofuncContext * /*ctx*/) override { }

  virtual void enterUnary(LATEXParser::UnaryContext * /*ctx*/) override { }
  virtual void exitUnary(LATEXParser::UnaryContext * /*ctx*/) override { }

  virtual void enterUnary_nofunc(LATEXParser::Unary_nofuncContext * /*ctx*/) override { }
  virtual void exitUnary_nofunc(LATEXParser::Unary_nofuncContext * /*ctx*/) override { }

  virtual void enterPostfix(LATEXParser::PostfixContext * /*ctx*/) override { }
  virtual void exitPostfix(LATEXParser::PostfixContext * /*ctx*/) override { }

  virtual void enterPostfix_nofunc(LATEXParser::Postfix_nofuncContext * /*ctx*/) override { }
  virtual void exitPostfix_nofunc(LATEXParser::Postfix_nofuncContext * /*ctx*/) override { }

  virtual void enterPostfix_op(LATEXParser::Postfix_opContext * /*ctx*/) override { }
  virtual void exitPostfix_op(LATEXParser::Postfix_opContext * /*ctx*/) override { }

  virtual void enterEval_at(LATEXParser::Eval_atContext * /*ctx*/) override { }
  virtual void exitEval_at(LATEXParser::Eval_atContext * /*ctx*/) override { }

  virtual void enterEval_at_sub(LATEXParser::Eval_at_subContext * /*ctx*/) override { }
  virtual void exitEval_at_sub(LATEXParser::Eval_at_subContext * /*ctx*/) override { }

  virtual void enterEval_at_sup(LATEXParser::Eval_at_supContext * /*ctx*/) override { }
  virtual void exitEval_at_sup(LATEXParser::Eval_at_supContext * /*ctx*/) override { }

  virtual void enterExp(LATEXParser::ExpContext * /*ctx*/) override { }
  virtual void exitExp(LATEXParser::ExpContext * /*ctx*/) override { }

  virtual void enterExp_nofunc(LATEXParser::Exp_nofuncContext * /*ctx*/) override { }
  virtual void exitExp_nofunc(LATEXParser::Exp_nofuncContext * /*ctx*/) override { }

  virtual void enterComp(LATEXParser::CompContext * /*ctx*/) override { }
  virtual void exitComp(LATEXParser::CompContext * /*ctx*/) override { }

  virtual void enterComp_nofunc(LATEXParser::Comp_nofuncContext * /*ctx*/) override { }
  virtual void exitComp_nofunc(LATEXParser::Comp_nofuncContext * /*ctx*/) override { }

  virtual void enterGroup(LATEXParser::GroupContext * /*ctx*/) override { }
  virtual void exitGroup(LATEXParser::GroupContext * /*ctx*/) override { }

  virtual void enterAbs_group(LATEXParser::Abs_groupContext * /*ctx*/) override { }
  virtual void exitAbs_group(LATEXParser::Abs_groupContext * /*ctx*/) override { }

  virtual void enterFloor_group(LATEXParser::Floor_groupContext * /*ctx*/) override { }
  virtual void exitFloor_group(LATEXParser::Floor_groupContext * /*ctx*/) override { }

  virtual void enterCeil_group(LATEXParser::Ceil_groupContext * /*ctx*/) override { }
  virtual void exitCeil_group(LATEXParser::Ceil_groupContext * /*ctx*/) override { }

  virtual void enterAccent(LATEXParser::AccentContext * /*ctx*/) override { }
  virtual void exitAccent(LATEXParser::AccentContext * /*ctx*/) override { }

  virtual void enterAtom_expr(LATEXParser::Atom_exprContext * /*ctx*/) override { }
  virtual void exitAtom_expr(LATEXParser::Atom_exprContext * /*ctx*/) override { }

  virtual void enterAtom(LATEXParser::AtomContext * /*ctx*/) override { }
  virtual void exitAtom(LATEXParser::AtomContext * /*ctx*/) override { }

  virtual void enterMathit(LATEXParser::MathitContext * /*ctx*/) override { }
  virtual void exitMathit(LATEXParser::MathitContext * /*ctx*/) override { }

  virtual void enterMathit_text(LATEXParser::Mathit_textContext * /*ctx*/) override { }
  virtual void exitMathit_text(LATEXParser::Mathit_textContext * /*ctx*/) override { }

  virtual void enterFrac(LATEXParser::FracContext * /*ctx*/) override { }
  virtual void exitFrac(LATEXParser::FracContext * /*ctx*/) override { }

  virtual void enterBinom(LATEXParser::BinomContext * /*ctx*/) override { }
  virtual void exitBinom(LATEXParser::BinomContext * /*ctx*/) override { }

  virtual void enterFunc_normal_functions_single_arg(LATEXParser::Func_normal_functions_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_functions_single_arg(LATEXParser::Func_normal_functions_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_functions_multi_arg(LATEXParser::Func_normal_functions_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_functions_multi_arg(LATEXParser::Func_normal_functions_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_operator_names_single_arg(LATEXParser::Func_operator_names_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_operator_names_single_arg(LATEXParser::Func_operator_names_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_operator_names_multi_arg(LATEXParser::Func_operator_names_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_operator_names_multi_arg(LATEXParser::Func_operator_names_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_single_arg(LATEXParser::Func_normal_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_single_arg(LATEXParser::Func_normal_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_multi_arg(LATEXParser::Func_normal_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_multi_arg(LATEXParser::Func_normal_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc(LATEXParser::FuncContext * /*ctx*/) override { }
  virtual void exitFunc(LATEXParser::FuncContext * /*ctx*/) override { }

  virtual void enterArgs(LATEXParser::ArgsContext * /*ctx*/) override { }
  virtual void exitArgs(LATEXParser::ArgsContext * /*ctx*/) override { }

  virtual void enterLimit_sub(LATEXParser::Limit_subContext * /*ctx*/) override { }
  virtual void exitLimit_sub(LATEXParser::Limit_subContext * /*ctx*/) override { }

  virtual void enterFunc_single_arg(LATEXParser::Func_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_single_arg(LATEXParser::Func_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_single_arg_noparens(LATEXParser::Func_single_arg_noparensContext * /*ctx*/) override { }
  virtual void exitFunc_single_arg_noparens(LATEXParser::Func_single_arg_noparensContext * /*ctx*/) override { }

  virtual void enterFunc_multi_arg(LATEXParser::Func_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_multi_arg(LATEXParser::Func_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_multi_arg_noparens(LATEXParser::Func_multi_arg_noparensContext * /*ctx*/) override { }
  virtual void exitFunc_multi_arg_noparens(LATEXParser::Func_multi_arg_noparensContext * /*ctx*/) override { }

  virtual void enterSubexpr(LATEXParser::SubexprContext * /*ctx*/) override { }
  virtual void exitSubexpr(LATEXParser::SubexprContext * /*ctx*/) override { }

  virtual void enterSupexpr(LATEXParser::SupexprContext * /*ctx*/) override { }
  virtual void exitSupexpr(LATEXParser::SupexprContext * /*ctx*/) override { }

  virtual void enterSubeq(LATEXParser::SubeqContext * /*ctx*/) override { }
  virtual void exitSubeq(LATEXParser::SubeqContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

}  // namespace latex2antlr
