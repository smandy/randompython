# nth roots of unity / complex numbers

from math import *
from cmath import *

import pylab as pl

tpi = 2 * pi * 1j

def unityroots(n):
    return [ exp( tpi * (x/n)) for x in range(n) ]
 
def nthroot(z):
    pass

    
def doplot(ns, *args, **kwargs):
    xs = [ real(x) for x in ns ] + [ real(ns[0])]
    ys = [ imag(x) for x in ns ] + [ imag(ns[0])]
    #print(xs)
    #print(ys)
    pl.plot( xs, ys, *args, **kwargs)
    
pl.clf()
pl.grid(True)

circle = [ exp( tpi * n) for n in np.linspace(0.0,1.0,50, endpoint = False) ]

doplot(circle)

for i in range(5,6):
    doplot(unityroots(i), 'rx-', ms = 20, mew=3)

