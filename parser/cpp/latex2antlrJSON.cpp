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

Json::Value toJsonTree(tree::ParseTree *tree, LATEXParser *parser) {
    const std::vector<std::string> ruleNames = parser->getRuleNames();

    Json::Value node;
    std::string name;
    if (RuleContext::is(tree)) {
        RuleContext *ruleContext = static_cast<RuleContext *>(tree);
        int ruleIndex = ruleContext->getRuleIndex();
        name = ruleNames[ruleIndex];
    } else if (tree::ErrorNode::is(tree)) {
        tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
        Token* token = terminalNode->getSymbol();
        if (token) {
            node["error"] = token->getText();
        } else {
            node["error"] = token->toString();
        }
    } else if (tree::TerminalNode::is(tree)) {
        tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
        Token* token = terminalNode->getSymbol();
        if (token) {
            node["text"] = token->getText();
            node["type"] = (int)token->getType();
        } else {
            node["type"] = "-1";
        }
    }

    int childrenCount = tree->children.size();
    if (childrenCount == 0) {
        return node;
    }

    if (childrenCount == 1 && name != "postfix" && name != "postfix_no_func" && name != "postfix_op") {
        node[name] = toJsonTree(tree->children[0], parser);
        return node;
    }

    Json::Value children;
    for (int i = 0; i < childrenCount; i++) {
        tree::ParserTree *childTree = tree->children[i];
        Json::Value childNode = toJsonTree(childTree, parser);
    }
    node[name] = children;

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
