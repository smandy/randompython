import math
import builtins

from sympy import *
x  = symbols('x')

#from sympy import simplify

# simplify( ( x*x - 2 ) / ( 2 * x))

x = 1.5

EPSILON = 1.0e-12

while True:
    newX = (x / 2.0 + 1 / x)
    print(f"new={newX:4f} old={x:4f} diff={newX-x}")
    if builtins.abs( newX -x )<=EPSILON:
        break
    x = newX

