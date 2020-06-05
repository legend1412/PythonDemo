# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc  # 计算roc和auc
from sklearn import model_selection
from sklearn.svm import SVC

# improt some data to play with

iris = datasets.load_iris()
X = iris.data
y = iris.target

print(set(y))  # {0,1,2}

# 变为2分类
X, y = X[y != 2], y[y != 2]
# add noisy features to make the problem harder
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

# shuffle and split training and test sets
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=.3, random_state=0)
# learn to predict each class against the other
svm = svm.SVC(kernel='linear', probability=True, random_state=random_state)

# 通过decision_function() 返回wx+b 计算得到的y_score的值，用在roc_curve()函数中
# noinspection PyTypeChecker
svm_model: SVC = svm.fit(X_train, y_train)
y_score = svm_model.decision_function(X_test)

# compute ROC curve and ROC area for each class
# fp rate:原本是错的，预测是对的比例（越小越好，0是理想）
# tp rate:原本是对的，预测是对的比例（越大越好，1是理想）
# 分类别0,1   0.36<0.5=>0
fpr, tpr, threashold = roc_curve(y_test, y_score)
roc_auc = auc(fpr, tpr)
print(roc_auc)

# plt.figure()
lw = 2
plt.figure(figsize=(8, 8))
# 假正率为横坐标，真正率为纵坐标做曲线
plt.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receviver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
