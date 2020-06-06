import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score

y_pred = [0, 2, 1, 3]
y_true = [0, 1, 2, 3]
print("accuracy_score:", accuracy_score(y_true, y_pred))

y_pred = [0, 0, 2, 2, 0, 2]
y_true = [2, 0, 2, 2, 0, 1]
print("confusion_matrix:\r\n", confusion_matrix(y_true, y_pred))

# 0 1 2
# 0[[2 0 0]
# 1[0 0 1]
# 2[1 0 2]]

y_pred = [0, 1, 0, 1, 0, 1, 0, 1]
y_true = [0, 0, 0, 1, 1, 1, 1, 1]
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print("tn, fp, fn, tp:", tn, fp, fn, fp)  # (2,1,2,3)


def calcauc(labels, probs):
    n = 0
    p = 0
    neg_prob = []
    pos_prob = []
    for index, label in enumerate(labels):
        if label == 1:
            p += 1
            pos_prob.append(probs[index])
        else:
            n += 1
            neg_prob.append(probs[index])

    # 公式需要满足：预测得到正样本的概率大于负样本的概率0,1  1:0.8>0:0.1 p(y=1|x)=0.9 y=0
    # 一共有N*P对样本，（一对样本即一个正样本和一个负样本）
    # 统计这N*P对样本里，正样本的预测概率大于负样本的预测概率的个数
    number = 0
    for pos in pos_prob:
        for neg in neg_prob:
            # 正样本概率>负样本 1
            if pos > neg:
                number += 1
            # 正样本和负样本概率一样 0.5
            elif pos == neg:
                number += 0.5
            # 还有没写的，当负样本概率>正样本 0，不就不需要加
    return number / (n * p)


y = np.array([1, 0, 0, 0, 1, 0, 1, 0])
pred = np.array([0.9, 0.8, 0.3, 0.1, 0.4, 0.9, 0.66, 0.7])
print('auc=', calcauc(y, pred))
print('roc_auc=', roc_auc_score(y, pred))

'''
优化下循环，扫描一次数据，进行排序，把正样本拿出来
A 0 0.1
C 1 0.3
B 0 0.4
D 1 0.8
E 1 0.9
C,D,E

2+4+5=>A+C+A+B+C+D+A+B+C+D+E=>1+2+3=>C,C,D,C,D,E(A,A,B,A,B)  
1+2+3+4=>4*(4+1)/2=10
两层for循环，找规律变成一次循环 正样本个数P
((2+4)-(p(p+1)/2))/n*p=正样本>负样本的个数 n(n+1)/2
'''
y = np.array([0, 1, 0, 1, 1])
pred = np.array([0.1, 0.3, 0.4, 0.8, 0.9])
print('auc=', calcauc(y, pred))
print('roc_auc=', roc_auc_score(y, pred))
