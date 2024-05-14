from scipy import stats
import pylab as pl
import numpy as np
x = pl.linspace(0,1000, 1000,endpoint = True)
clf()

for i, v in enumerate(pl.linspace(0, 0.01, 9)):
#v = 0.02
    print( (i,v))

    pl.subplot( 3,3 , i + 1)
    y = v * x + ( 1.0 - v) * pl.randn(1000)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    
    plot(x,y, 'bx')
    plot(x, x * slope + intercept, 'r-', lw = 3)
    title( f"i={i} v={v} p={p_value:.3f}\nr={r_value:.2f} s={slope:.3f}")

    
