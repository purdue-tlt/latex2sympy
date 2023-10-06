import os
import hashlib


def test_ensure_grammar_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../LATEX.g4', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == '8532f17fe8000457059e7d1f8f7da18b73fffecf8a5b7830dab0bbb7d9f199b8', \
        'LATEX.g4 has changed. Please run the build.sh script then update the hash' + \
        f'in this test to {file_hash}'


def test_ensure_cpp_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../src/latex2sympy/latex2antlrJson.cpp', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == '0d3b8aa0570d245303392be38b73bcff8b019272e43041a170e46ee3efac9cc0', \
        'latex2antlrJson.cpp has changed. Please run the build.sh script then update the hash' + \
        f'in this test to {file_hash}'
