# -*- coding: UTF-8 -*-
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('../data/MNIST/', one_hot=True)

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.6)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))


# sess = tf.Session()


# 权重初始化
def weight_variable(shape):
    initial = tf.random.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# 1 步长（stride，size），0 边距（padding，size）的模板，保证输出和输入时同i个大小
# padding：是否对输入的图像矩阵边缘补0，'SAME'（是）和 'VALID'（否）
def conv2d(x1, w):
    return tf.nn.conv2d(x1, w, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x1):
    return tf.nn.max_pool2d(x1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# 卷积核大小5*5 -> 32 feature map,1表示channel，黑白
w_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# 取到的是one_hot形式的图片，即在一个数组中
x = tf.compat.v1.placeholder(tf.float32, shape=[None, 784])
# reshape将数组转化成28*28矩阵大小，即图片
x_image = tf.reshape(x, [-1, 28, 28, 1])

# ###############model#################################

# 第一层，以relu为激励函数（与softplus,sigmoid一样的功能），前向传播进行（加权+偏置bias），卷积，池化
h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)  # 32个28*28 feature maps
# 12*12
h_pool1 = max_pool_2x2(h_conv1)  # 32个14*14 feature maps

# 第二层：这里为什么是channel=32?
# 因为上一层生成了32个feature map,channel=1(原始图片channel)*32（feature map数量）
w_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)  # 64@14*14
h_pool2 = max_pool_2x2(h_conv2)  # 64@7*7

# 第三层7*7图片大小，因为需要做全连接层，需要将图片（矩阵）变成向量shape
# 还有没有别的方式进行这一层得到全连接层？
w_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

# dropout
# 1、按照一定概率丢失节点，可以减少过拟合
# 2、自动处理输出值的scale
keep_prob = tf.compat.v1.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob=keep_prob)

# 输出层
w_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
# 训练设置
y_ = tf.compat.v1.placeholder(tf.float32, shape=[None, 10])
cross_entropy = -tf.reduce_sum(y_ * tf.math.log(y_conv))

train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# 预测设置 index[0,1,2,3,4,5,6,7,8,9] [0.1,0.01,0.03,0.05,0.5,0.2,0.01,...]  [0,0,0,0,1,0,0,0,0,...]\
correct_pred = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))  # [0,0,1,1,1]
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# sess.run(tf.initialize_all_variables())
sess.run(tf.compat.v1.global_variables_initializer())

# 开始训练打印日志
total = 2000
good = 0
for i in range(total):
    batch = mnist.train.next_batch(50)
    # total += batch[0].shape[0]
    # 预测过程需要所有节点都起到作用，所以keep_prob:1.0
    train_accuracy = accuracy.eval(session=sess, feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
    good += train_accuracy
    if i % 100 == 0:
        print('step:%d,training accuracy %g' % (i, train_accuracy))
    # 训练过程需要将部分节点dropout，所以要给定一个概率0.5 early_stop
    train_step.run(session=sess, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    # print('Test accuracy %g' % accuracy.eval(session=sess,
    #                                          feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
print('Good: %g,Test accuracy:%g' % (good, (good / total)))
