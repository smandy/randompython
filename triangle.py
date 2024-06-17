import numpy as np
import numpy.linalg
import math

#det = linalg.det
# file://TriangleParadox_1000.svg

t1 = [ (0,0), (8,3), (13,5), (13,0) ]
t2 = [ (0,0), (5,2), (13,5), (13,0) ]

from math import atan

RADIANS_TO_DEGREES = 180.0 / math.pi 

def calcRad(ts):
    return RADIANS_TO_DEGREES * atan(ts[1][1] / ts[1][0])

print(f"t1 angle is {calcRad(t1)}")
print(f"t2 angle is {calcRad(t2)}")
    
def roundoff(xs):
    return xs + xs[:1]

def doplot(xs, *args, **kwargs):
    plot( [ x[0] for x in xs], [x[1] for x in xs], *args, **kwargs)

doplot(roundoff(t1), 'r-x', ms = 17, mew = 3)
doplot(roundoff(t2), 'b-x', ms = 17, mew = 3)
    
def calc(xs):
    #print(f"Calc {xs}")
    x2 = roundoff(xs)
    pairs = list(zip( x2[:-1], x2[1:] ))
    #print(pairs)
    arrays = [ det(np.array(x)) for x in pairs]
    a2 = sum(arrays)
    print(f"a = {a2/2}")
    return a2/2

print(f"\nTotal is {calc(t1)-calc(t2)}")



