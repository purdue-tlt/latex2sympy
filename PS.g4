grammar PS;

options {
    language=Python2;
}

WS: [ \t\r\n]+ -> skip;
DOLLAR_SIGN: '\\$' -> skip;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACE_VISUAL: '\\{';
R_BRACE_VISUAL: '\\}';
L_BRACKET: '[';
R_BRACKET: ']';
L_LEFT: '\\left';
R_RIGHT: '\\right';
ML_LEFT: '\\mleft';
MR_RIGHT: '\\mright';

BAR: '|';

//functions
FUNC_LIM:  '\\lim';
LIM_APPROACH_SYM: '\\to' | '\\rightarrow' | '\\Rightarrow' | '\\longrightarrow' | '\\Longrightarrow';
FUNC_INT:  '\\int';
FUNC_SUM:  '\\sum';
FUNC_PROD: '\\prod';

FUNC_LOG:  '\\log';
FUNC_LN:   '\\ln';
FUNC_EXP: '\\exp' | '\\exponentialE';
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


FUNC_SQRT: '\\sqrt';

//commands
CMD_TIMES: '\\times';
CMD_CDOT:  '\\cdot';
CMD_DIV:   '\\div';
CMD_FRAC:  '\\frac';
CMD_BINOM: '\\binom';
CMD_CHOOSE: '\\choose';
CMD_MOD: '\\mod';

CMD_MATHIT: '\\mathit';

CMD_OPERATORNAME: '\\operatorname';

//matrix test
MATRIX_TYPE_MATRIX: 'matrix';
MATRIX_TYPE_PMATRIX: 'pmatrix';
MATRIX_TYPE_BMATRIX: 'bmatrix';
MATRIX_TYPES: MATRIX_TYPE_MATRIX | MATRIX_TYPE_PMATRIX | MATRIX_TYPE_BMATRIX;
CMD_MATRIX_START: '\\begin' L_BRACE MATRIX_TYPES R_BRACE;
CMD_MATRIX_END: '\\end' L_BRACE MATRIX_TYPES R_BRACE;
MATRIX_DEL_COL: '&';
MATRIX_DEL_ROW: '\\\\';

//accents such as overline and hat
ACCENT_OVERLINE:  '\\overline';
ACCENT_BAR:  '\\bar';

UNDERSCORE: '_';
CARET: '^';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
PERIOD: '.';

fragment WS_CHAR: [ \t\r\n];
DIFFERENTIAL: 'd' WS_CHAR*? ([a-zA-Z] | '\\' [a-zA-Z]+);

EXP_E: 'e';
E_NOTATION_E: 'E';
LETTER_NO_E: [a-df-zA-DF-Z]; // exclude e for exponential function and e notation
fragment LETTER: [a-zA-Z];
fragment DIGIT: [0-9];
NUMBER:
    DIGIT+ (COMMA DIGIT DIGIT DIGIT)*
    | DIGIT* (COMMA DIGIT DIGIT DIGIT)* PERIOD DIGIT+;

E_NOTATION: NUMBER E_NOTATION_E (SUB | ADD)? DIGIT+;

EQUAL: '=';
LT: '<';
LTE: '\\leq' | '\\le';
GT: '>';
GTE: '\\geq' | '\\ge';
UNEQUAL: '!=' | '\\ne' | '\\neq';

BANG: '!';

fragment PERCENT_SIGN: '\\%';
PERCENT_NUMBER: NUMBER PERCENT_SIGN;

//Excludes some letters for use as e.g. constants in SYMBOL
GREEK_LETTER:
    '\\char"000391' | //Alpha
    '\\alpha' |
    '\\char"000392' | //Beta
    '\\beta' |
    '\\Gamma' |
    '\\gamma' |
    '\\Delta' |
    '\\delta' |
    '\\char"000190' | //Epsilon
    '\\epsilon' |
    '\\varepsilon' |
    '\\char"000396' | //Zeta
    '\\zeta' |
    '\\char"000397' | //Eta
    '\\eta' |
    '\\Theta' |
    '\\theta' |
    '\\vartheta' |
    '\\char"000399' | //Iota
    '\\iota' |
    '\\char"00039A' | //Kappa
    '\\kappa' |
    '\\Lambda' |
    '\\lambda' |
    '\\char"00039C' | //Mu
    '\\mu' |
    '\\char"00039D' | //Nu
    '\\nu' |
    '\\Xi' |
    '\\xi' |
    '\\char"00039F' | //Omicron
    '\\omicron' |
    '\\Pi' |
    '\\varpi' |
    '\\char"0003A1' | //Rho
    '\\rho' |
    '\\varrho' |
    '\\Sigma' |
    '\\sigma' |
    '\\varsigma' |
    '\\char"0003A4' | //Tau
    '\\tau' |
    '\\Upsilon' |
    '\\upsilon' |
    '\\Phi' |
    '\\phi' |
    '\\varphi' |
    '\\char"0003A7' | //Chi
    '\\chi' |
    '\\Psi' |
    '\\psi' |
    '\\Omega' |
    '\\omega';

fragment PI: '\\pi';
fragment INFTY_CMD: '\\infty';
fragment INFTY: INFTY_CMD | DOLLAR_SIGN INFTY_CMD | INFTY_CMD PERCENT_SIGN;
SYMBOL: PI | INFTY;

fragment VARIABLE_CMD: '\\variable';
fragment VARIABLE_SYMBOL: (GREEK_LETTER [ ]? | LETTER | DIGIT)+ (UNDERSCORE ((L_BRACE (GREEK_LETTER [ ]? | LETTER | DIGIT | COMMA)+ R_BRACE) | (GREEK_LETTER [ ]? | LETTER | DIGIT)))?;
VARIABLE: VARIABLE_CMD L_BRACE VARIABLE_SYMBOL R_BRACE PERCENT_SIGN?;

//collection of accents
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
    | L_BRACKET relation_list_content R_BRACKET
    | L_BRACE relation_list_content R_BRACE
    | L_BRACE_VISUAL relation_list_content R_BRACE_VISUAL
    | L_LEFT L_BRACKET relation_list_content R_RIGHT R_BRACKET
    | L_LEFT L_BRACE_VISUAL relation_list_content R_RIGHT R_BRACE_VISUAL
    | ML_LEFT L_BRACKET relation_list_content MR_RIGHT R_BRACKET
    | ML_LEFT L_BRACE_VISUAL relation_list_content MR_RIGHT R_BRACE_VISUAL;

relation_list_content:
    relation COMMA relation (COMMA relation)*
    | relation SEMICOLON relation (SEMICOLON relation)*;

equality:
    expr EQUAL expr;

expr: additive;

additive:
    additive (ADD | SUB) additive
    | mp;

// mult part
mp:
    mp (MUL | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV | COLON | CMD_MOD) mp
    | unary;

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
    | func
    | atom
    | frac
    | binom
    | matrix;

comp_nofunc:
    group
    | abs_group
    | atom
    | frac
    | binom
    | matrix;

group:
    L_PAREN expr R_PAREN
    | L_BRACKET expr R_BRACKET
    | L_BRACE expr R_BRACE
    | L_LEFT L_PAREN expr R_RIGHT R_PAREN
    | L_LEFT L_BRACKET expr R_RIGHT R_BRACKET
    | L_LEFT L_BRACE expr R_RIGHT R_BRACE
    | L_LEFT L_BRACE_VISUAL expr R_RIGHT R_BRACE_VISUAL
    | ML_LEFT L_PAREN expr MR_RIGHT R_PAREN
    | ML_LEFT L_BRACKET expr MR_RIGHT R_BRACKET
    | ML_LEFT L_BRACE expr MR_RIGHT R_BRACE
    | ML_LEFT L_BRACE_VISUAL expr MR_RIGHT R_BRACE_VISUAL;


abs_group:
    BAR expr BAR
    | L_LEFT BAR expr R_RIGHT BAR
    | ML_LEFT BAR expr MR_RIGHT BAR;


//indicate an accent
accent:
    accent_symbol
    L_BRACE base=expr R_BRACE;

atom: (LETTER_NO_E | GREEK_LETTER | accent) subexpr? | SYMBOL | NUMBER | PERCENT_NUMBER | E_NOTATION | DIFFERENTIAL | mathit | VARIABLE;

mathit: CMD_MATHIT L_BRACE mathit_text R_BRACE;
mathit_text: (LETTER_NO_E | E_NOTATION_E | EXP_E)+;

frac:
    CMD_FRAC L_BRACE
    upper=expr
    R_BRACE L_BRACE
    lower=expr
    R_BRACE;

//a binomial expression
binom:
    (CMD_BINOM | CMD_CHOOSE) L_BRACE
    upper=expr
    R_BRACE L_BRACE
    lower=expr
    R_BRACE;

func_normal_functions:
    FUNC_LOG | FUNC_LN | FUNC_EXP
    | FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_CSC | FUNC_SEC | FUNC_COT
    | FUNC_ARCSIN | FUNC_ARCCOS | FUNC_ARCTAN
    | FUNC_ARCCSC | FUNC_ARCSEC | FUNC_ARCCOT
    | FUNC_SINH | FUNC_COSH | FUNC_TANH
    | FUNC_ARSINH | FUNC_ARCOSH | FUNC_ARTANH
    | FUNC_ARCSINH | FUNC_ARCCOSH | FUNC_ARCTANH;

func_operator_names:
    FUNC_ARSINH_NAME | FUNC_ARCOSH_NAME | FUNC_ARTANH_NAME
    | FUNC_ARCSINH_NAME | FUNC_ARCCOSH_NAME | FUNC_ARCTANH_NAME;

func_normal:
    (func_normal_functions)
    |
    (CMD_OPERATORNAME L_BRACE func_operator_name=func_operator_names R_BRACE);

func:
    func_normal
    (subexpr? supexpr? | supexpr? subexpr?)
    (L_LEFT? L_PAREN func_arg R_RIGHT? R_PAREN | ML_LEFT? L_PAREN func_arg MR_RIGHT? R_PAREN | func_arg_noparens)

    //Do not do arbitraty functions but see as multiplications
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
    | EXP_E supexpr?; //Exponential function e^x

args: (expr ',' args) | expr;

limit_sub:
    UNDERSCORE L_BRACE
    (LETTER_NO_E | GREEK_LETTER)
    LIM_APPROACH_SYM
    expr (CARET L_BRACE (ADD | SUB) R_BRACE)?
    R_BRACE;

func_arg: expr | (expr ',' func_arg);
func_arg_noparens: mp_nofunc;

subexpr: UNDERSCORE (atom | L_BRACE expr R_BRACE);
supexpr: CARET (atom | L_BRACE expr R_BRACE);

subeq: UNDERSCORE L_BRACE equality R_BRACE;
supeq: UNDERSCORE L_BRACE equality R_BRACE;
