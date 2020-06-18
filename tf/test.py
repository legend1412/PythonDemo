# -*- conding:UTF-8 -*-
import tensorflow as tf
import tensorflow.contrib.eager as tfe

tfe.enable_eager_execution()

initial = tf.truncated_normal((2, 2), stddev=0.1)

with tf.Session() as sess:
    # sess.run(tf.global_variables_initializer())
    print(sess.run(initial))

a = tf.constant([1,2,1,2,3,0])
a = tf.reshape(a,[2,3])
b = tf.constant([2])
c = tf.reduce_max(a,axis=0,keep_dims=True)

init = tf.global_variables_initializer()

with tf.Session() as sess:
