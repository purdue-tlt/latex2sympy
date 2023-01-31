#include "antlr4-runtime.h"
// #include "/opt/Homebrew/include/antlr4-runtime/antlr4-runtime.h"
#include "LATEXLexer.h"
#include "LATEXParser.h"
#include <pybind11/pybind11.h>
#include <chrono>
#include <json/json.h>

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

void addTokensAndErrors(Json::Value node, tree::ParseTree *tree, LATEXParser *parser) {
    Json::Value tokens;
    Json::Value errors;
    for (auto *child : tree->children) {
        if (tree::ErrorNode::is(child)) {
            tree::ErrorNode *errorNode = static_cast<tree::ErrorNode *>(child);
            Json::Value childNode = toJsonNode(errorNode);
            errors.append(childNode);
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
}

Json::Value fracToJsonTree(LATEXParser::FracContext *frac, LATEXParser *parser) {
    Json::Value node;

    Json::Value upper;
    LATEXParser::ExprContext *upperCtx = frac->expr(0);
    node["upper"] = toJsonTree(upperCtx, parser);
    node["upper"]["text"] = upperCtx->getText();

    Json::Value lower;
    LATEXParser::ExprContext *lowerCtx = frac->expr(1);
    node["lower"] = toJsonTree(lowerCtx, parser);
    node["lower"]["text"] = lowerCtx->getText();

    addTokensAndErrors(node, frac, parser);

    return node;
}

Json::Value funcToJsonTree(LATEXParser::FuncContext *func, LATEXParser *parser) {
    if (func->FUNC_SQRT()) {
        Json::Value node;
        node["type"] = (int)LATEXParser::FUNC_SQRT;

        Json::Value base;
        LATEXParser::ExprContext *baseCtx = func->base;
        node["base"] = toJsonTree(baseCtx, parser);

        if (func->root) {
            Json::Value root;
            LATEXParser::ExprContext *rootCtx = func->root;
            node["root"] = toJsonTree(rootCtx, parser);
        }

        addTokensAndErrors(node, func, parser);
        return node;
    }
    return toJsonTree(func, parser);
}

Json::Value toJsonTree(tree::ParseTree *tree, LATEXParser *parser) {
    std::string name = getRuleName(tree, parser);
    Json::Value node;

    for (auto *child : tree->children) {
        if (ParserRuleContext::is(child)) {
            std::string childName = getRuleName(child, parser);
            if (childName == "frac") {
                LATEXParser::FracContext *frac = static_cast<LATEXParser::FracContext *>(child);
                Json::Value childNode = fracToJsonTree(frac, parser);
                node[childName] = childNode;
            } else if (childName == "func") {
                LATEXParser::FuncContext *func = static_cast<LATEXParser::FuncContext *>(child);
                Json::Value childNode = funcToJsonTree(func, parser);
                node[childName] = childNode;
            } else {
                Json::Value childNode = toJsonTree(child, parser);
                if (node[childName].empty()) {
                    if (childName == "postfix"
                        || childName == "postfix_op"
                        || childName == "postfix_nofunc")
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
        }
    }

    addTokensAndErrors(node, tree, parser);

    if (name == "func_multi_arg") {
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

std::string parseToJson(const std::string &input) {
    // auto begin = high_resolution_clock::now();
    ANTLRInputStream stream(input);
    LATEXLexer lexer(&stream);
    CommonTokenStream tokens(&lexer);
    LATEXParser parser(&tokens);
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
