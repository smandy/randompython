# nth roots of unity / complex numbers

from math import *
from cmath import *

import pylab as pl

tpi = 2 * pi * 1j

def unityroots(n):
    return [ exp( tpi * (x/n)) for x in range(n) ]
 
def nthroots(z, n):
    rn = np.abs(z)
    r = np.power(rn, 1.0 / n)
    thetan = np.angle( z)
    theta = thetan / n
    print( f"thetan={thetan} theta={theta}")
    return [ r * exp( 1j * theta) * x for x in unityroots(n) ]

    
def doplot(ns, *args, **kwargs):
    xs = [ real(x) for x in ns ] + [ real(ns[0])]
    ys = [ imag(x) for x in ns ] + [ imag(ns[0])]
    # print(xs)
    # print(ys)
    pl.plot( xs, ys, *args, **kwargs)
    
pl.clf()
pl.grid(True)

circle = [ 1 * exp( tpi * n) for n in np.linspace(0.0,1.0,50, endpoint = False) ]

doplot(circle)

if 0:
    for i in range(5,6):
        doplot(unityroots(i), 'rx-', ms = 20, mew=3)


for theta in np.linspace( 0.0, 2 * math.pi / 2, 5):
    doplot(nthroots( 1 * exp( 1j * theta), 5), 'rx-', ms=20, mew = 3)

    

