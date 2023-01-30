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

// std::string getJsonNodeName(tree::ParseTree *tree, LATEXParser *parser) {
//     const std::vector<std::string> ruleNames = parser->getRuleNames();
//     const dfa::Vocabulary vocab = parser->getVocabulary();
//     if (RuleContext::is(tree)) {
//         RuleContext *ruleContext = static_cast<RuleContext *>(tree);
//         int ruleIndex = ruleContext->getRuleIndex();
//         return ruleNames[ruleIndex];
//     } else if (tree::ErrorNode::is(tree)) {
//         tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
//         Token* token = terminalNode->getSymbol();
//         if (token) {
//             return token->getText();
//         }
//         return "error";
//     } else if (tree::TerminalNode::is(tree)) {
//         tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
//         Token* token = terminalNode->getSymbol();
//         if (token) {
//             return token->toString();
//         }
//         return "-1";
//     }
//     return "";
// }

// Json::Value toJsonTree(tree::ParseTree *tree, LATEXParser *parser) {
//     const std::vector<std::string> ruleNames = parser->getRuleNames();

//     Json::Value node;
//     std::string name;
//     if (RuleContext::is(tree)) {
//         RuleContext *ruleContext = static_cast<RuleContext *>(tree);
//         int ruleIndex = ruleContext->getRuleIndex();
//         name = ruleNames[ruleIndex];
//     } else if (tree::ErrorNode::is(tree)) {
//         tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
//         Token* token = terminalNode->getSymbol();
//         if (token) {
//             node["error"] = token->getText();
//         }
//         node["error"] = token->toString();
//     } else if (tree::TerminalNode::is(tree)) {
//         tree::TerminalNode *terminalNode = static_cast<tree::TerminalNode *>(tree);
//         Token* token = terminalNode->getSymbol();
//         if (token) {
//             node["text"] = token->getText();
//             node["type"] = std::to_string((int)token->getType());
//             node["line"] = std::to_string((int)token->getLine());
//         }
//     }

//     int childrenCount = tree->children.size();
//     if (childrenCount == 0) {
//         return node;
//     }
//     if (childrenCount == 1) {
//         node[name] = toJsonTree(tree->children[0], parser);
//         return node;
//     }
//     Json::Value children;
//     for (int i = 0; i < childrenCount; i++) {
//         children.append(toJsonTree(tree->children[i], parser));
//     }
//     node[name] = children;
//     return node;
// }

// std::string toJsonString(tree::ParseTree *tree, LATEXParser *parser) {
//     Json::Value root = toJsonTree(tree, parser);
//     Json::FastWriter fastWriter;
//     std::string json = fastWriter.write(root);
//     return json;
// }

Json::Value convertMp(LATEXParser::MpContext *mp) {
    Json::Value node;

    // if (mp->mp()) {

    // } else {

    // }

    return node;
}

Json::Value convertAdditive(LATEXParser::AdditiveContext *add) {
    Json::Value node;

    if (add->ADD()) {
        Json::Value lh = convertRelation(add->additive()[0]);
        Json::Value rh = convertRelation(add->additive()[1]);

    } else if (add->SUB()) {
        Json::Value lh = convertRelation(add->additive()[0]);
        Json::Value rh = convertRelation(add->additive()[1]);

    } else {
        return convertMp(add->mp());
    }

    return node;
}

Json::Value convertExpr(LATEXParser::ExprContext *expr) {
    return convertAdditive(expr->additive());
}

Json::Value convertRelation(LATEXParser::RelationContext *relation) {
    if (relation->expr())
        return convertExpr(relation->expr());

    Json::Value node;
    Json::Value lh = convertRelation(relation->relation()[0]);
    Json::Value rh = convertRelation(relation->relation()[1]);
    node["lh"] = lh;
    node["rh"] = rh;
    if (relation->LT())
        node["type"] = "LT";
    if (relation->GT())
        node["type"] = "GT";
    if (relation->GTE())
        node["type"] = "GTE";
    if (relation->EQUAL())
        node["type"] = "EQUAL";
    if (relation->UNEQUAL())
        node["type"] = "UNEQUAL";
    return node;
}

Json::Value convertRelationList(LATEXParser::Relation_listContext *relationList) {
    Json::Value array;
    std::vector<LATEXParser::RelationContext *> relations = relationList->relation_list_content()->relation();
    for (LATEXParser::RelationContext *relation: relations) {
        array.append(convertRelation(relation));
    }
    return array;
}

Json::Value convertMath(LATEXParser::MathContext *math) {
    Json::Value root;
    if (math->relation_list()) {
        root["relation_list"] = convertRelationList(math->relation_list());
    } else {
        root["relation"] = convertRelation(math->relation());
    }
    return root;
}

int parse(const std::string &input) {
    auto begin = high_resolution_clock::now();

    ANTLRInputStream stream(input);
    LATEXLexer lexer(&stream);
    CommonTokenStream tokens(&lexer);
    LATEXParser parser(&tokens);
    LATEXParser::MathContext *math = parser.math();

    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - begin);

    std::cout << math -> toStringTree(&parser, true) << std::endl;
    std::cout << "Elapsed Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    begin = high_resolution_clock::now();

    // std::string jsonString = toJsonString(math, &parser);

    Json::Value json = convertMath(math);
    Json::FastWriter fastWriter;
    std::string jsonString = fastWriter.write(json);

    std::cout << jsonString << std::endl;

    end = high_resolution_clock::now();
    duration = duration_cast<microseconds>(end - begin);

    std::cout << "Elapsed Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    return 0;
}

namespace py = pybind11;

PYBIND11_MODULE(latex2antlr2py, m) {
    m.doc() = "pybind11 latex2antlr2py plugin"; // optional module docstring
    m.def("parse", &parse, "A function which parses latex");
}
