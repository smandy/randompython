import pylab as pl
import numpy as np

# Logistic regression - think I did this at dublin airport.

pl.figure()

N = 10000

def sigmoid(z):
    return 1.0 / ( 1 + np.exp(-z))

alpha = 0.001

xs = pl.randn(N)
ys = pl.randn(N)
good = np.abs(xs - ys) < 1
bad = np.logical_not(good)

print(np.where(good)[0].shape)
print(np.where(bad)[0].shape)

b = 0
X = np.vstack( [xs, ys, xs * xs, ys * ys, xs * ys ] ) #, xs * xs * xs, ys * ys * ys])
Y = np.abs(X[0] - X[1]) < 1
Y = Y[np.newaxis,:].astype(int)
W = np.zeros( shape = (X.shape[0], 1))

#gi = Y[0,:]==1
#bi = Y[0,:]==0

pl.plot(X[0,good], X[1,good], 'rx')
pl.plot(X[0,bad], X[1,bad], 'bx')

for i in range(10000):
    z = W.T.dot( X ) + b
    a = sigmoid(z)
    J = - (Y * np.log( a ) + (1 - Y) * np.log( 1 - a ))
    if i % 100 == 0:
        print("iter %s J is %s" % (i, J.sum()))
    dz = a - Y
    W -= alpha * X.dot(dz.T)
    b -= alpha * dz.sum()
    #print(W)

pl.figure()
pl.title("My fit")

good = (a>0.5)[0,:]
bad = (a<0.5)[0,:]
pl.plot(X[0,good], X[1,good], 'rx')
pl.plot(X[0,bad], X[1,bad], 'bx')
    
