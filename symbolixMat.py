

from sympy import MatMul, MatrixSymbol
from sympy import expand, factor, symbols

A = MatrixSymbol('A', 3, 3)
y = MatrixSymbol('y', 3, 1)
x = (A.T*A).I * A * y

A = MatrixSymbol('A', 5, 4)
B = MatrixSymbol('B', 4, 3)
C = MatrixSymbol('C', 3, 6)
d = MatMul(A, B, C)

A = MatrixSymbol('A', 1, 3)
B = MatrixSymbol('B', 3, 1)
d = MatMul(A,B)
e = MatMul(B, A)


x, y = symbols('x y')
c = x*x + 2*x *y + y * y

d = factor(c)
print(d)

f = expand(d)
print(f)


