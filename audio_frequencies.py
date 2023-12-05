import pylab as pl
import numpy as np

print()
print()

xs = np.arange(0,37).reshape(37,1)
ys = 2 **  (xs / 12.0)

pl.clf()    
pl.plot(xs, ys, 'bo-', ms = 5.0)
