import os
import hashlib


def test_ensure_grammar_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../LATEX.g4', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == '1ccb60dd2978bc41f945ce94bc099e729750106d58c7772544426a4c1628359c', \
        'LATEX.g4 has changed. Please run the compile.sh script for all architectures then update the hash' + \
        f' in this test to {file_hash}'


def test_ensure_cpp_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../src/latex2sympy/latex2antlrJson.cpp', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == 'ba2d9a6efb73422a596aa6ea50c0bc9967ddae6a98fc6674bdababeefd254861', \
        'latex2antlrJson.cpp has changed. Please run the compile.sh script for all architectures then update the hash' + \
        f' in this test to {file_hash}'
