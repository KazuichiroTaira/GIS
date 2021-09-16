import numpy as np
from sklearn.neighbors import KDTree

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

print(X.shape)

tree = KDTree(X)

print(X[0].shape)
print(np.array([0.4, 0.2]).shape)
x = np.array([[0.4, 0.2], ])
dist, ind = tree.query(x, k=3)

print(dist[0])

print(ind[0])