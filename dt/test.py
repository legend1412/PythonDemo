import os
import pydotplus
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from IPython.display import Image
import numpy as np

iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=2018)

clf = DecisionTreeClassifier(criterion="gini", splitter="best", max_depth=None, min_samples_split=2,
                             min_samples_leaf=1, min_weight_fraction_leaf=0., max_features=None,
                             random_state=None, max_leaf_nodes=None, class_weight=None, presort=None)

dt_model = clf.fit(X_train, y_train)
print(cross_val_score(clf, iris.data, iris.target, cv=10))

dot_data = tree.export_graphviz(dt_model, out_file='tree.dot', feature_names=iris.feature_names,
                                class_names=iris.target_names, filled=True, rounded=True,
                                special_characters=True)
print(dot_data)

os.environ["PATH"] += os.pathsep + 'D:\\'
graph = pydotplus.graph_from_dot_data(dot_data)
# graph = pydotplus.graph_from_dot_file('tree.dot')
Image(graph.create_png())
# graph.write_pdf("wine.pdf")

a = (0, 0)
b = (1, -1)

print(max(a, b))

# .npy文件是numpy专用的二进制文件
arr = np.array([[1, 2], [3, 4]])

# 保存.npy文件
np.save("../data/test.npy", arr)
print("save .npy done")

# 读取.npy文件
print(np.load("../data/test.npy"))
print("load .npy done")
