import latex2sympy

a = "1+2-3+\\frac{4}{5}+6^7+\sqrt{5}+6+\\variable{DEMO_{a,b,c}}"

b = latex2sympy.process_sympy(a)
print(b)
for i in b.free_symbols:
	print(i)
