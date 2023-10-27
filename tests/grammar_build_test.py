import os
import hashlib


def test_ensure_grammar_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../LATEX.g4', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == 'a5c8dce931b0479d4fa62f454fba166bdf7564b847ebe0b7693838cc722cb857', \
        'LATEX.g4 has changed. Please run the compile.sh script for all architectures then update the hash' + \
        f'in this test to {file_hash}'


def test_ensure_cpp_file_is_built():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    grammar_file = open(f'{tests_dir}/../src/latex2sympy/latex2antlrJson.cpp', 'r')
    h = hashlib.new('sha256')
    h.update(grammar_file.read().encode('utf-8'))
    grammar_file.close()
    file_hash = h.hexdigest()
    assert file_hash == '027382d064898632608ffeffc5f5f34230f8a4e92865fd1994ae4f064618534c', \
        'latex2antlrJson.cpp has changed. Please run the compile.sh script for all architectures then update the hash' + \
        f'in this test to {file_hash}'
