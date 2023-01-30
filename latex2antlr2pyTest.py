from parser.cpp.build.lib.latex2antlrJson import parseToJson
import json

json_string = parseToJson('x_{1}!')
print(json_string)
# math_json = json.loads(json_string)
# print(math_json)
