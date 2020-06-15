# -*- coding:UTF-8 -*-

import tensorflow_core as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow_core.examples.tutorials.mnist import input_data
from PIL import Image

tf.reset_default_graph()

# # 读入数据
mnist = input_data.read_data_sets('../data/MNIST/', one_hot=True)
print(mnist.train.images.shape, mnist.train.labels.shape)  # (55000,784)(55000,10)
print(mnist.test.images.shape, mnist.test.labels.shape)  # (10000,784)(1000,10)
print(mnist.validation.images.shape, mnist.validation.labels.shape)  # (5000,784)(5000,10)
