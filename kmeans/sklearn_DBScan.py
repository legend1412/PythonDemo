import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
# from sklearn.externals import joblib
from joblib import dump, load
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans


def getclusterdata(flag='c', ns=1000, nf=2, centers=None, cluster_std=None):
    """
    得到回归数据
    centers(簇中心的个数或者自定义的簇中心)
    cluster_std(簇数据方差代表簇的聚合程序)
    """
    if cluster_std is None:
        cluster_std = [0.4, 0.5, 0.2]
    if centers is None:
        centers = [[-1, -1], [1, 1], [2, 2]]
    if flag == 'c':
        cluster_x, cluster_y = datasets.make_circles(n_samples=ns, factor=.6, noise=.05)
    elif flag == 'b':
        cluster_x, cluster_y = datasets.make_blobs(n_samples=ns, n_features=nf, centers=centers,
                                                   cluster_std=cluster_std, random_state=9)
    else:
        cluster_x, cluster_y = datasets.make_moons(n_samples=ns, noise=0.1, random_state=1)
    return cluster_x, cluster_y


def datasplit(dataset, label, radio=0.3):
    """
    数据集分割-------训练集，测试集合
    """
    # noinspection PyBroadException
    try:
        x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size=radio)
    except Exception as e:
        print(e)
        dataset, label = np.array(dataset), np.array(label)
        x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size=radio)

    print('----------------------split_data shape--------------------------------')
    print(len(x_train), len(y_train))
    print(len(x_test), len(y_test))
    return x_train, x_test, y_train, y_test


def savemodel(model, save_path):
    """
    模型持久化存储
    """
    dump(model, save_path)
    print(u"持久化存储完成!")


def loadmodel(model_path="model.pkl"):
    """
    加载保存本地的模型
    """
    model = load(model_path)
    return model


def clustermodel(flag='c'):
    """
    Kmeans算法关键参数:
    n_clusters:数据集中类别数目
    DBSCAN算法关键参数:
    eps:DBSCAN算法参数，即我们的ε-邻域的距离阈值和样本距离超过ε的样本点不在ε-邻域内
    min_samples：DBSACN算法参数，即样本点要成为核心对象所需要的ε-邻域的样本数阈值
    """
    x, y = getclusterdata(flag=flag, ns=3000, nf=5, centers=[[-1, -1], [1, 1], [2, 2]], cluster_std=[0.4, 0.5, 0.2])
    x_train, x_test, y_train, y_test = datasplit(x, y, radio=0.3)
    # 绘图
    plt.figure(figsize=(16, 8))
    # Kmeans模型
    model = KMeans(n_clusters=3, random_state=9)
    model.fit(x_train)
    y_pred = model.predict(x_test)
    plt.subplot(121)
    plt.scatter(x_test[:, 0], x_test[:, 1], c=y_pred)
    plt.title("KMeans Cluster Result")
    # DBSCAN模型
    # 下面的程序报错：AttributError:'DBSCAN' object has no attribute 'predict'
    # model = DBSCAN(eps=0.1,min_sample=10)
    # model.fit(X_train)
    # y_pred=model.predict(X_test)
    # 改为这样的形式就可以了 moons 0.2,20,circle:0.1,7 blob:0.2,13
    y_pred = DBSCAN(eps=0.1, min_samples=4).fit_predict(x_test)
    plt.subplot(122)
    plt.scatter(x_test[:, 0], x_test[:, 1], c=y_pred)
    plt.title("DBSCAN Cluster Result")
    if flag == 'c':
        plt.savefig('circleData.png')
    elif flag == 'b':
        plt.savefig('blobData.png')
    else:
        plt.savefig('moonData.png')


if __name__ == '__main__':
    clustermodel("c")
