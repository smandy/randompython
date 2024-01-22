import numpy as np



from math import pi
import cmath

twopi = 2 * pi

twopij = complex( 0, twopi)

degs = linspace( 0, twopi, 200, endpoint = True)


zs = np.exp(degs * twopij)

clf()
grid(True)

scatter(zs.real, zs.imag, marker = 'x')



