# -*- coding:UTF-8 -*-

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow_core.examples.tutorials.mnist import input_data
from PIL import Image

tf.compat.v1.reset_default_graph()

# # 读入数据
mnist = input_data.read_data_sets('../data/MNIST/', one_hot=True)
print(mnist.train.images.shape, mnist.train.labels.shape)  # (55000,784)(55000,10)
print(mnist.test.images.shape, mnist.test.labels.shape)  # (10000,784)(1000,10)
print(mnist.validation.images.shape, mnist.validation.labels.shape)  # (5000,784)(5000,10)


def img_show(img):
    img1 = Image.fromarray(img * 255)  # Image和Ndrray互相转换
    img2 = img1.convert('RGB')  # jpg可以是RGB模式，也可以是CMYK模式
    plt.imshow(img2, cmap="gray")
    plt.show()


im = mnist.train.images[2].reshape((28, 28))  # 读取的格式为Ndarry
print(mnist.train.labels[2])
img_show(im)
