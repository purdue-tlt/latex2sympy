#include <chrono>
#include <sstream>
#include "antlr4-runtime.h"
#include <json/json.h>
#include <pybind11/pybind11.h>
#include "LATEXLexer.h"
#include "LATEXParser.h"

using namespace latex2antlr;
using namespace antlr4;
using namespace std::chrono;

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
    if (name == "func_multi_arg" ||
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

// in order to export the LATEXLexer enum names,
// convert LATEXLexerToken array to strings and copy it here
static const char* LATEXLexerTokenStrings[] = {
    "WS", "DOLLAR_SIGN", "ADD", "SUB", "MUL", "DIV", "L_PAREN", 
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
    "FUNC_MAX", "FUNC_MIN", "CMD_TIMES", "CMD_CDOT", "CMD_DIV", 
    "CMD_FRAC", "CMD_BINOM", "CMD_CHOOSE", "CMD_MOD", "CMD_MATHIT", 
    "CMD_OPERATORNAME", "MATRIX_TYPE_MATRIX", "MATRIX_TYPE_PMATRIX", 
    "MATRIX_TYPE_BMATRIX", "MATRIX_TYPES", "CMD_MATRIX_START", 
    "CMD_MATRIX_END", "MATRIX_DEL_COL", "MATRIX_DEL_ROW", "ACCENT_OVERLINE", 
    "ACCENT_BAR", "UNDERSCORE", "CARET", "COLON", "SEMICOLON", 
    "COMMA", "PERIOD", "DIFFERENTIAL", "EXP_E", "E_NOTATION_E", 
    "LETTER_NO_E", "NUMBER", "FRACTION_NUMBER", "SCI_NOTATION_NUMBER", 
    "E_NOTATION", "EQUAL", "LT", "LTE", "GT", "GTE", 
    "UNEQUAL", "BANG", "PERCENT_NUMBER", "GREEK_CMD", "SYMBOL", 
    "VARIABLE"
};

PYBIND11_MODULE(latex2antlrJson, m) {
    m.doc() = "pybind11 latex2antlrJson plugin"; // optional module docstring
    m.def("parseToJson", &parseToJson, "A function which parses latex and returns a json string of antlr data");
    py::enum_<LATEXLexerToken> tokens = py::enum_<LATEXLexerToken>(m, "LATEXLexerToken");
    // iterate from the first to last LATEXLexer enum values
    for (int token = LATEXLexerToken::WS; token <= LATEXLexerToken::VARIABLE; token++)
    {
        tokens.value(LATEXLexerTokenStrings[token - 1], static_cast<LATEXLexerToken>(token));
    }
    tokens.export_values();
}
