import pylab as pl
import numpy as np

N = 100000

def sigmoid(z):
    return 1.0 / ( 1 + np.exp(-z))

alpha = 0.0001

# Secret variables
sxs = (4 * np.random.random(N) - 2.0).reshape(N,1)
sys = (4 * np.random.random(N) - 2.0).reshape(N,1)

good = np.abs(sxs - sys) < 1
bad = np.logical_not(good)

print( np.where(good)[0].shape)
print( np.where(bad)[0].shape)

b = 0
X = np.hstack([
    sxs,
    sys,
    sxs * sxs,
    sys * sys,
    sxs * sys
])

Y = np.abs(X[:,0] - X[:,1] + 1) < 1.0
Y = Y[:,np.newaxis].astype(int)
W = np.zeros( shape = (X.shape[1], 1))

pl.figure('initial')
pl.clf()
pl.title('initial')

gidx = np.where(good)[0]
bidx = np.where(bad)[0]
pl.plot(X[gidx,0], X[gidx,1], 'rx', alpha = 0.2)
pl.plot(X[bidx,0], X[bidx,1], 'bx', alpha = 0.2)
idx = 0
pl.figure('reg')
pl.clf()

iters = 1000
images = 16
every = int(iters / images) + 1

for i in range(iters):
    # print("Iter %s" % i)
    z = X.dot(W) + b
    a = sigmoid(z)
    J = - (Y * np.log( a ) + (1 - Y) * np.log( 1 - a ))
    dz = a - Y
    W -= alpha * dz.T.dot(X).T
    b -= alpha * dz.sum()
    if i % every == 1:
        print("iter %s J is %s" % (i, J.sum()))
        idx += 1
        pl.subplot(4,4,idx)
        y = "My fit %s" % i
        # pl.figure(y)
        pl.title(y)
        good = (a>0.5)[:,0]
        bad = (a<0.5)[:,0]
        pl.plot(X[good,0], X[good,1], 'rx', alpha=0.2)
        pl.plot(X[bad,0], X[bad,1], 'bx', alpha=0.2)

pl.figure('final')        
pl.plot(X[good,0], X[good,1], 'rx', alpha=0.02)
pl.plot(X[bad,0], X[bad,1], 'bx', alpha=0.02)
