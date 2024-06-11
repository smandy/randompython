from sympy import *
x  = symbols('x')
import numpy as np
import pylab as pl

simp = simplify( (2 * x ** 2 - x - 15) / ( x**2 - 9 ))

def doit(x):
    return (2 * x ** 2 - x - 15) / ( x**2 - 9 )

clf()
xs = np.linspace(-5, 0, 100)
pl.plot(xs, doit(xs))
