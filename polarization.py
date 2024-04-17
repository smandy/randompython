# Try to get intuition around horizontal/circular + elliptical polarisation

import numpy as np

from math import pi
import cmath

twopi = 2 * pi

twopij = complex( 0, twopi)

degs = linspace( 0, twopi, 200, endpoint = True)

clf()

for i in range(9):
    subplot( 3,3, i+1)
    grid(True)
    
    phi = i * pi / 4.0
    phi = i * pi / 16.0

    xs = sin(degs + phi)
    ys = sin(degs)
    title(f"{i} π / 4")

    offset = 10

    lw = 8
    
    plot( xs[:66-offset], ys[:66-offset], 'b-', lw=lw)
    plot( xs[66:133-offset], ys[66:133-offset], 'r-', lw = lw)
    plot( xs[133:-offset], ys[133:-offset], 'm-', lw = lw)




