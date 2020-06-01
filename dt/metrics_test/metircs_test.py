import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score

y_pred = [0, 2, 1, 3]
y_true = [0, 1, 2, 3]
print("accuracy_score:", accuracy_score(y_true, y_pred))

y_pred = [0, 0, 2, 2, 0, 2]
y_true = [2, 0, 2, 2, 0, 1]
print("confusion_matrix:", confusion_matrix(y_true, y_pred))

# 0 1 2
# 0[[2 0 0]
# 1[0 0 1]
# 2[1 0 2]]

y_pred = [0, 1, 0, 1, 0, 1, 0, 1]
y_true = [0, 0, 0, 1, 1, 1, 1, 1]
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(tn, fp, fn, fp)  # (2,1,2,3)
