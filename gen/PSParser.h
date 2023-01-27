
// Generated from PS.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"


namespace latex2sympy {


class  PSParser : public antlr4::Parser {
public:
  enum {
    WS = 1, DOLLAR_SIGN = 2, ADD = 3, SUB = 4, MUL = 5, DIV = 6, L_PAREN = 7, 
    R_PAREN = 8, L_GROUP = 9, R_GROUP = 10, L_BRACE = 11, R_BRACE = 12, 
    L_BRACE_VISUAL = 13, R_BRACE_VISUAL = 14, L_BRACE_CMD = 15, R_BRACE_CMD = 16, 
    L_BRACKET = 17, R_BRACKET = 18, L_BRACK = 19, R_BRACK = 20, BAR = 21, 
    L_VERT = 22, R_VERT = 23, VERT = 24, L_FLOOR = 25, R_FLOOR = 26, LL_CORNER = 27, 
    LR_CORNER = 28, L_CEIL = 29, R_CEIL = 30, UL_CORNER = 31, UR_CORNER = 32, 
    L_LEFT = 33, R_RIGHT = 34, ML_LEFT = 35, MR_RIGHT = 36, FUNC_LIM = 37, 
    LIM_APPROACH_SYM = 38, FUNC_INT = 39, FUNC_SUM = 40, FUNC_PROD = 41, 
    FUNC_LOG = 42, FUNC_LN = 43, FUNC_EXP = 44, FUNC_SIN = 45, FUNC_COS = 46, 
    FUNC_TAN = 47, FUNC_CSC = 48, FUNC_SEC = 49, FUNC_COT = 50, FUNC_ARCSIN = 51, 
    FUNC_ARCCOS = 52, FUNC_ARCTAN = 53, FUNC_ARCCSC = 54, FUNC_ARCSEC = 55, 
    FUNC_ARCCOT = 56, FUNC_SINH = 57, FUNC_COSH = 58, FUNC_TANH = 59, FUNC_ARSINH = 60, 
    FUNC_ARCOSH = 61, FUNC_ARTANH = 62, FUNC_ARCSINH = 63, FUNC_ARCCOSH = 64, 
    FUNC_ARCTANH = 65, FUNC_ARSINH_NAME = 66, FUNC_ARCSINH_NAME = 67, FUNC_ARCOSH_NAME = 68, 
    FUNC_ARCCOSH_NAME = 69, FUNC_ARTANH_NAME = 70, FUNC_ARCTANH_NAME = 71, 
    FUNC_GCD_NAME = 72, FUNC_LCM_NAME = 73, FUNC_FLOOR_NAME = 74, FUNC_CEIL_NAME = 75, 
    FUNC_SQRT = 76, FUNC_GCD = 77, FUNC_LCM = 78, FUNC_FLOOR = 79, FUNC_CEIL = 80, 
    FUNC_MAX = 81, FUNC_MIN = 82, CMD_TIMES = 83, CMD_CDOT = 84, CMD_DIV = 85, 
    CMD_FRAC = 86, CMD_BINOM = 87, CMD_CHOOSE = 88, CMD_MOD = 89, CMD_MATHIT = 90, 
    CMD_OPERATORNAME = 91, MATRIX_TYPE_MATRIX = 92, MATRIX_TYPE_PMATRIX = 93, 
    MATRIX_TYPE_BMATRIX = 94, MATRIX_TYPES = 95, CMD_MATRIX_START = 96, 
    CMD_MATRIX_END = 97, MATRIX_DEL_COL = 98, MATRIX_DEL_ROW = 99, ACCENT_OVERLINE = 100, 
    ACCENT_BAR = 101, UNDERSCORE = 102, CARET = 103, COLON = 104, SEMICOLON = 105, 
    COMMA = 106, PERIOD = 107, DIFFERENTIAL = 108, EXP_E = 109, E_NOTATION_E = 110, 
    LETTER_NO_E = 111, NUMBER = 112, FRACTION_NUMBER = 113, SCI_NOTATION_NUMBER = 114, 
    E_NOTATION = 115, EQUAL = 116, LT = 117, LTE = 118, GT = 119, GTE = 120, 
    UNEQUAL = 121, BANG = 122, PERCENT_NUMBER = 123, GREEK_CMD = 124, SYMBOL = 125, 
    VARIABLE = 126
  };

  enum {
    RuleAccent_symbol = 0, RuleMath = 1, RuleMatrix = 2, RuleMatrix_row = 3, 
    RuleRelation = 4, RuleRelation_list = 5, RuleRelation_list_content = 6, 
    RuleEquality = 7, RuleExpr = 8, RuleAdditive = 9, RuleMp = 10, RuleMp_nofunc = 11, 
    RuleUnary = 12, RuleUnary_nofunc = 13, RulePostfix = 14, RulePostfix_nofunc = 15, 
    RulePostfix_op = 16, RuleEval_at = 17, RuleEval_at_sub = 18, RuleEval_at_sup = 19, 
    RuleExp = 20, RuleExp_nofunc = 21, RuleComp = 22, RuleComp_nofunc = 23, 
    RuleGroup = 24, RuleAbs_group = 25, RuleFloor_group = 26, RuleCeil_group = 27, 
    RuleAccent = 28, RuleAtom_expr = 29, RuleAtom = 30, RuleMathit = 31, 
    RuleMathit_text = 32, RuleFrac = 33, RuleBinom = 34, RuleFunc_normal_functions_single_arg = 35, 
    RuleFunc_normal_functions_multi_arg = 36, RuleFunc_operator_names_single_arg = 37, 
    RuleFunc_operator_names_multi_arg = 38, RuleFunc_normal_single_arg = 39, 
    RuleFunc_normal_multi_arg = 40, RuleFunc = 41, RuleArgs = 42, RuleLimit_sub = 43, 
    RuleFunc_single_arg = 44, RuleFunc_single_arg_noparens = 45, RuleFunc_multi_arg = 46, 
    RuleFunc_multi_arg_noparens = 47, RuleSubexpr = 48, RuleSupexpr = 49, 
    RuleSubeq = 50
  };

  explicit PSParser(antlr4::TokenStream *input);

  PSParser(antlr4::TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options);

  ~PSParser() override;

  std::string getGrammarFileName() const override;

  const antlr4::atn::ATN& getATN() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;


  class Accent_symbolContext;
  class MathContext;
  class MatrixContext;
  class Matrix_rowContext;
  class RelationContext;
  class Relation_listContext;
  class Relation_list_contentContext;
  class EqualityContext;
  class ExprContext;
  class AdditiveContext;
  class MpContext;
  class Mp_nofuncContext;
  class UnaryContext;
  class Unary_nofuncContext;
  class PostfixContext;
  class Postfix_nofuncContext;
  class Postfix_opContext;
  class Eval_atContext;
  class Eval_at_subContext;
  class Eval_at_supContext;
  class ExpContext;
  class Exp_nofuncContext;
  class CompContext;
  class Comp_nofuncContext;
  class GroupContext;
  class Abs_groupContext;
  class Floor_groupContext;
  class Ceil_groupContext;
  class AccentContext;
  class Atom_exprContext;
  class AtomContext;
  class MathitContext;
  class Mathit_textContext;
  class FracContext;
  class BinomContext;
  class Func_normal_functions_single_argContext;
  class Func_normal_functions_multi_argContext;
  class Func_operator_names_single_argContext;
  class Func_operator_names_multi_argContext;
  class Func_normal_single_argContext;
  class Func_normal_multi_argContext;
  class FuncContext;
  class ArgsContext;
  class Limit_subContext;
  class Func_single_argContext;
  class Func_single_arg_noparensContext;
  class Func_multi_argContext;
  class Func_multi_arg_noparensContext;
  class SubexprContext;
  class SupexprContext;
  class SubeqContext; 

  class  Accent_symbolContext : public antlr4::ParserRuleContext {
  public:
    Accent_symbolContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ACCENT_BAR();
    antlr4::tree::TerminalNode *ACCENT_OVERLINE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Accent_symbolContext* accent_symbol();

  class  MathContext : public antlr4::ParserRuleContext {
  public:
    MathContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    RelationContext *relation();
    Relation_listContext *relation_list();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  MathContext* math();

  class  MatrixContext : public antlr4::ParserRuleContext {
  public:
    MatrixContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CMD_MATRIX_START();
    std::vector<Matrix_rowContext *> matrix_row();
    Matrix_rowContext* matrix_row(size_t i);
    antlr4::tree::TerminalNode *CMD_MATRIX_END();
    std::vector<antlr4::tree::TerminalNode *> MATRIX_DEL_ROW();
    antlr4::tree::TerminalNode* MATRIX_DEL_ROW(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  MatrixContext* matrix();

  class  Matrix_rowContext : public antlr4::ParserRuleContext {
  public:
    Matrix_rowContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MATRIX_DEL_COL();
    antlr4::tree::TerminalNode* MATRIX_DEL_COL(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Matrix_rowContext* matrix_row();

  class  RelationContext : public antlr4::ParserRuleContext {
  public:
    RelationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExprContext *expr();
    std::vector<RelationContext *> relation();
    RelationContext* relation(size_t i);
    antlr4::tree::TerminalNode *EQUAL();
    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *LTE();
    antlr4::tree::TerminalNode *GT();
    antlr4::tree::TerminalNode *GTE();
    antlr4::tree::TerminalNode *UNEQUAL();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  RelationContext* relation();
  RelationContext* relation(int precedence);
  class  Relation_listContext : public antlr4::ParserRuleContext {
  public:
    Relation_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Relation_list_contentContext *relation_list_content();
    antlr4::tree::TerminalNode *L_PAREN();
    antlr4::tree::TerminalNode *R_PAREN();
    antlr4::tree::TerminalNode *L_GROUP();
    antlr4::tree::TerminalNode *R_GROUP();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    antlr4::tree::TerminalNode *L_BRACE_VISUAL();
    antlr4::tree::TerminalNode *R_BRACE_VISUAL();
    antlr4::tree::TerminalNode *L_BRACE_CMD();
    antlr4::tree::TerminalNode *R_BRACE_CMD();
    antlr4::tree::TerminalNode *L_BRACKET();
    antlr4::tree::TerminalNode *R_BRACKET();
    antlr4::tree::TerminalNode *L_BRACK();
    antlr4::tree::TerminalNode *R_BRACK();
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Relation_listContext* relation_list();

  class  Relation_list_contentContext : public antlr4::ParserRuleContext {
  public:
    Relation_list_contentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<RelationContext *> relation();
    RelationContext* relation(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SEMICOLON();
    antlr4::tree::TerminalNode* SEMICOLON(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Relation_list_contentContext* relation_list_content();

  class  EqualityContext : public antlr4::ParserRuleContext {
  public:
    EqualityContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);
    antlr4::tree::TerminalNode *EQUAL();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  EqualityContext* equality();

  class  ExprContext : public antlr4::ParserRuleContext {
  public:
    ExprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AdditiveContext *additive();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  ExprContext* expr();

  class  AdditiveContext : public antlr4::ParserRuleContext {
  public:
    AdditiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    MpContext *mp();
    std::vector<AdditiveContext *> additive();
    AdditiveContext* additive(size_t i);
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  AdditiveContext* additive();
  AdditiveContext* additive(int precedence);
  class  MpContext : public antlr4::ParserRuleContext {
  public:
    MpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnaryContext *unary();
    std::vector<MpContext *> mp();
    MpContext* mp(size_t i);
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *CMD_TIMES();
    antlr4::tree::TerminalNode *CMD_CDOT();
    antlr4::tree::TerminalNode *DIV();
    antlr4::tree::TerminalNode *CMD_DIV();
    antlr4::tree::TerminalNode *COLON();
    antlr4::tree::TerminalNode *CMD_MOD();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  MpContext* mp();
  MpContext* mp(int precedence);
  class  Mp_nofuncContext : public antlr4::ParserRuleContext {
  public:
    Mp_nofuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Unary_nofuncContext *unary_nofunc();
    std::vector<Mp_nofuncContext *> mp_nofunc();
    Mp_nofuncContext* mp_nofunc(size_t i);
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *CMD_TIMES();
    antlr4::tree::TerminalNode *CMD_CDOT();
    antlr4::tree::TerminalNode *DIV();
    antlr4::tree::TerminalNode *CMD_DIV();
    antlr4::tree::TerminalNode *COLON();
    antlr4::tree::TerminalNode *CMD_MOD();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Mp_nofuncContext* mp_nofunc();
  Mp_nofuncContext* mp_nofunc(int precedence);
  class  UnaryContext : public antlr4::ParserRuleContext {
  public:
    UnaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    UnaryContext *unary();
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();
    std::vector<PostfixContext *> postfix();
    PostfixContext* postfix(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  UnaryContext* unary();

  class  Unary_nofuncContext : public antlr4::ParserRuleContext {
  public:
    Unary_nofuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Unary_nofuncContext *unary_nofunc();
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();
    PostfixContext *postfix();
    std::vector<Postfix_nofuncContext *> postfix_nofunc();
    Postfix_nofuncContext* postfix_nofunc(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Unary_nofuncContext* unary_nofunc();

  class  PostfixContext : public antlr4::ParserRuleContext {
  public:
    PostfixContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpContext *exp();
    std::vector<Postfix_opContext *> postfix_op();
    Postfix_opContext* postfix_op(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  PostfixContext* postfix();

  class  Postfix_nofuncContext : public antlr4::ParserRuleContext {
  public:
    Postfix_nofuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Exp_nofuncContext *exp_nofunc();
    std::vector<Postfix_opContext *> postfix_op();
    Postfix_opContext* postfix_op(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Postfix_nofuncContext* postfix_nofunc();

  class  Postfix_opContext : public antlr4::ParserRuleContext {
  public:
    Postfix_opContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BANG();
    Eval_atContext *eval_at();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Postfix_opContext* postfix_op();

  class  Eval_atContext : public antlr4::ParserRuleContext {
  public:
    Eval_atContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BAR();
    Eval_at_supContext *eval_at_sup();
    Eval_at_subContext *eval_at_sub();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Eval_atContext* eval_at();

  class  Eval_at_subContext : public antlr4::ParserRuleContext {
  public:
    Eval_at_subContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDERSCORE();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    ExprContext *expr();
    EqualityContext *equality();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Eval_at_subContext* eval_at_sub();

  class  Eval_at_supContext : public antlr4::ParserRuleContext {
  public:
    Eval_at_supContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CARET();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    ExprContext *expr();
    EqualityContext *equality();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Eval_at_supContext* eval_at_sup();

  class  ExpContext : public antlr4::ParserRuleContext {
  public:
    ExpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    CompContext *comp();
    ExpContext *exp();
    antlr4::tree::TerminalNode *CARET();
    AtomContext *atom();
    antlr4::tree::TerminalNode *L_BRACE();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_BRACE();
    SubexprContext *subexpr();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  ExpContext* exp();
  ExpContext* exp(int precedence);
  class  Exp_nofuncContext : public antlr4::ParserRuleContext {
  public:
    Exp_nofuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Comp_nofuncContext *comp_nofunc();
    Exp_nofuncContext *exp_nofunc();
    antlr4::tree::TerminalNode *CARET();
    AtomContext *atom();
    antlr4::tree::TerminalNode *L_BRACE();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_BRACE();
    SubexprContext *subexpr();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Exp_nofuncContext* exp_nofunc();
  Exp_nofuncContext* exp_nofunc(int precedence);
  class  CompContext : public antlr4::ParserRuleContext {
  public:
    CompContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    GroupContext *group();
    Abs_groupContext *abs_group();
    Floor_groupContext *floor_group();
    Ceil_groupContext *ceil_group();
    FuncContext *func();
    AtomContext *atom();
    FracContext *frac();
    BinomContext *binom();
    MatrixContext *matrix();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  CompContext* comp();

  class  Comp_nofuncContext : public antlr4::ParserRuleContext {
  public:
    Comp_nofuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    GroupContext *group();
    Abs_groupContext *abs_group();
    Floor_groupContext *floor_group();
    Ceil_groupContext *ceil_group();
    AtomContext *atom();
    FracContext *frac();
    BinomContext *binom();
    MatrixContext *matrix();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Comp_nofuncContext* comp_nofunc();

  class  GroupContext : public antlr4::ParserRuleContext {
  public:
    GroupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *L_PAREN();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_PAREN();
    antlr4::tree::TerminalNode *L_GROUP();
    antlr4::tree::TerminalNode *R_GROUP();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    antlr4::tree::TerminalNode *L_BRACE_VISUAL();
    antlr4::tree::TerminalNode *R_BRACE_VISUAL();
    antlr4::tree::TerminalNode *L_BRACE_CMD();
    antlr4::tree::TerminalNode *R_BRACE_CMD();
    antlr4::tree::TerminalNode *L_BRACKET();
    antlr4::tree::TerminalNode *R_BRACKET();
    antlr4::tree::TerminalNode *L_BRACK();
    antlr4::tree::TerminalNode *R_BRACK();
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  GroupContext* group();

  class  Abs_groupContext : public antlr4::ParserRuleContext {
  public:
    Abs_groupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> BAR();
    antlr4::tree::TerminalNode* BAR(size_t i);
    ExprContext *expr();
    antlr4::tree::TerminalNode *L_VERT();
    antlr4::tree::TerminalNode *R_VERT();
    std::vector<antlr4::tree::TerminalNode *> VERT();
    antlr4::tree::TerminalNode* VERT(size_t i);
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Abs_groupContext* abs_group();

  class  Floor_groupContext : public antlr4::ParserRuleContext {
  public:
    Floor_groupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *L_FLOOR();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_FLOOR();
    antlr4::tree::TerminalNode *LL_CORNER();
    antlr4::tree::TerminalNode *LR_CORNER();
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Floor_groupContext* floor_group();

  class  Ceil_groupContext : public antlr4::ParserRuleContext {
  public:
    Ceil_groupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *L_CEIL();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_CEIL();
    antlr4::tree::TerminalNode *UL_CORNER();
    antlr4::tree::TerminalNode *UR_CORNER();
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Ceil_groupContext* ceil_group();

  class  AccentContext : public antlr4::ParserRuleContext {
  public:
    PSParser::ExprContext *base = nullptr;
    AccentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Accent_symbolContext *accent_symbol();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    ExprContext *expr();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  AccentContext* accent();

  class  Atom_exprContext : public antlr4::ParserRuleContext {
  public:
    Atom_exprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LETTER_NO_E();
    antlr4::tree::TerminalNode *GREEK_CMD();
    AccentContext *accent();
    SupexprContext *supexpr();
    SubexprContext *subexpr();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Atom_exprContext* atom_expr();

  class  AtomContext : public antlr4::ParserRuleContext {
  public:
    AtomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Atom_exprContext *atom_expr();
    antlr4::tree::TerminalNode *SYMBOL();
    antlr4::tree::TerminalNode *NUMBER();
    antlr4::tree::TerminalNode *SCI_NOTATION_NUMBER();
    antlr4::tree::TerminalNode *FRACTION_NUMBER();
    antlr4::tree::TerminalNode *PERCENT_NUMBER();
    antlr4::tree::TerminalNode *E_NOTATION();
    antlr4::tree::TerminalNode *DIFFERENTIAL();
    MathitContext *mathit();
    antlr4::tree::TerminalNode *VARIABLE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  AtomContext* atom();

  class  MathitContext : public antlr4::ParserRuleContext {
  public:
    MathitContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CMD_MATHIT();
    antlr4::tree::TerminalNode *L_BRACE();
    Mathit_textContext *mathit_text();
    antlr4::tree::TerminalNode *R_BRACE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  MathitContext* mathit();

  class  Mathit_textContext : public antlr4::ParserRuleContext {
  public:
    Mathit_textContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> LETTER_NO_E();
    antlr4::tree::TerminalNode* LETTER_NO_E(size_t i);
    std::vector<antlr4::tree::TerminalNode *> E_NOTATION_E();
    antlr4::tree::TerminalNode* E_NOTATION_E(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EXP_E();
    antlr4::tree::TerminalNode* EXP_E(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Mathit_textContext* mathit_text();

  class  FracContext : public antlr4::ParserRuleContext {
  public:
    PSParser::ExprContext *upper = nullptr;
    PSParser::ExprContext *lower = nullptr;
    FracContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CMD_FRAC();
    std::vector<antlr4::tree::TerminalNode *> L_BRACE();
    antlr4::tree::TerminalNode* L_BRACE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> R_BRACE();
    antlr4::tree::TerminalNode* R_BRACE(size_t i);
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  FracContext* frac();

  class  BinomContext : public antlr4::ParserRuleContext {
  public:
    PSParser::ExprContext *upper = nullptr;
    PSParser::ExprContext *lower = nullptr;
    BinomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> L_BRACE();
    antlr4::tree::TerminalNode* L_BRACE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> R_BRACE();
    antlr4::tree::TerminalNode* R_BRACE(size_t i);
    antlr4::tree::TerminalNode *CMD_BINOM();
    antlr4::tree::TerminalNode *CMD_CHOOSE();
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  BinomContext* binom();

  class  Func_normal_functions_single_argContext : public antlr4::ParserRuleContext {
  public:
    Func_normal_functions_single_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FUNC_LOG();
    antlr4::tree::TerminalNode *FUNC_LN();
    antlr4::tree::TerminalNode *FUNC_EXP();
    antlr4::tree::TerminalNode *FUNC_SIN();
    antlr4::tree::TerminalNode *FUNC_COS();
    antlr4::tree::TerminalNode *FUNC_TAN();
    antlr4::tree::TerminalNode *FUNC_CSC();
    antlr4::tree::TerminalNode *FUNC_SEC();
    antlr4::tree::TerminalNode *FUNC_COT();
    antlr4::tree::TerminalNode *FUNC_ARCSIN();
    antlr4::tree::TerminalNode *FUNC_ARCCOS();
    antlr4::tree::TerminalNode *FUNC_ARCTAN();
    antlr4::tree::TerminalNode *FUNC_ARCCSC();
    antlr4::tree::TerminalNode *FUNC_ARCSEC();
    antlr4::tree::TerminalNode *FUNC_ARCCOT();
    antlr4::tree::TerminalNode *FUNC_SINH();
    antlr4::tree::TerminalNode *FUNC_COSH();
    antlr4::tree::TerminalNode *FUNC_TANH();
    antlr4::tree::TerminalNode *FUNC_ARSINH();
    antlr4::tree::TerminalNode *FUNC_ARCOSH();
    antlr4::tree::TerminalNode *FUNC_ARTANH();
    antlr4::tree::TerminalNode *FUNC_ARCSINH();
    antlr4::tree::TerminalNode *FUNC_ARCCOSH();
    antlr4::tree::TerminalNode *FUNC_ARCTANH();
    antlr4::tree::TerminalNode *FUNC_FLOOR();
    antlr4::tree::TerminalNode *FUNC_CEIL();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_normal_functions_single_argContext* func_normal_functions_single_arg();

  class  Func_normal_functions_multi_argContext : public antlr4::ParserRuleContext {
  public:
    Func_normal_functions_multi_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FUNC_GCD();
    antlr4::tree::TerminalNode *FUNC_LCM();
    antlr4::tree::TerminalNode *FUNC_MAX();
    antlr4::tree::TerminalNode *FUNC_MIN();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_normal_functions_multi_argContext* func_normal_functions_multi_arg();

  class  Func_operator_names_single_argContext : public antlr4::ParserRuleContext {
  public:
    Func_operator_names_single_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FUNC_ARSINH_NAME();
    antlr4::tree::TerminalNode *FUNC_ARCOSH_NAME();
    antlr4::tree::TerminalNode *FUNC_ARTANH_NAME();
    antlr4::tree::TerminalNode *FUNC_ARCSINH_NAME();
    antlr4::tree::TerminalNode *FUNC_ARCCOSH_NAME();
    antlr4::tree::TerminalNode *FUNC_ARCTANH_NAME();
    antlr4::tree::TerminalNode *FUNC_FLOOR_NAME();
    antlr4::tree::TerminalNode *FUNC_CEIL_NAME();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_operator_names_single_argContext* func_operator_names_single_arg();

  class  Func_operator_names_multi_argContext : public antlr4::ParserRuleContext {
  public:
    Func_operator_names_multi_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FUNC_GCD_NAME();
    antlr4::tree::TerminalNode *FUNC_LCM_NAME();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_operator_names_multi_argContext* func_operator_names_multi_arg();

  class  Func_normal_single_argContext : public antlr4::ParserRuleContext {
  public:
    PSParser::Func_operator_names_single_argContext *func_operator_name = nullptr;
    Func_normal_single_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Func_normal_functions_single_argContext *func_normal_functions_single_arg();
    antlr4::tree::TerminalNode *CMD_OPERATORNAME();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    Func_operator_names_single_argContext *func_operator_names_single_arg();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_normal_single_argContext* func_normal_single_arg();

  class  Func_normal_multi_argContext : public antlr4::ParserRuleContext {
  public:
    PSParser::Func_operator_names_multi_argContext *func_operator_name = nullptr;
    Func_normal_multi_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Func_normal_functions_multi_argContext *func_normal_functions_multi_arg();
    antlr4::tree::TerminalNode *CMD_OPERATORNAME();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    Func_operator_names_multi_argContext *func_operator_names_multi_arg();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_normal_multi_argContext* func_normal_multi_arg();

  class  FuncContext : public antlr4::ParserRuleContext {
  public:
    PSParser::ExprContext *root = nullptr;
    PSParser::ExprContext *base = nullptr;
    FuncContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Func_normal_single_argContext *func_normal_single_arg();
    antlr4::tree::TerminalNode *L_PAREN();
    Func_single_argContext *func_single_arg();
    antlr4::tree::TerminalNode *R_PAREN();
    Func_single_arg_noparensContext *func_single_arg_noparens();
    SubexprContext *subexpr();
    SupexprContext *supexpr();
    antlr4::tree::TerminalNode *L_LEFT();
    antlr4::tree::TerminalNode *R_RIGHT();
    antlr4::tree::TerminalNode *ML_LEFT();
    antlr4::tree::TerminalNode *MR_RIGHT();
    Func_normal_multi_argContext *func_normal_multi_arg();
    Func_multi_argContext *func_multi_arg();
    Func_multi_arg_noparensContext *func_multi_arg_noparens();
    antlr4::tree::TerminalNode *FUNC_INT();
    antlr4::tree::TerminalNode *DIFFERENTIAL();
    FracContext *frac();
    AdditiveContext *additive();
    antlr4::tree::TerminalNode *UNDERSCORE();
    std::vector<antlr4::tree::TerminalNode *> L_BRACE();
    antlr4::tree::TerminalNode* L_BRACE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> R_BRACE();
    antlr4::tree::TerminalNode* R_BRACE(size_t i);
    antlr4::tree::TerminalNode *CARET();
    antlr4::tree::TerminalNode *FUNC_SQRT();
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);
    antlr4::tree::TerminalNode *L_BRACKET();
    antlr4::tree::TerminalNode *R_BRACKET();
    MpContext *mp();
    antlr4::tree::TerminalNode *FUNC_SUM();
    antlr4::tree::TerminalNode *FUNC_PROD();
    SubeqContext *subeq();
    antlr4::tree::TerminalNode *FUNC_LIM();
    Limit_subContext *limit_sub();
    antlr4::tree::TerminalNode *EXP_E();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  FuncContext* func();

  class  ArgsContext : public antlr4::ParserRuleContext {
  public:
    ArgsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExprContext *expr();
    antlr4::tree::TerminalNode *COMMA();
    ArgsContext *args();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  ArgsContext* args();

  class  Limit_subContext : public antlr4::ParserRuleContext {
  public:
    Limit_subContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDERSCORE();
    std::vector<antlr4::tree::TerminalNode *> L_BRACE();
    antlr4::tree::TerminalNode* L_BRACE(size_t i);
    antlr4::tree::TerminalNode *LIM_APPROACH_SYM();
    ExprContext *expr();
    std::vector<antlr4::tree::TerminalNode *> R_BRACE();
    antlr4::tree::TerminalNode* R_BRACE(size_t i);
    antlr4::tree::TerminalNode *LETTER_NO_E();
    antlr4::tree::TerminalNode *GREEK_CMD();
    antlr4::tree::TerminalNode *CARET();
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *SUB();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Limit_subContext* limit_sub();

  class  Func_single_argContext : public antlr4::ParserRuleContext {
  public:
    Func_single_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExprContext *expr();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_single_argContext* func_single_arg();

  class  Func_single_arg_noparensContext : public antlr4::ParserRuleContext {
  public:
    Func_single_arg_noparensContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Mp_nofuncContext *mp_nofunc();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_single_arg_noparensContext* func_single_arg_noparens();

  class  Func_multi_argContext : public antlr4::ParserRuleContext {
  public:
    Func_multi_argContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExprContext *expr();
    antlr4::tree::TerminalNode *COMMA();
    Func_multi_argContext *func_multi_arg();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_multi_argContext* func_multi_arg();

  class  Func_multi_arg_noparensContext : public antlr4::ParserRuleContext {
  public:
    Func_multi_arg_noparensContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Mp_nofuncContext *mp_nofunc();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  Func_multi_arg_noparensContext* func_multi_arg_noparens();

  class  SubexprContext : public antlr4::ParserRuleContext {
  public:
    SubexprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDERSCORE();
    AtomContext *atom();
    antlr4::tree::TerminalNode *L_BRACE();
    antlr4::tree::TerminalNode *R_BRACE();
    ExprContext *expr();
    ArgsContext *args();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  SubexprContext* subexpr();

  class  SupexprContext : public antlr4::ParserRuleContext {
  public:
    SupexprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CARET();
    AtomContext *atom();
    antlr4::tree::TerminalNode *L_BRACE();
    ExprContext *expr();
    antlr4::tree::TerminalNode *R_BRACE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  SupexprContext* supexpr();

  class  SubeqContext : public antlr4::ParserRuleContext {
  public:
    SubeqContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDERSCORE();
    antlr4::tree::TerminalNode *L_BRACE();
    EqualityContext *equality();
    antlr4::tree::TerminalNode *R_BRACE();

    virtual void enterRule(antlr4::tree::ParseTreeListener *listener) override;
    virtual void exitRule(antlr4::tree::ParseTreeListener *listener) override;
   
  };

  SubeqContext* subeq();


  bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;

  bool relationSempred(RelationContext *_localctx, size_t predicateIndex);
  bool additiveSempred(AdditiveContext *_localctx, size_t predicateIndex);
  bool mpSempred(MpContext *_localctx, size_t predicateIndex);
  bool mp_nofuncSempred(Mp_nofuncContext *_localctx, size_t predicateIndex);
  bool expSempred(ExpContext *_localctx, size_t predicateIndex);
  bool exp_nofuncSempred(Exp_nofuncContext *_localctx, size_t predicateIndex);

  // By default the static state used to implement the parser is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:
};

}  // namespace latex2sympy
