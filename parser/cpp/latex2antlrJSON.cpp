#include "antlr4-runtime.h"
// #include "/opt/Homebrew/include/antlr4-runtime/antlr4-runtime.h"
#include "LATEXLexer.h"
#include "LATEXParser.h"
#include <pybind11/pybind11.h>
#include <chrono>
#include <json/json.h>
#include <sstream>

using namespace latex2antlr;
using namespace antlr4;
using namespace std::chrono;

Json::Value toJsonNode(tree::ErrorNode *errorNode) {
    Json::Value node;
    Token* token = errorNode->getSymbol();
    if (token) {
        node["error"] = token->getText();
    } else {
        node["error"] = token->toString();
    }
    return node;
}

Json::Value toJsonNode(tree::TerminalNode *terminalNode) {
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

std::string getRuleName(tree::ParseTree *tree, LATEXParser *parser) {
    ParserRuleContext *ruleContext = static_cast<ParserRuleContext *>(tree);
    const std::vector<std::string> ruleNames = parser->getRuleNames();
    int ruleIndex = ruleContext->getRuleIndex();
    std::string name = ruleNames[ruleIndex];
    return name;
}

Json::Value toJsonTree(tree::ParseTree *tree, LATEXParser *parser);

Json::Value fracToJsonTree(LATEXParser::FracContext *frac, LATEXParser *parser) {
    Json::Value node;

    LATEXParser::ExprContext *upperCtx = frac->expr(0);
    Json::Value upper = toJsonTree(upperCtx, parser);
    upper["text"] = upperCtx->getText();
    upper["start"]["text"] = upperCtx->getStart()->getText();
    upper["start"]["type"] = (int)upperCtx->getStart()->getType();
    upper["stop"]["text"] = upperCtx->getStop()->getText();
    upper["stop"]["type"] = (int)upperCtx->getStop()->getType();
    node["upper"] = upper;

    LATEXParser::ExprContext *lowerCtx = frac->expr(1);
    Json::Value lower = toJsonTree(lowerCtx, parser);
    lower["text"] = lowerCtx->getText();
    lower["start"]["text"] = lowerCtx->getStart()->getText();
    lower["start"]["type"] = (int)lowerCtx->getStart()->getType();
    lower["stop"]["text"] = lowerCtx->getStop()->getText();
    lower["stop"]["type"] = (int)lowerCtx->getStop()->getType();
    misc::Interval lowerInterval = lowerCtx->getSourceInterval();
    lower["intervalLength"] = (int)lowerInterval.length();
    node["lower"] = lower;

    Json::Value tokens;
    Json::Value errors;
    for (auto *child : frac->children) {
        if (tree::ErrorNode::is(child)) {
            tree::ErrorNode *errorNode = static_cast<tree::ErrorNode *>(child);
            Json::Value childNode = toJsonNode(errorNode);
            tokens.append(childNode);
        } else if (tree::TerminalNode::is(child)) {
            tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(child);
            Json::Value childNode = toJsonNode(terminalNode);
            tokens.append(childNode);
        }
    }
    if (tokens.size() == 1) {
        node["text"] = tokens[0]["text"];
        node["type"] = tokens[0]["type"];
    } else if (tokens.size() > 0) {
        node["tokens"] = tokens;
    }
    if (errors.size() == 1) {
        node["error"] = tokens[0]["error"];
    } else if (errors.size() > 0) {
        node["errors"] = errors;
    }

    return node;
}

Json::Value toJsonTree(tree::ParseTree *tree, LATEXParser *parser) {
    std::string name = getRuleName(tree, parser);
    std::string parentName = tree->parent ? getRuleName(tree->parent, parser) : "";

    Json::Value node;
    Json::Value tokens;
    Json::Value errors;
    for (auto *child : tree->children) {
        if (ParserRuleContext::is(child)) {
            std::string childName = getRuleName(child, parser);
            if (childName == "frac") {
                LATEXParser::FracContext *frac = static_cast<LATEXParser::FracContext *>(child);
                Json::Value childNode = fracToJsonTree(frac, parser);
                node[childName] = childNode;
            } else {
                Json::Value childNode = toJsonTree(child, parser);
                // merge keys together into a single array
                if (childName == "postfix_nofunc") 
                    childName = "postfix";
                if (node[childName].empty()) {
                    if (childName == "postfix" || childName == "postfix_op" || childName == "matrix_row")
                    {
                        Json::Value array;
                        array.append(childNode);
                        node[childName] = array;
                    } else {
                        node[childName] = childNode;
                    }
                } else if (node[childName].isArray()) {
                    node[childName].append(childNode);
                } else {
                    Json::Value array;
                    array.append(node[childName]);
                    array.append(childNode);
                    node[childName] = array;
                }
            }
        } else if (tree::ErrorNode::is(child)) {
            tree::ErrorNode *errorNode = static_cast<tree::ErrorNode *>(child);
            Json::Value childNode = toJsonNode(errorNode);
            tokens.append(childNode);
        } else if (tree::TerminalNode::is(child)) {
            tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(child);
            Json::Value childNode = toJsonNode(terminalNode);
            tokens.append(childNode);
        }
    }

    if (tokens.size() == 1) {
        node["text"] = tokens[0]["text"];
        node["type"] = tokens[0]["type"];
    } else if (tokens.size() > 0) {
        node["tokens"] = tokens;
    }
    if (errors.size() == 1) {
        node["error"] = tokens[0]["error"];
    } else if (errors.size() > 0) {
        node["errors"] = errors;
    }

    // return full text of tree for specific rules
    if (name == "func_multi_arg" || parentName == "supexpr" || parentName == "subexpr" || parentName == "accent") {
        node["text"] = tree->getText();
    }

    return node;
}

std::string toJsonString(tree::ParseTree *tree, LATEXParser *parser) {
    Json::Value root = toJsonTree(tree, parser);
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

std::string parseToJson(const std::string &input) {
    // auto begin = high_resolution_clock::now();
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
    // auto end = high_resolution_clock::now();
    // auto duration = duration_cast<microseconds>(end - begin);
    // std::cout << math -> toStringTree(&parser, true) << std::endl;
    // std::cout << "Elapsed Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    // begin = high_resolution_clock::now();
    std::string jsonString = toJsonString(math, &parser);
    // end = high_resolution_clock::now();
    // duration = duration_cast<microseconds>(end - begin);
    // std::cout << "Elapsed Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    return jsonString;
}

namespace py = pybind11;

PYBIND11_MODULE(latex2antlrJson, m) {
    m.doc() = "pybind11 latex2antlrJson plugin"; // optional module docstring
    m.def("parseToJson", &parseToJson, "A function which parses latex and returns a json string of antlr data");
}
