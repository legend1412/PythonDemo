# -*- conding:UTF-8 -*-
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from sklearn.preprocessing import StandardScaler


# D(x)=(max-min)^2/12,均值：0，方差为(min+max)/2 [-sqrt(6/(max+min),sqrt(6/(max+min)))]
# 目标是要学习w（权重），快速求解w的值，做了简单w的初始化
# 1、层数多的时候，梯度会消失，w更新不大
# 2、zero初始化，学习起来相对比较慢
def init_w(f_in, f_out, constant=2):
    low = -constant * np.sqrt(6 / (f_in + f_out))
    high = constant * np.sqrt(6 / (f_in + f_out))
    return tf.random_uniform((f_in, f_out), minval=low, maxval=high, dtype=tf.float32)


class AutoEncoder(object):
    def __init__(self, n_input, n_hidden, transfer_function=tf.nn.softplus,
                 optimizer=tf.train.AdadeltaOptimizer(), scale=0.1):
        """
        :param n_input:输入变量数
        :param n_hidden:隐含层节点数
        :param transfer_function:隐含层激活函数，默认为softplus：log(exp(features)+1)
        :param optimizer:优化器，Adam
        :param scale:高斯噪声系数，0.1
        """
        self.n_hidden = n_hidden
        self.n_input = n_input
        self.transfer = transfer_function
        self.scale = tf.placeholder(tf.float32)
        self.training_scale = scale
        netword_weigths = self._initialize_weights()
        self.weights=netword_weigths
        # model：定义网络结构
        self.x = tf.placeholder(tf.float32,[None,self.n_input])
        #sigmoid((x+噪音)*w1+b1) softplus((x+噪音)*w1+b1)
        self.hidden = self.transfer(tf.add(tf.matul(self.x+scale*tf.random_uniform((n_input,)),
                                                    self.weights['w1']),self.weights['b1']))
        #输出=隐含层[]*w2+b2=x(reconstruction)
        self.reconstruction = self.transfer(tf.add(tf.matmul(self.hidden,self.weights['w2']),
                                                   self.weights['b2']))
        #cost：定义损失函数：1/2sum((输出-x)^2)
        self.cost = 0.5*tf.reduce_sum(tf.pow(tf.subtract(self.reconstruction,self.x),2.0))
        self.optimizer = optimizer.minimize(self.cost)

        init=tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

    def _initialize_weights(self):
        all_weight = dict()
        #初始化权重在合适范围内
        # [初始化大小：在每层建传递更新较小，权重更新少，初始化权重太大，容易发散]

