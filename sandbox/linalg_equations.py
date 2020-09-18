from latex2sympy import process_sympy
import sys
sys.path.append("..")

latex = "2*\\begin{pmatrix}1\\\\2\\\\3\\end{pmatrix}"
math = process_sympy(latex)
print("latex: %s to math: %s" % (latex, math))
