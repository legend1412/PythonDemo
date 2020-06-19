# -*- conding:UTF-8 -*-
import os
import tensorflow as tf
from collections import Counter
import numpy as np
import time

# -----------------------单词数据进行编码转码的方法----------------------------
# 读取数据，返回word list
def read_word(filename):
    with tf.gfile.GFile(filename,'r') as f:
        return f.read().replace('\n','<eos>'.split())

# 建立词典对，单词进行数字编码，对应数字可以理解单词在词典中的位置
def build_vocab(filename):
    data = read_word(filename)

