#include <sstream>
#include "antlr4-runtime.h"
#include <json/json.h>
#include <pybind11/pybind11.h>
#include "LATEXLexer.h"
#include "LATEXParser.h"

using namespace latex2antlr;
using namespace antlr4;

/// @brief Return the friendly name for the given ParseTree if it is a RuleContext.
std::string getRuleName(tree::ParseTree *tree, LATEXParser *parser) {
    std::string name = "";
    if (ParserRuleContext::is(tree)) {
        ParserRuleContext *ruleContext = static_cast<ParserRuleContext *>(tree);
        const std::vector<std::string> ruleNames = parser->getRuleNames();
        int ruleIndex = ruleContext->getRuleIndex();
        name = ruleNames[ruleIndex];
    }
    return name;
}

/// @brief Convert a terminal node into a JSON object.
Json::Value toJson(tree::TerminalNode *terminalNode) {
    Json::Value node;
    Token* token = terminalNode->getSymbol();
    if (token) {
        node["text"] = token->getText();
        node["type"] = (int)token->getType();
    } else {
        node["type"] = "-1";
    }
    return node;
}

/// @brief Convert a ParseTree into a JSON object, recursively.
Json::Value toJson(tree::ParseTree *tree, LATEXParser *parser);

/// @brief Convert a FracContext into a JSON object.
Json::Value fracToJson(LATEXParser::FracContext *frac, LATEXParser *parser) {
    Json::Value node;

    // explicitly construct upper and lower nodes with required sub nodes

    LATEXParser::ExprContext *upperCtx = frac->expr(0);
    Json::Value upper = toJson(upperCtx, parser);
    upper["text"] = upperCtx->getText();
    upper["start"]["text"] = upperCtx->getStart()->getText();
    upper["start"]["type"] = (int)upperCtx->getStart()->getType();
    upper["stop"]["text"] = upperCtx->getStop()->getText();
    upper["stop"]["type"] = (int)upperCtx->getStop()->getType();
    node["upper"] = upper;

    LATEXParser::ExprContext *lowerCtx = frac->expr(1);
    Json::Value lower = toJson(lowerCtx, parser);
    lower["text"] = lowerCtx->getText();
    lower["start"]["text"] = lowerCtx->getStart()->getText();
    lower["start"]["type"] = (int)lowerCtx->getStart()->getType();
    lower["stop"]["text"] = lowerCtx->getStop()->getText();
    lower["stop"]["type"] = (int)lowerCtx->getStop()->getType();
    node["lower"] = lower;

    // iterate all children to find all terminal nodes to create tokens
    Json::Value tokens;
    for (auto *child : frac->children) {
        if (tree::TerminalNode::is(child)) {
            tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(child);
            Json::Value childNode = toJson(terminalNode);
            tokens.append(childNode);
        }
    }

    // if there is only one token, merge it into the current node
    // otherwise add tokens as a nested array
    if (tokens.size() == 1) {
        node["text"] = tokens[0]["text"];
        node["type"] = tokens[0]["type"];
    } else if (tokens.size() > 0) {
        node["tokens"] = tokens;
    }

    return node;
}

/// @brief Convert a ParseTree into a JSON object, recursively.
Json::Value toJson(tree::ParseTree *tree, LATEXParser *parser) {
    std::string name = getRuleName(tree, parser);
    std::string parentName = tree->parent ? getRuleName(tree->parent, parser) : "";

    Json::Value node;
    Json::Value tokens;

    // iterate all children to find nested rule contexts and terminal nodes
    for (auto *child : tree->children) {
        if (ParserRuleContext::is(child)) {
            std::string childName = getRuleName(child, parser);
            // frac requires additional custom subnodes
            if (childName == "frac") {
                LATEXParser::FracContext *frac = static_cast<LATEXParser::FracContext *>(child);
                Json::Value childNode = fracToJson(frac, parser);
                node[childName] = childNode;
            } else {
                // recurse to convert the child tree
                Json::Value childNode = toJson(child, parser);
                if (node[childName].empty()) {
                    // force certain rules to ALWAYs return as an array
                    // otherwise, single values are set as property objects, e.g. { "foo": child }
                    if (childName == "postfix" ||
                        childName == "postfix_nofunc" ||
                        childName == "postfix_op" ||
                        childName == "matrix_row")
                    {
                        Json::Value array;
                        array.append(childNode);
                        node[childName] = array;
                    } else {
                        node[childName] = childNode;
                    }
                } else if (node[childName].isArray()) {
                    // if there is already an array at the given name, simply append the new child
                    node[childName].append(childNode);
                } else {
                    // if a child with the same name was added as a property object
                    // convert that property to an array, and append the new child
                    // e.g. { "foo": child1 } => { "foo": [child1, child2]}
                    Json::Value array;
                    array.append(node[childName]);
                    array.append(childNode);
                    node[childName] = array;
                }
            }
        } else if (tree::TerminalNode::is(child)) {
            tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(child);
            Json::Value childNode = toJson(terminalNode);
            tokens.append(childNode);
        }
    }

    // if there is only one token, merge it into the current node
    // otherwise add tokens as a nested array
    if (tokens.size() == 1) {
        node["text"] = tokens[0]["text"];
        node["type"] = tokens[0]["type"];
    } else if (tokens.size() > 0) {
        node["tokens"] = tokens;
    }

    // return the full text of the tree for specific rules
    if (name == "func_args" ||
        name == "mathit_text" ||
        parentName == "supexpr" ||
        parentName == "subexpr" ||
        parentName == "accent") {
        node["text"] = tree->getText();
    }

    return node;
}

/// @brief Convert a ParseTree to JSON and then write it to a string.
std::string toJsonString(tree::ParseTree *tree, LATEXParser *parser) {
    Json::Value root = toJson(tree, parser);
    Json::FastWriter fastWriter;
    std::string json = fastWriter.write(root);
    return json;
}

class MathErrorListener : public BaseErrorListener {
    public:
        std::string src;
        MathErrorListener(const std::string &input) : BaseErrorListener() {
            src = input;
        }

        void syntaxError(Recognizer *recognizer, Token *offendingSymbol, size_t line, size_t charPositionInLine,
            const std::string &msg, std::exception_ptr e) {
                std::string marker(charPositionInLine, '~');
                std::ostringstream ss;
                if (msg.rfind("missing", 0) == 0) {
                    ss << msg << "\n" << src << "\n" << marker << "^";
                } else if (msg.rfind("no viable", 0) == 0) {
                    ss << "I expected something else here" << "\n" << src << "\n" << marker << "^";
                } else if (msg.rfind("mismatched", 0) == 0) {
                    ss << "I expected something else here" << "\n" << src << "\n" << marker << "^";
                } else {
                    ss << "I don't understand this" << "\n" << src << "\n" << marker << "^";
                }
                std::string str = ss.str();
                throw std::invalid_argument(str);
        }

};

/// @brief A function which parses a latex string and returns a json string of antlr data
std::string parseToJson(const std::string &input) {
    MathErrorListener mathErrorListener(input);
    ANTLRInputStream stream(input);

    LATEXLexer lexer(&stream);
    lexer.removeErrorListeners();
    lexer.addErrorListener(&mathErrorListener);

    CommonTokenStream tokens(&lexer);
    LATEXParser parser(&tokens);
    parser.removeErrorListeners();
    parser.addErrorListener(&mathErrorListener);

    LATEXParser::MathContext *math = parser.math();

    std::string jsonString = toJsonString(math, &parser);
    return jsonString;
}

namespace py = pybind11;

// in order to export the LATEXLexer enum values, which is anonymous,
// copy the enum here from LATEXLexer.h and give it a name
enum LATEXLexerToken {
    WS = 1, DOLLAR_SIGN = 2, UNDERSCORE = 3, CARET = 4, COLON = 5, SEMICOLON = 6, 
    COMMA = 7, ADD = 8, SUB = 9, MUL = 10, DIV = 11, EQUAL = 12, LT = 13, 
    LTE = 14, GT = 15, GTE = 16, UNEQUAL = 17, BANG = 18, L_PAREN = 19, 
    R_PAREN = 20, L_GROUP = 21, R_GROUP = 22, L_BRACE = 23, R_BRACE = 24, 
    L_BRACE_VISUAL = 25, R_BRACE_VISUAL = 26, L_BRACE_CMD = 27, R_BRACE_CMD = 28, 
    L_BRACKET = 29, R_BRACKET = 30, L_BRACK = 31, R_BRACK = 32, BAR = 33, 
    L_VERT = 34, R_VERT = 35, VERT = 36, L_FLOOR = 37, R_FLOOR = 38, LL_CORNER = 39, 
    LR_CORNER = 40, L_CEIL = 41, R_CEIL = 42, UL_CORNER = 43, UR_CORNER = 44, 
    L_LEFT = 45, R_RIGHT = 46, ML_LEFT = 47, MR_RIGHT = 48, FUNC_LIM = 49, 
    LIM_APPROACH_SYM = 50, FUNC_INT = 51, FUNC_SUM = 52, FUNC_PROD = 53, 
    FUNC_LOG = 54, FUNC_LN = 55, FUNC_EXP = 56, FUNC_SIN = 57, FUNC_COS = 58, 
    FUNC_TAN = 59, FUNC_CSC = 60, FUNC_SEC = 61, FUNC_COT = 62, FUNC_ARCSIN = 63, 
    FUNC_ARCCOS = 64, FUNC_ARCTAN = 65, FUNC_ARCCSC = 66, FUNC_ARCSEC = 67, 
    FUNC_ARCCOT = 68, FUNC_SINH = 69, FUNC_COSH = 70, FUNC_TANH = 71, FUNC_ARSINH = 72, 
    FUNC_ARCOSH = 73, FUNC_ARTANH = 74, FUNC_ARCSINH = 75, FUNC_ARCCOSH = 76, 
    FUNC_ARCTANH = 77, FUNC_ARSINH_NAME = 78, FUNC_ARCSINH_NAME = 79, FUNC_ARCOSH_NAME = 80, 
    FUNC_ARCCOSH_NAME = 81, FUNC_ARTANH_NAME = 82, FUNC_ARCTANH_NAME = 83, 
    FUNC_GCD_NAME = 84, FUNC_LCM_NAME = 85, FUNC_FLOOR_NAME = 86, FUNC_CEIL_NAME = 87, 
    FUNC_SQRT = 88, FUNC_GCD = 89, FUNC_LCM = 90, FUNC_FLOOR = 91, FUNC_CEIL = 92, 
    FUNC_MAX = 93, FUNC_MIN = 94, FUNC_RE_NAME = 95, FUNC_IM_NAME = 96, 
    FUNC_ARG_NAME = 97, FUNC_ABS_NAME = 98, FUNC_CONJ_NAME = 99, CMD_TIMES = 100, CMD_CDOT = 101, 
    CMD_DIV = 102, CMD_FRAC = 103, CMD_BINOM = 104, CMD_CHOOSE = 105, CMD_MOD = 106, 
    CMD_MATHIT = 107, CMD_OPERATORNAME = 108, MATRIX_TYPE_MATRIX = 109, 
    MATRIX_TYPE_PMATRIX = 110, MATRIX_TYPE_BMATRIX = 111, MATRIX_TYPES = 112, 
    CMD_MATRIX_START = 113, CMD_MATRIX_END = 114, MATRIX_DEL_COL = 115, 
    MATRIX_DEL_ROW = 116, ACCENT_OVERLINE = 117, ACCENT_BAR = 118, LETTER = 119, 
    UNIT_SYMBOL = 120, NUMBER = 121, FRACTION_NUMBER = 122, SCI_NOTATION_NUMBER = 123, 
    E_NOTATION = 124, PERCENT_NUMBER = 125, GREEK_CMD = 126, EXP_E = 127, 
    DIFFERENTIAL_D = 128, SYMBOL = 129, VARIABLE = 130, COMPLEX_NUMBER_POLAR_ANGLE = 131
};

// in order to export the LATEXLexer enum names,
// convert LATEXLexerToken array to strings and copy it here
static const char* LATEXLexerTokenStrings[] = {
    "WS", "DOLLAR_SIGN", "UNDERSCORE", "CARET", "COLON", "SEMICOLON", 
    "COMMA", "ADD", "SUB", "MUL", "DIV", "EQUAL", "LT", 
    "LTE", "GT", "GTE", "UNEQUAL", "BANG", "L_PAREN", 
    "R_PAREN", "L_GROUP", "R_GROUP", "L_BRACE", "R_BRACE", 
    "L_BRACE_VISUAL", "R_BRACE_VISUAL", "L_BRACE_CMD", "R_BRACE_CMD", 
    "L_BRACKET", "R_BRACKET", "L_BRACK", "R_BRACK", "BAR", 
    "L_VERT", "R_VERT", "VERT", "L_FLOOR", "R_FLOOR", "LL_CORNER", 
    "LR_CORNER", "L_CEIL", "R_CEIL", "UL_CORNER", "UR_CORNER", 
    "L_LEFT", "R_RIGHT", "ML_LEFT", "MR_RIGHT", "FUNC_LIM", 
    "LIM_APPROACH_SYM", "FUNC_INT", "FUNC_SUM", "FUNC_PROD", 
    "FUNC_LOG", "FUNC_LN", "FUNC_EXP", "FUNC_SIN", "FUNC_COS", 
    "FUNC_TAN", "FUNC_CSC", "FUNC_SEC", "FUNC_COT", "FUNC_ARCSIN", 
    "FUNC_ARCCOS", "FUNC_ARCTAN", "FUNC_ARCCSC", "FUNC_ARCSEC", 
    "FUNC_ARCCOT", "FUNC_SINH", "FUNC_COSH", "FUNC_TANH", "FUNC_ARSINH", 
    "FUNC_ARCOSH", "FUNC_ARTANH", "FUNC_ARCSINH", "FUNC_ARCCOSH", 
    "FUNC_ARCTANH", "FUNC_ARSINH_NAME", "FUNC_ARCSINH_NAME", "FUNC_ARCOSH_NAME", 
    "FUNC_ARCCOSH_NAME", "FUNC_ARTANH_NAME", "FUNC_ARCTANH_NAME", 
    "FUNC_GCD_NAME", "FUNC_LCM_NAME", "FUNC_FLOOR_NAME", "FUNC_CEIL_NAME", 
    "FUNC_SQRT", "FUNC_GCD", "FUNC_LCM", "FUNC_FLOOR", "FUNC_CEIL", 
    "FUNC_MAX", "FUNC_MIN", "FUNC_RE_NAME", "FUNC_IM_NAME", 
    "FUNC_ARG_NAME", "FUNC_ABS_NAME", "FUNC_CONJ_NAME", "CMD_TIMES", "CMD_CDOT", 
    "CMD_DIV", "CMD_FRAC", "CMD_BINOM", "CMD_CHOOSE", "CMD_MOD", 
    "CMD_MATHIT", "CMD_OPERATORNAME", "MATRIX_TYPE_MATRIX", 
    "MATRIX_TYPE_PMATRIX", "MATRIX_TYPE_BMATRIX", "MATRIX_TYPES", 
    "CMD_MATRIX_START", "CMD_MATRIX_END", "MATRIX_DEL_COL", 
    "MATRIX_DEL_ROW", "ACCENT_OVERLINE", "ACCENT_BAR", "LETTER", 
    "UNIT_SYMBOL", "NUMBER", "FRACTION_NUMBER", "SCI_NOTATION_NUMBER", 
    "E_NOTATION", "PERCENT_NUMBER", "GREEK_CMD", "EXP_E", 
    "DIFFERENTIAL_D", "SYMBOL", "VARIABLE", "COMPLEX_NUMBER_POLAR_ANGLE"
};

PYBIND11_MODULE(latex2antlrJson, m) {
    m.doc() = "pybind11 latex2antlrJson plugin"; // optional module docstring
    m.def("parseToJson", &parseToJson, "A function which parses latex and returns a json string of antlr data");
    py::enum_<LATEXLexerToken> tokens = py::enum_<LATEXLexerToken>(m, "LATEXLexerToken");
    // iterate from the first to last LATEXLexer enum values
    for (int token = LATEXLexerToken::WS; token <= LATEXLexerToken::COMPLEX_NUMBER_POLAR_ANGLE; token++)
    {
        tokens.value(LATEXLexerTokenStrings[token - 1], static_cast<LATEXLexerToken>(token));
    }
    tokens.export_values();
}
