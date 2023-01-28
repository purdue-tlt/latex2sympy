
// Generated from LATEX.g4 by ANTLR 4.11.1

#pragma once


#include "antlr4-runtime.h"


namespace latex2antlr {


class  LATEXLexer : public antlr4::Lexer {
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

  explicit LATEXLexer(antlr4::CharStream *input);

  ~LATEXLexer() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

};

}  // namespace latex2antlr
