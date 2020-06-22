# -*- coding:UTF-8 -*-
import tensorflow as tf
# import tensorflow.contrib.eager as tfe
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from pprint import pprint

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

# tfe.enable_eager_execution()
#
# initial = tf.truncated_normal((2, 2), stddev=0.1)
#
# with tf.Session() as sess:
#     # sess.run(tf.global_variables_initializer())
#     print(sess.run(initial))
#
# a = tf.constant([1, 2, 1, 2, 3, 0])
# a = tf.reshape(a, [2, 3])
# d = tf.constant([2])
# c = tf.reduce_max(a, axis=0, keep_dims=True)
#
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#     print(a.eval())
#     print(sess.run(c))
#
# mnist = input_data.read_data_sets('../data/MNIST/', one_hot=True)
# a = mnist.train.images
# sample = np.array(a[0])
# print(sample.reshape([28, 28]))
# pprint(a[0])
#
# # data以后做好数据处理的数据，从文件中读入数据
# x = tf.placeholder(tf.float32, [None, 1])
# y_true = tf.placeholder(tf.float32, [None, 1])
#
# # 定义模型参数变量
# w = tf.Variable(tf.zeros([1, 1]))
# b = tf.Variable(tf.zeros([1]))
#
# # 表示输出的计算方式
# y_pred = tf.matmul(x, w) + b
# # 目标函数:cost,loss,我们在寻找使的这个loss最小的w，b
# loss = tf.reduce_mean(tf.square(y_pred - y_true))
# # 通过梯度方式寻找使得loss最小的w，b
# optimizer = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
#
# init = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init)
#     for step in range(200):
#         sess.run(optimizer, feed_dict={x: step[0], y_true: step[1]})
#         if step % 20 == 0:
#             print(sess.run([w, b], feed_dict={x: step[0], y_true: step[1]}))
#
# # tf.argmax(a, axis=1)=> [1,0,1]  tf.argmax(a, axis=0)=>[1,2]
# axis=0；所有行扫一遍，取每一列最大的，axis=1：每一行最大的
a = [
    [1, 2],  # 1
    [2, 1],  # 0
    [1, 3],  # 1
]
with tf.Session() as sess:
    print(sess.run(tf.argmax(a, 0)))
