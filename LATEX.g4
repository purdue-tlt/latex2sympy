grammar LATEX;

WS: [ \t\r\n]+ -> skip;
DOLLAR_SIGN: '\\$' -> skip;

UNDERSCORE: '_';
CARET: '^';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
PERIOD: '.';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
EQUAL: '=';
LT: '<';
LTE: '\\leq' | '\\le';
GT: '>';
GTE: '\\geq' | '\\ge';
UNEQUAL: '!=' | '\\ne' | '\\neq';
BANG: '!';

L_PAREN: '(';
R_PAREN: ')';
L_GROUP: '\\lgroup';
R_GROUP: '\\rgroup';
L_BRACE: '{';
R_BRACE: '}';
L_BRACE_VISUAL: '\\{';
R_BRACE_VISUAL: '\\}';
L_BRACE_CMD: '\\lbrace';
R_BRACE_CMD: '\\rbrace';
L_BRACKET: '[';
R_BRACKET: ']';
L_BRACK: '\\lbrack';
R_BRACK: '\\rbrack';

BAR: '|';
L_VERT: '\\lvert';
R_VERT: '\\rvert';
VERT: '\\vert';

L_FLOOR: '\\lfloor';
R_FLOOR: '\\rfloor';
LL_CORNER: '\\llcorner';
LR_CORNER: '\\lrcorner';

L_CEIL: '\\lceil';
R_CEIL: '\\rceil';
UL_CORNER: '\\ulcorner';
UR_CORNER: '\\urcorner';

L_LEFT: '\\left';
R_RIGHT: '\\right';
ML_LEFT: '\\mleft';
MR_RIGHT: '\\mright';

// functions
FUNC_LIM:  '\\lim';
LIM_APPROACH_SYM: '\\to' | '\\rightarrow' | '\\Rightarrow' | '\\longrightarrow' | '\\Longrightarrow';
FUNC_INT:  '\\int';
FUNC_SUM:  '\\sum';
FUNC_PROD: '\\prod';

FUNC_LOG:  '\\log';
FUNC_LN:   '\\ln';
FUNC_EXP: '\\exp';
FUNC_SIN:  '\\sin';
FUNC_COS:  '\\cos';
FUNC_TAN:  '\\tan';
FUNC_CSC:  '\\csc';
FUNC_SEC:  '\\sec';
FUNC_COT:  '\\cot';

FUNC_ARCSIN: '\\arcsin';
FUNC_ARCCOS: '\\arccos';
FUNC_ARCTAN: '\\arctan';
FUNC_ARCCSC: '\\arccsc';
FUNC_ARCSEC: '\\arcsec';
FUNC_ARCCOT: '\\arccot';

FUNC_SINH: '\\sinh';
FUNC_COSH: '\\cosh';
FUNC_TANH: '\\tanh';
FUNC_ARSINH: '\\arsinh';
FUNC_ARCOSH: '\\arcosh';
FUNC_ARTANH: '\\artanh';
FUNC_ARCSINH: '\\arcsinh';
FUNC_ARCCOSH: '\\arccosh';
FUNC_ARCTANH: '\\arctanh';

FUNC_ARSINH_NAME: 'arsinh';
FUNC_ARCSINH_NAME: 'arcsinh';
FUNC_ARCOSH_NAME: 'arcosh';
FUNC_ARCCOSH_NAME: 'arccosh';
FUNC_ARTANH_NAME: 'artanh';
FUNC_ARCTANH_NAME: 'arctanh';
FUNC_GCD_NAME: 'gcd';
FUNC_LCM_NAME: 'lcm';
FUNC_FLOOR_NAME: 'floor';
FUNC_CEIL_NAME: 'ceil';

FUNC_SQRT: '\\sqrt';
FUNC_GCD: '\\gcd';
FUNC_LCM: '\\lcm';
FUNC_FLOOR: '\\floor';
FUNC_CEIL: '\\ceil';
FUNC_MAX: '\\max';
FUNC_MIN: '\\min';

FUNC_RE_NAME: 'Re';
FUNC_IM_NAME: 'Im';
FUNC_ARG_NAME: 'Arg';
FUNC_ABS_NAME: 'Abs';

// commands
CMD_TIMES: '\\times';
CMD_CDOT: '\\cdot';
CMD_DIV: '\\div';
CMD_FRAC: '\\frac';
CMD_BINOM: '\\binom';
CMD_CHOOSE: '\\choose';
CMD_MOD: '\\mod';

CMD_MATHIT: '\\mathit';

CMD_OPERATORNAME: '\\operatorname';

// matrix test
MATRIX_TYPE_MATRIX: 'matrix';
MATRIX_TYPE_PMATRIX: 'pmatrix';
MATRIX_TYPE_BMATRIX: 'bmatrix';
MATRIX_TYPES: MATRIX_TYPE_MATRIX | MATRIX_TYPE_PMATRIX | MATRIX_TYPE_BMATRIX;
CMD_MATRIX_START: '\\begin' L_BRACE MATRIX_TYPES R_BRACE;
CMD_MATRIX_END: '\\end' L_BRACE MATRIX_TYPES R_BRACE;
MATRIX_DEL_COL: '&';
MATRIX_DEL_ROW: '\\\\';

// accents such as overline and hat
ACCENT_OVERLINE: '\\overline';
ACCENT_BAR: '\\bar';

fragment WS_CHAR: [ \t\r\n];
fragment LETTER: [a-zA-Z];
fragment DIGIT: [0-9];

EXP_E: 'e' | '\\exponentialE';
E_NOTATION_E: 'E';
LETTER_NO_E: [a-df-zA-DF-Z]; // exclude e for exponential function and e notation

DIFFERENTIAL: 'd' WS_CHAR*? (LETTER | '\\' LETTER+);

NUMBER:
    DIGIT+ (COMMA DIGIT DIGIT DIGIT)*
    | DIGIT* (COMMA DIGIT DIGIT DIGIT)* PERIOD DIGIT+;

FRACTION_NUMBER: CMD_FRAC L_BRACE
    SUB? NUMBER
    R_BRACE L_BRACE
    SUB? NUMBER
    R_BRACE;

SCI_NOTATION_NUMBER: NUMBER CMD_TIMES ' 10' CARET (DIGIT | L_BRACE SUB? NUMBER R_BRACE);

E_NOTATION: NUMBER E_NOTATION_E (SUB | ADD)? DIGIT+;

fragment PERCENT_SIGN: '\\%';
PERCENT_NUMBER: NUMBER PERCENT_SIGN;

// Excludes some letters for use as e.g. constants in SYMBOL
fragment GREEK_LETTER:
    '\\char"000391' | // Alpha
    '\\alpha' |
    '\\char"000392' | // Beta
    '\\beta' |
    '\\Gamma' |
    '\\gamma' |
    '\\Delta' |
    '\\delta' |
    '\\char"000190' | // Epsilon
    '\\epsilon' |
    '\\varepsilon' |
    '\\char"000396' | // Zeta
    '\\zeta' |
    '\\char"000397' | // Eta
    '\\eta' |
    '\\Theta' |
    '\\theta' |
    '\\vartheta' |
    '\\char"000399' | // Iota
    '\\iota' |
    '\\char"00039A' | // Kappa
    '\\kappa' |
    '\\Lambda' |
    '\\lambda' |
    '\\char"00039C' | // Mu
    '\\mu' |
    '\\char"00039D' | // Nu
    '\\nu' |
    '\\Xi' |
    '\\xi' |
    '\\char"00039F' | // Omicron
    '\\omicron' |
    '\\Pi' |
    '\\varpi' |
    '\\char"0003A1' | // Rho
    '\\rho' |
    '\\varrho' |
    '\\Sigma' |
    '\\sigma' |
    '\\varsigma' |
    '\\char"0003A4' | // Tau
    '\\tau' |
    '\\Upsilon' |
    '\\upsilon' |
    '\\Phi' |
    '\\phi' |
    '\\varphi' |
    '\\char"0003A7' | // Chi
    '\\chi' |
    '\\Psi' |
    '\\psi' |
    '\\Omega' |
    '\\omega';
GREEK_CMD: GREEK_LETTER [ ]?;

fragment PI: '\\pi';
fragment INFTY_CMD: '\\infty';
fragment INFTY: INFTY_CMD | DOLLAR_SIGN INFTY_CMD | INFTY_CMD PERCENT_SIGN;
fragment EMPTYSET: '\\emptyset';
fragment IMAGINARY_I: '\\imaginaryI';
fragment IMAGINARY_J: '\\imaginaryJ';
SYMBOL: PI | INFTY | EMPTYSET | IMAGINARY_I | IMAGINARY_J;

fragment VARIABLE_CMD: '\\variable';
fragment VARIABLE_SYMBOL: (GREEK_CMD | LETTER | DIGIT)+ (UNDERSCORE ((L_BRACE (GREEK_CMD | LETTER | DIGIT | COMMA)+ R_BRACE) | (GREEK_CMD | LETTER | DIGIT)))?;
VARIABLE: VARIABLE_CMD L_BRACE VARIABLE_SYMBOL R_BRACE PERCENT_SIGN?;

fragment ANGLE: '\\angle';
fragment DEGREE: '\\degree';
fragment COMPLEX_NUMBER_POLAR_ANGLE_DEGREES: (NUMBER | VARIABLE) DEGREE ' ';
fragment COMPLEX_NUMBER_RADIANS: 
    NUMBER ((MUL | CMD_TIMES ' ' | CMD_CDOT ' ')? PI)?
    | (NUMBER (MUL | CMD_TIMES ' ' | CMD_CDOT ' ')?)? PI;
fragment COMPLEX_NUMBER_RADIAN_FRACTION: CMD_FRAC L_BRACE SUB? COMPLEX_NUMBER_RADIANS R_BRACE L_BRACE SUB? NUMBER R_BRACE;
fragment COMPLEX_NUMBER_POLAR_ANGLE_RADIANS:
    COMPLEX_NUMBER_RADIANS
    | COMPLEX_NUMBER_RADIAN_FRACTION
    | FRACTION_NUMBER PI
    | VARIABLE;
COMPLEX_NUMBER_POLAR_ANGLE: ANGLE ' ' SUB? (COMPLEX_NUMBER_POLAR_ANGLE_DEGREES | COMPLEX_NUMBER_POLAR_ANGLE_RADIANS);

// collection of accents
accent_symbol:
    ACCENT_BAR | ACCENT_OVERLINE;

math: relation | relation_list;

matrix:
    CMD_MATRIX_START
    matrix_row (MATRIX_DEL_ROW matrix_row)*
    CMD_MATRIX_END;

matrix_row:
    expr (MATRIX_DEL_COL expr)*;

relation:
    relation (EQUAL | LT | LTE | GT | GTE | UNEQUAL) relation
    | expr;

relation_list:
    relation_list_content
    | L_PAREN relation_list_content R_PAREN
    | L_GROUP relation_list_content R_GROUP
    | L_BRACE relation_list_content R_BRACE
    | L_BRACE_VISUAL relation_list_content R_BRACE_VISUAL
    | L_BRACE_CMD relation_list_content R_BRACE_CMD
    | L_BRACKET relation_list_content R_BRACKET
    | L_BRACK relation_list_content R_BRACK
    | L_LEFT L_PAREN relation_list_content R_RIGHT R_PAREN
    | L_LEFT L_GROUP relation_list_content R_RIGHT R_GROUP
    | L_LEFT L_BRACE relation_list_content R_RIGHT R_BRACE
    | L_LEFT L_BRACE_VISUAL relation_list_content R_RIGHT R_BRACE_VISUAL
    | L_LEFT L_BRACE_CMD relation_list_content R_RIGHT R_BRACE_CMD
    | L_LEFT L_BRACKET relation_list_content R_RIGHT R_BRACKET
    | L_LEFT L_BRACK relation_list_content R_RIGHT R_BRACK
    | ML_LEFT L_PAREN relation_list_content MR_RIGHT R_PAREN
    | ML_LEFT L_GROUP relation_list_content MR_RIGHT R_GROUP
    | ML_LEFT L_BRACE relation_list_content MR_RIGHT R_BRACE
    | ML_LEFT L_BRACE_VISUAL relation_list_content MR_RIGHT R_BRACE_VISUAL
    | ML_LEFT L_BRACE_CMD relation_list_content MR_RIGHT R_BRACE_CMD
    | ML_LEFT L_BRACKET relation_list_content MR_RIGHT R_BRACKET
    | ML_LEFT L_BRACK relation_list_content MR_RIGHT R_BRACK;

relation_list_content:
    relation COMMA relation (COMMA relation)*
    | relation SEMICOLON relation (SEMICOLON relation)*;

equality:
    expr EQUAL expr;

expr: additive;

additive:
    additive (ADD | SUB) additive
    | mp;

// multi part
mp:
    mp (MUL | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV | COLON | CMD_MOD) mp
    | unary;

// multi part that does not include "func"
mp_nofunc:
    mp_nofunc (MUL | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV | COLON | CMD_MOD) mp_nofunc
    | unary_nofunc;

unary:
    (ADD | SUB) unary
    | postfix+;

unary_nofunc:
    (ADD | SUB) unary_nofunc
    | postfix postfix_nofunc*;

postfix: exp postfix_op*;
postfix_nofunc: exp_nofunc postfix_op*;
postfix_op: BANG | eval_at;

eval_at:
    BAR (eval_at_sup | eval_at_sub | eval_at_sup eval_at_sub);

eval_at_sub:
    UNDERSCORE L_BRACE
    (expr | equality)
    R_BRACE;

eval_at_sup:
    CARET L_BRACE
    (expr | equality)
    R_BRACE;

exp:
    exp CARET (atom | L_BRACE expr R_BRACE) subexpr?
    | comp;

exp_nofunc:
    exp_nofunc CARET (atom | L_BRACE expr R_BRACE) subexpr?
    | comp_nofunc;

comp:
    group
    | abs_group
    | floor_group
    | ceil_group
    | func
    | atom
    | frac
    | binom
    | matrix;

comp_nofunc:
    group
    | abs_group
    | floor_group
    | ceil_group
    | atom
    | frac
    | binom
    | matrix;

group:
    L_PAREN expr R_PAREN
    | L_GROUP expr R_GROUP
    | L_BRACE expr R_BRACE
    | L_BRACE_VISUAL expr R_BRACE_VISUAL
    | L_BRACE_CMD expr R_BRACE_CMD
    | L_BRACKET expr R_BRACKET
    | L_BRACK expr R_BRACK
    | L_LEFT L_PAREN expr R_RIGHT R_PAREN
    | L_LEFT L_GROUP expr R_RIGHT R_GROUP
    | L_LEFT L_BRACE expr R_RIGHT R_BRACE
    | L_LEFT L_BRACE_VISUAL expr R_RIGHT R_BRACE_VISUAL
    | L_LEFT L_BRACE_CMD expr R_RIGHT R_BRACE_CMD
    | L_LEFT L_BRACKET expr R_RIGHT R_BRACKET
    | L_LEFT L_BRACK expr R_RIGHT R_BRACK
    | ML_LEFT L_PAREN expr MR_RIGHT R_PAREN
    | ML_LEFT L_GROUP expr MR_RIGHT R_GROUP
    | ML_LEFT L_BRACE expr MR_RIGHT R_BRACE
    | ML_LEFT L_BRACE_VISUAL expr MR_RIGHT R_BRACE_VISUAL
    | ML_LEFT L_BRACE_CMD expr MR_RIGHT R_BRACE_CMD
    | ML_LEFT L_BRACKET expr MR_RIGHT R_BRACKET
    | ML_LEFT L_BRACK expr MR_RIGHT R_BRACK;


abs_group:
    BAR expr BAR
    | L_VERT expr R_VERT
    | VERT expr VERT
    | L_LEFT BAR expr R_RIGHT BAR
    | L_LEFT L_VERT expr R_RIGHT R_VERT
    | L_LEFT VERT expr R_RIGHT VERT
    | ML_LEFT BAR expr MR_RIGHT BAR
    | ML_LEFT L_VERT expr MR_RIGHT R_VERT
    | ML_LEFT VERT expr MR_RIGHT VERT;


floor_group:
    L_FLOOR expr R_FLOOR
    | LL_CORNER expr LR_CORNER
    | L_LEFT L_FLOOR expr R_RIGHT R_FLOOR
    | L_LEFT LL_CORNER expr R_RIGHT LR_CORNER
    | ML_LEFT L_FLOOR expr MR_RIGHT R_FLOOR
    | ML_LEFT LL_CORNER expr MR_RIGHT LR_CORNER;


ceil_group:
    L_CEIL expr R_CEIL
    | UL_CORNER expr UR_CORNER
    | L_LEFT L_CEIL expr R_RIGHT R_CEIL
    | L_LEFT UL_CORNER expr R_RIGHT UR_CORNER
    | ML_LEFT L_CEIL expr MR_RIGHT R_CEIL
    | ML_LEFT UL_CORNER expr MR_RIGHT UR_CORNER;


// indicate an accent
accent:
    accent_symbol
    L_BRACE base=expr R_BRACE;

atom_expr: (LETTER_NO_E | GREEK_CMD | accent) (supexpr subexpr | subexpr supexpr | subexpr | supexpr)?;
atom: atom_expr | SYMBOL | NUMBER | SCI_NOTATION_NUMBER | FRACTION_NUMBER | PERCENT_NUMBER | E_NOTATION | DIFFERENTIAL | mathit | VARIABLE | COMPLEX_NUMBER_POLAR_ANGLE;

mathit: CMD_MATHIT L_BRACE mathit_text R_BRACE;
mathit_text: (LETTER_NO_E | E_NOTATION_E | EXP_E)+;

frac:
    CMD_FRAC L_BRACE
    upper=expr
    R_BRACE L_BRACE
    lower=expr
    R_BRACE;

// a binomial expression
binom:
    (CMD_BINOM | CMD_CHOOSE) L_BRACE
    upper=expr
    R_BRACE L_BRACE
    lower=expr
    R_BRACE;

args: expr (',' args)?;
func_arg: expr;
func_arg_noparens: mp_nofunc;
func_args: expr (',' func_args)?;

subexpr: UNDERSCORE (atom | L_BRACE (expr | args) R_BRACE);
supexpr: CARET (atom | L_BRACE expr R_BRACE);
subeq: UNDERSCORE L_BRACE equality R_BRACE;

limit_sub:
    UNDERSCORE L_BRACE
    (LETTER_NO_E | GREEK_CMD)
    LIM_APPROACH_SYM
    expr (CARET L_BRACE (ADD | SUB) R_BRACE)?
    R_BRACE;

func_cmd_single_arg:
    FUNC_LOG | FUNC_LN | FUNC_EXP
    | FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_CSC | FUNC_SEC | FUNC_COT
    | FUNC_ARCSIN | FUNC_ARCCOS | FUNC_ARCTAN
    | FUNC_ARCCSC | FUNC_ARCSEC | FUNC_ARCCOT
    | FUNC_SINH | FUNC_COSH | FUNC_TANH
    | FUNC_ARSINH | FUNC_ARCOSH | FUNC_ARTANH
    | FUNC_ARCSINH | FUNC_ARCCOSH | FUNC_ARCTANH
    | FUNC_FLOOR | FUNC_CEIL;

func_cmd_multi_arg:
    FUNC_GCD | FUNC_LCM | FUNC_MAX | FUNC_MIN;

func_name_single_arg:
    FUNC_ARSINH_NAME | FUNC_ARCOSH_NAME | FUNC_ARTANH_NAME
    | FUNC_ARCSINH_NAME | FUNC_ARCCOSH_NAME | FUNC_ARCTANH_NAME
    | FUNC_FLOOR_NAME | FUNC_CEIL_NAME
    | FUNC_RE_NAME | FUNC_IM_NAME | FUNC_ARG_NAME | FUNC_ABS_NAME;

func_name_multi_arg:
    FUNC_GCD_NAME | FUNC_LCM_NAME;

func_single_arg:
    func_cmd_single_arg
    | CMD_OPERATORNAME L_BRACE func_operator_name=func_name_single_arg R_BRACE;

func_multi_arg:
    func_cmd_multi_arg
    | CMD_OPERATORNAME L_BRACE func_operator_name=func_name_multi_arg R_BRACE;

func:
    func_single_arg
    (subexpr? supexpr? | supexpr? subexpr?)
    (L_LEFT? L_PAREN func_arg R_RIGHT? R_PAREN | ML_LEFT? L_PAREN func_arg MR_RIGHT? R_PAREN | func_arg_noparens)

    | func_multi_arg
    (subexpr? supexpr? | supexpr? subexpr?)
    (L_LEFT? L_PAREN func_args R_RIGHT? R_PAREN | ML_LEFT? L_PAREN func_args MR_RIGHT? R_PAREN)

    // Do not do arbitrary functions but see as multiplications
    /*| (LETTER_NO_E | SYMBOL) subexpr? // e.g. f(x)
    L_PAREN args R_PAREN

    | (LETTER_NO_E | SYMBOL) subexpr? // e.g. f(x)
    L_LEFT L_PAREN args R_RIGHT R_PAREN*/

    | FUNC_INT
    (subexpr supexpr | supexpr subexpr | (UNDERSCORE L_BRACE R_BRACE) (CARET L_BRACE R_BRACE) | (CARET L_BRACE R_BRACE) (UNDERSCORE L_BRACE R_BRACE) )?
    (additive? DIFFERENTIAL | frac | additive)

    | FUNC_SQRT
    (L_BRACKET root=expr R_BRACKET)?
    L_BRACE base=expr R_BRACE

    | (FUNC_SUM | FUNC_PROD)
    (subeq supexpr | supexpr subeq)
    mp
    | FUNC_LIM limit_sub mp
    | EXP_E supexpr?; // Exponential function e^x
