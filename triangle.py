import numpy as np
import numpy.linalg
from math import atan, pi
from numpy.lib.stride_tricks import sliding_window_view

det = linalg.det
# file://TriangleParadox_1000.svg

def roundoff(xs):
    return np.vstack( (xs, [xs[0]]))

t1 = roundoff(np.array([ (0,0), (8,3), (13,5), (13,0) ]))
t2 = roundoff(np.array([ (0,0), (5,2), (13,5), (13,0) ]))

#t12 = np.array([ (0,0), (8,3), (13,5), (13,0) ])
RADIANS_TO_DEGREES = 180.0 / pi 

def calcRad(ts):
    return RADIANS_TO_DEGREES * atan(ts[1][1] / ts[1][0])

print(f"t1 angle is {calcRad(t1)}")
print(f"t2 angle is {calcRad(t2)}")
    

def doplot(xs, *args, **kwargs):
    plot( [ x[0] for x in xs], [x[1] for x in xs], *args, **kwargs)

doplot(roundoff(t1), 'r-x', ms = 17, mew = 3)
doplot(roundoff(t2), 'b-x', ms = 17, mew = 3)
    
def calc(xs):
    #pairs = list(zip( x2[:-1], x2[1:] ))
    #print(pairs)
    x3 = sliding_window_view(xs, 2,0)
    print(f"x3 = {x3} shape={x3.shape} det={det(x3)}")
    #arrays = det(xs)
    a2 = sum(det(x3))
    print(f"a = {a2/2}")
    return a2/2

print(f"\nTotal is {calc(t1)-calc(t2)}")



