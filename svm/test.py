from svm.svmMLiA import *
from numpy import *
import numpy as np
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt

data_mat, label_mat = load_data_set('testSet.txt')
print(label_mat)
print(len(label_mat))
print(mat(zeros((10, 1))))

x1 = np.arange(3.0).reshape((3, 1))
"""
[[0.1.2.]
 [3.4.5.]
 [6.7.8.]]
"""
print(x1)
# [0.1.2.]
x2 = np.arange(3.0)
print(x2)
x = np.multiply(mat(zeros((len(label_mat), 1))), label_mat)
print(x)
print(x.shape)

print(np.multiply(x1, x2))
"""
[[0.1.4.]
 [0.4.10.]
 [0.7.16.]]
"""
test_rbf()
a = mat([[0, 1], [2, 3]])
print(a.shape)
print(a.A.shape)

b, alphas = smo_simple(data_mat, label_mat, C=0.6, toler=0.001, max_iter=40)
print('b:', b)
print('alphas:', alphas)
print('alphas[alphas>0]:', alphas[alphas > 0])

data = load_breast_cancer()
x = data.data
print(x.shape)
y = data.target
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.show()
