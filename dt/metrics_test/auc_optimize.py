import numpy as np
from sklearn.metrics import roc_curve, auc


# 公式：根据预测概率排序之后
# 公式的分母计算规则，处理正样本之前，先计算已经有多少个负样本个数，将负样本累加再做计算
def auc_calculate(labels, preds, n_bins=100):
    postive_len = sum(labels)  # 正样本数量（因为正样本都是1）
    negative_len = len(labels) - postive_len  # 负样本数量
    total_case = postive_len * negative_len  # 正负样本对
    pos_histogram = [0 for _ in range(n_bins)]
    neg_histogram = [0 for _ in range(n_bins)]
    bin_width = 1.0 / n_bins
    for i in range(len(labels)):
        nth_bin = int(preds[i] / bin_width)
        # print(nth_bin)
        if labels[i] == 1:
            pos_histogram[nth_bin] += 1
        else:
            neg_histogram[nth_bin] += 1
    # print("pos_histogram:", pos_histogram)
    # print("neg_histogram:", neg_histogram)
    # 累加负样本个数
    accumulated_neg = 0
    # 满足正负样本pair的个数
    satisfied_pair = 0
    for i in range(n_bins):
        satisfied_pair += (pos_histogram[i] * accumulated_neg + pos_histogram[i] * neg_histogram[i] * 0.5)
        accumulated_neg += neg_histogram[i]
    return satisfied_pair / float(total_case)


# （sum（正样本的index）-（正样本个数（正样本个数+1））/2）/正负样本对个数
def auc_calculate1(labels, preds):
    postive_len = sum(labels)  # 正样本数量（因为正样本都是1）
    negative_len = len(labels) - postive_len  # 负样本数量
    total_case = postive_len * negative_len  # 正负样本对
    # 先要对样本进行排序，升序排列
    for i in range(len(preds)):
        for j in range(i + 1, len(preds)):
            if preds[i] > preds[j]:
                preds[i], preds[j] = preds[j], preds[i]
                labels[i], labels[j] = labels[j], labels[i]
            if preds[i] == preds[j]:
                if labels[i] == 0 and labels[j] == 1:
                    labels[i], labels[j] = labels[j], labels[i]

    # print(preds)
    # print(labels)
    # 正样本索引和
    sump = 0
    for i in range(len(labels)):
        if (i + 1) < len(labels):
            if preds[i] == preds[i + 1]:
                if labels[i] == 1 and labels[i + 1] == 1:
                    sump += (i + 1)
                    continue
                elif labels[i] == 0 and labels[i + 1] == 0:
                    continue
                else:
                    sump += (2 * i + 3) / 2
                    continue
        if labels[i] == 1:
            sump += (i + 1)
    # print(sump)
    return (sump - postive_len * (postive_len + 1) / 2) / float(total_case)


if __name__ == '__main__':
    y = np.array([1, 1, 0, 0, 1, 1, 1, 0])
    pred = np.array([0.9, 0.8, 0.3, 0.1, 0.4, 0.8, 0.66, 0.7])
    # y = np.array([0, 1, 0, 1, 1])
    # pred = np.array([0.3, 0.3, 0.4, 0.8, 0.9])
    fpr, tpr, thresholds = roc_curve(y, pred, pos_label=1)
    print("sklearn:", auc(fpr, tpr))
    print("验证:", auc_calculate(y, pred))
    print("验证1:", auc_calculate1(y, pred))
    # print(auc_calculate([1,0],[0.9,0.8]))
