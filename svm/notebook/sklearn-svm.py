from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from time import time
import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler

data = load_breast_cancer()
x = data.data
y = data.target
print(x.shape)
print(np.unique(y))
plt.scatter(x[:, 0], x[, :1], c=y)
plt.show()

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=2019)
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for kernel in kernels:
    time0 = time()
    clf = SVC(kernel=kernel, gamma='auto', degree=1, cache_size=5000)
    clf.fit(X_train, y_train)
    print('The accuracy under kernel %s is %f' % (kernel, clf.score(X_test, y_test)))
    print(datetime.datetime.fromtimestamp(time() - time0).strftime('%M:%S:%F'))

# 探索下数据（数据量纲不统一，数据分布式偏态的）
data = pd.DataFrame(x)
print(data.describe([0.01, 0.05, 0.1, 0.25, 0.5, 0.78, 0.9, 0.99]).T)
# 数据标准化，（压缩到0-1之间服从正态分布）
x = StandardScaler().fit_transform(x)
data = pd.DataFrame(x)
print(data.describe([0.01, 0.05, 0.1, 0.25, 0.5, 0.78, 0.9, 0.99]).T)

X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.3, random_state=2019)
for kernel in kernels:
    time0 = time()
    clf = SVC(kernel=kernel,gamma='autp',degree=1,cache_size=5000)
    clf.fit(X_train,y_train)
    print('The accuracy under kernel %s is %f' % (kernel, clf.score(X_test, y_test)))
    print(datetime.datetime.fromtimestamp(time() - time0).strftime('%M:%S:%F'))

#简单gamma调参
score=[]
gamma_range=np.logspace(-10,1,50)
print('gamma_range:',gamma_range)
for i in gamma_range:
    clf_new = SVC(kernel='rbf',gamma=i,cache_size=5000)
    clf_new.fit(X_train,y_train)
    score.append(clf_new.score(X_test,y_test))
print(max(score),gamma_range[score.index(max(score))])
plt.plot(gamma_range,score)
plt.show()

#linear c 调参
score=[]
C_range= np.linspace(0.001,30,50)
for i in C_range:
    clf = SVC(kernel='linear',C=i,cache_size=5000)
    clf.fit(X_train,y_train)
    score.append(clf.score(X_test,y_test))
print(max(score),C_range[score.index(max(score))])
plt.plot(C_range,score)
plt.show()

# rbf c调参
score = []
RBF_range = np.linspace(0.001,30,50)
for i in RBF_range:
    clf = SVC(kernel='rbf',C=i,cache_size=5000)
    clf.fit(X_train,y_train)
    score.append(clf.score(X_test,y_test))
print(max(score),RBF_range[score.index(max(score))])
plt.plot(RBF_range,score)
plt.show()

# 进一步调参 4-5 3.5306122448979593
score = []
N_range = np.linspace(3,5,50)
for i in N_range:
    clf = SVC(kernel='rbf',gamma=0.007196856730011514,C=i,cache_size=5000)
    clf.fit(X_train,y_train)
    score.append(clf.score(X_test,y_test))
print(max(score),N_range[score.index(max(score))])
plt.plot(N_range,score)
plt.show()
