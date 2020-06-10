import numpy as np
import matplotlib.pyplot as plt

# 初始化x和y，x：data，y对应label
datainit = []
labelinit = []

fr = open('../data/testSet.txt')
for line in fr.readlines():
    line = line.strip().split()
    # 每条样本加了一维都为1
    datainit.append([1.0, float(line[0]), float(line[1])])
    labelinit.append(int(line[-1]))


# print(data)  # [[1.0, -0.017612, 14.053064], [1.0, -1.395634, 4.662541],...]
# print(label)  # [0, 1, 0, 0, 0, 1, 0, 1,...]


# 画图 将样本点画出来
def plot_function(data, label, weights=None):
    # np是numpy的别名，获取data样本数量
    k = np.shape(data)[0]
    # 坐标x1，y1存标签为1的，坐标x2，y2存标签为0的
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for j in range(k):
        if int(label[j]) == 1:
            x1.append(data[j][1])
            y1.append(data[j][2])
        else:
            x2.append(data[j][1])
            y2.append(data[j][2])
    fig = plt.figure()
    # title
    ax = fig.add_subplot(111)
    ax.scatter(x1, y1, s=100, c='red', marker='s')
    ax.scatter(x2, y2, s=100, c='black')
    if weights is not None:
        x = np.arange(-3.0, 3.0, 0.1)
        y = -(weights[0] + weights[1] * x) / weights[2]  # x2=-(w1x1+w[0])/w2
        ax.plot(x, y)
        plt.xlabel('X1')
        plt.ylabel('X2')
    plt.show()


# 定义sigmoid函数，t传入wx
def sigmoid(t):
    return 1.0 / (1 + np.exp(-t))


data2 = np.mat(datainit)  # 100*3 X 矩阵，把datainit中进行变换,100是数据条数，3是每条数据的数量
# print(data2)
label2 = np.mat(labelinit).transpose()  # 转置 100*1
# print(label2)
m, n = np.shape(data2)  # 100,3

# 梯度下降法
# 参数初始化
alpha = 0.001  # 步长
maxiter = 10000
weight = np.ones((n, 1))  # 3*1，w1<=>b
# print(weight)

# 记录迭代次数
i = 0
# 记录损失
loss_lst = []
iter_num = []
loss = None

while i < maxiter:  # 1终止条件 达到最大迭代次数跳出循环
    eta = sigmoid(data2 * weight)  # data:100*3,wight:3*1=100*1
    loss_new = -label2.T * np.log(eta) - (np.ones((m, 1)).T - label2.T) * np.log(1 - eta)

    if loss is None:  # 当loss没有值的时候赋值为当前loss（1_wx）
        loss = loss_new
    elif np.abs(loss - loss_new) < 1e-3:  # 2终止条件 损失函数变化不大的时候跳出循环
        break
    else:
        loss = loss_new

    # 记录loss
    if i < 300:
        loss_lst.append(loss.tolist()[0][0])
        iter_num.append(i)
    # eta为预测出来的值-样本真实值
    error = eta - label2
    # 梯度公式
    grad = data2.T * error
    # 权重更新公式 w_new = w+c*dir
    weight += alpha * (-grad)
    i += 1
    print('step', i, 'loss', loss_new)

print(weight.T.tolist()[0])
# 只打印数据点
# plot_function(datainit, labelinit)
# 打印数据点和模型直线
plot_function(datainit, labelinit, weight.T.tolist()[0])
