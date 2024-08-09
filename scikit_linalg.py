
import numpy as np

np.c_[np.array([1,2,3]), np.array([4,5,6])]
#array([[1, 4],
#           [2, 5],
#           [3, 6]])

b1 = np.c_[np.array([[1,2,3]]), 0, 0, np.array([[4,5,6]])]
    #array([[1, 2, 3, ..., 4, 5, 6]])


np.r_['-1', np.array([1,2,3]), np.array([4,5,6])]


X = 2 * np.random.rand(100,1)
y = 4 + 3 * X + np.random.randn(100,1)

clf()
plot(X,y, 'bx')
#plt.scatter(X,y, 'bx')

X_b = np.c_[ np.ones((100,1)), X]

theta = np.linalg.inv( X_b.T.dot(X_b)).dot(X_b.T).dot(y)

X_new = np.array([ [0], [2]])
X_new_b = np.c_[ np.ones((2,1)), X_new]
y_predict = X_new_b.dot(theta)
plot( X_new, y_predict, 'r-')
