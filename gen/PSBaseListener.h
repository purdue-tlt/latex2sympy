
// Generated from PS.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"
#include "PSListener.h"


namespace latex2sympy {

/**
 * This class provides an empty implementation of PSListener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  PSBaseListener : public PSListener {
public:

  virtual void enterAccent_symbol(PSParser::Accent_symbolContext * /*ctx*/) override { }
  virtual void exitAccent_symbol(PSParser::Accent_symbolContext * /*ctx*/) override { }

  virtual void enterMath(PSParser::MathContext * /*ctx*/) override { }
  virtual void exitMath(PSParser::MathContext * /*ctx*/) override { }

  virtual void enterMatrix(PSParser::MatrixContext * /*ctx*/) override { }
  virtual void exitMatrix(PSParser::MatrixContext * /*ctx*/) override { }

  virtual void enterMatrix_row(PSParser::Matrix_rowContext * /*ctx*/) override { }
  virtual void exitMatrix_row(PSParser::Matrix_rowContext * /*ctx*/) override { }

  virtual void enterRelation(PSParser::RelationContext * /*ctx*/) override { }
  virtual void exitRelation(PSParser::RelationContext * /*ctx*/) override { }

  virtual void enterRelation_list(PSParser::Relation_listContext * /*ctx*/) override { }
  virtual void exitRelation_list(PSParser::Relation_listContext * /*ctx*/) override { }

  virtual void enterRelation_list_content(PSParser::Relation_list_contentContext * /*ctx*/) override { }
  virtual void exitRelation_list_content(PSParser::Relation_list_contentContext * /*ctx*/) override { }

  virtual void enterEquality(PSParser::EqualityContext * /*ctx*/) override { }
  virtual void exitEquality(PSParser::EqualityContext * /*ctx*/) override { }

  virtual void enterExpr(PSParser::ExprContext * /*ctx*/) override { }
  virtual void exitExpr(PSParser::ExprContext * /*ctx*/) override { }

  virtual void enterAdditive(PSParser::AdditiveContext * /*ctx*/) override { }
  virtual void exitAdditive(PSParser::AdditiveContext * /*ctx*/) override { }

  virtual void enterMp(PSParser::MpContext * /*ctx*/) override { }
  virtual void exitMp(PSParser::MpContext * /*ctx*/) override { }

  virtual void enterMp_nofunc(PSParser::Mp_nofuncContext * /*ctx*/) override { }
  virtual void exitMp_nofunc(PSParser::Mp_nofuncContext * /*ctx*/) override { }

  virtual void enterUnary(PSParser::UnaryContext * /*ctx*/) override { }
  virtual void exitUnary(PSParser::UnaryContext * /*ctx*/) override { }

  virtual void enterUnary_nofunc(PSParser::Unary_nofuncContext * /*ctx*/) override { }
  virtual void exitUnary_nofunc(PSParser::Unary_nofuncContext * /*ctx*/) override { }

  virtual void enterPostfix(PSParser::PostfixContext * /*ctx*/) override { }
  virtual void exitPostfix(PSParser::PostfixContext * /*ctx*/) override { }

  virtual void enterPostfix_nofunc(PSParser::Postfix_nofuncContext * /*ctx*/) override { }
  virtual void exitPostfix_nofunc(PSParser::Postfix_nofuncContext * /*ctx*/) override { }

  virtual void enterPostfix_op(PSParser::Postfix_opContext * /*ctx*/) override { }
  virtual void exitPostfix_op(PSParser::Postfix_opContext * /*ctx*/) override { }

  virtual void enterEval_at(PSParser::Eval_atContext * /*ctx*/) override { }
  virtual void exitEval_at(PSParser::Eval_atContext * /*ctx*/) override { }

  virtual void enterEval_at_sub(PSParser::Eval_at_subContext * /*ctx*/) override { }
  virtual void exitEval_at_sub(PSParser::Eval_at_subContext * /*ctx*/) override { }

  virtual void enterEval_at_sup(PSParser::Eval_at_supContext * /*ctx*/) override { }
  virtual void exitEval_at_sup(PSParser::Eval_at_supContext * /*ctx*/) override { }

  virtual void enterExp(PSParser::ExpContext * /*ctx*/) override { }
  virtual void exitExp(PSParser::ExpContext * /*ctx*/) override { }

  virtual void enterExp_nofunc(PSParser::Exp_nofuncContext * /*ctx*/) override { }
  virtual void exitExp_nofunc(PSParser::Exp_nofuncContext * /*ctx*/) override { }

  virtual void enterComp(PSParser::CompContext * /*ctx*/) override { }
  virtual void exitComp(PSParser::CompContext * /*ctx*/) override { }

  virtual void enterComp_nofunc(PSParser::Comp_nofuncContext * /*ctx*/) override { }
  virtual void exitComp_nofunc(PSParser::Comp_nofuncContext * /*ctx*/) override { }

  virtual void enterGroup(PSParser::GroupContext * /*ctx*/) override { }
  virtual void exitGroup(PSParser::GroupContext * /*ctx*/) override { }

  virtual void enterAbs_group(PSParser::Abs_groupContext * /*ctx*/) override { }
  virtual void exitAbs_group(PSParser::Abs_groupContext * /*ctx*/) override { }

  virtual void enterFloor_group(PSParser::Floor_groupContext * /*ctx*/) override { }
  virtual void exitFloor_group(PSParser::Floor_groupContext * /*ctx*/) override { }

  virtual void enterCeil_group(PSParser::Ceil_groupContext * /*ctx*/) override { }
  virtual void exitCeil_group(PSParser::Ceil_groupContext * /*ctx*/) override { }

  virtual void enterAccent(PSParser::AccentContext * /*ctx*/) override { }
  virtual void exitAccent(PSParser::AccentContext * /*ctx*/) override { }

  virtual void enterAtom_expr(PSParser::Atom_exprContext * /*ctx*/) override { }
  virtual void exitAtom_expr(PSParser::Atom_exprContext * /*ctx*/) override { }

  virtual void enterAtom(PSParser::AtomContext * /*ctx*/) override { }
  virtual void exitAtom(PSParser::AtomContext * /*ctx*/) override { }

  virtual void enterMathit(PSParser::MathitContext * /*ctx*/) override { }
  virtual void exitMathit(PSParser::MathitContext * /*ctx*/) override { }

  virtual void enterMathit_text(PSParser::Mathit_textContext * /*ctx*/) override { }
  virtual void exitMathit_text(PSParser::Mathit_textContext * /*ctx*/) override { }

  virtual void enterFrac(PSParser::FracContext * /*ctx*/) override { }
  virtual void exitFrac(PSParser::FracContext * /*ctx*/) override { }

  virtual void enterBinom(PSParser::BinomContext * /*ctx*/) override { }
  virtual void exitBinom(PSParser::BinomContext * /*ctx*/) override { }

  virtual void enterFunc_normal_functions_single_arg(PSParser::Func_normal_functions_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_functions_single_arg(PSParser::Func_normal_functions_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_functions_multi_arg(PSParser::Func_normal_functions_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_functions_multi_arg(PSParser::Func_normal_functions_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_operator_names_single_arg(PSParser::Func_operator_names_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_operator_names_single_arg(PSParser::Func_operator_names_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_operator_names_multi_arg(PSParser::Func_operator_names_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_operator_names_multi_arg(PSParser::Func_operator_names_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_single_arg(PSParser::Func_normal_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_single_arg(PSParser::Func_normal_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_normal_multi_arg(PSParser::Func_normal_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_normal_multi_arg(PSParser::Func_normal_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc(PSParser::FuncContext * /*ctx*/) override { }
  virtual void exitFunc(PSParser::FuncContext * /*ctx*/) override { }

  virtual void enterArgs(PSParser::ArgsContext * /*ctx*/) override { }
  virtual void exitArgs(PSParser::ArgsContext * /*ctx*/) override { }

  virtual void enterLimit_sub(PSParser::Limit_subContext * /*ctx*/) override { }
  virtual void exitLimit_sub(PSParser::Limit_subContext * /*ctx*/) override { }

  virtual void enterFunc_single_arg(PSParser::Func_single_argContext * /*ctx*/) override { }
  virtual void exitFunc_single_arg(PSParser::Func_single_argContext * /*ctx*/) override { }

  virtual void enterFunc_single_arg_noparens(PSParser::Func_single_arg_noparensContext * /*ctx*/) override { }
  virtual void exitFunc_single_arg_noparens(PSParser::Func_single_arg_noparensContext * /*ctx*/) override { }

  virtual void enterFunc_multi_arg(PSParser::Func_multi_argContext * /*ctx*/) override { }
  virtual void exitFunc_multi_arg(PSParser::Func_multi_argContext * /*ctx*/) override { }

  virtual void enterFunc_multi_arg_noparens(PSParser::Func_multi_arg_noparensContext * /*ctx*/) override { }
  virtual void exitFunc_multi_arg_noparens(PSParser::Func_multi_arg_noparensContext * /*ctx*/) override { }

  virtual void enterSubexpr(PSParser::SubexprContext * /*ctx*/) override { }
  virtual void exitSubexpr(PSParser::SubexprContext * /*ctx*/) override { }

  virtual void enterSupexpr(PSParser::SupexprContext * /*ctx*/) override { }
  virtual void exitSupexpr(PSParser::SupexprContext * /*ctx*/) override { }

  virtual void enterSubeq(PSParser::SubeqContext * /*ctx*/) override { }
  virtual void exitSubeq(PSParser::SubeqContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

}  // namespace latex2sympy
