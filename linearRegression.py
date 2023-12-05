import scipy.io as sio
import numpy as np
import pylab as pl
from numpy.linalg import pinv

repos = '/home/andy/repos'
pt2 = 'machinelearning/machine-learning-ex5'

xs = sio.loadmat(f'{repos}/{pt2}/ex5/ex5data1.mat', matlab_compatible=True)
# x0 = np.matrix(xs['X'])
# y0 = np.matrix(xs['y'])

pl.figure('regression')
pl.clf()
N = 1000

x = np.linspace(1, 20, N)
y = 10 + 2 * x + 3 * pl.randn(N)

x0 = np.matrix(x).reshape(N, 1)
y0 = np.matrix(y).reshape(N, 1)

X = np.hstack([np.ones(shape=(len(x0), 1)), x0])
theta = pinv(X.T * X) * X.T * y0

r = X * theta

a = [True, False][0]
if a:
    pl.clf()
    pl.grid(True)
    pl.plot(x0, y0, 'bx')
    pl.plot(x0, X * theta, 'r-', lw=10)


# (expt k (/ (log n k) k )) )
# \( \displaystyle D = K^{\frac{1}{K} * log_{K}(N)}  \)
