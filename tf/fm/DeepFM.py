"""
Tensorflow implementation of DeepFM [1]
Reference:
[1] DeepFM: A Factorization-Machine based Neural Network for CTR Prediction,
    Huifeng Guo,Ruiming Tang,Yunming Yey,Zhenguo Li,Xiuqiang He.
"""
import numpy as np
import tensorflow as tf
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import roc_auc_score
from time import time
from tensorflow.contrib.layers.python.layers import batch_norm as batch_norm


# from yellowfin import YROptimizer

class DeepFM(BaseEstimator, TransformerMixin):
    def __init__(self, feature_size, field_size, embedding_size=8, dropout_fm=[1.0, 1.0],
                 deep_layers=[32, 32], dropout_deep=[0.5, 0.5, 0.5], deep_layers_activation=tf.nn.relu,
                 epoch=10, batch_size=256, learing_rate=0.001, optimizer_type='adam', batach_norm=0,
                 batch_norm_decay=0.995, verbose=False, random_seed=2016, use_fm=True, usr_deep=True,
                 loss_type='logloss', eval_metric=roc_auc_score, l2_reg=0.0, greater_is_better=True):
        assert (use_fm or usr_deep)
        assert loss_type in ['logloss', 'mse'], "loss_type can be either 'logloss' for calssification task or 'mse' for regression task"

        self.feature_fm = feature_size  # denote as M,size of the feature dictionary
        self.field_size = field_size  # denote as F,size of the feature fields
        self.embedding_size = embedding_size

        self.dropout_fm = dropout_fm
        self.deep_layers = deep_layers
        self.dropout_deep = dropout_deep
        self.deep_layers_activation = deep_layers_activation
        self.use_fm = use_fm
        self.use_deep = usr_deep
        self.l2_reg = l2_reg

        self.epoch = epoch
        self.batch_size = batch_size
        self.learning_rate = learing_rate
        self.optimizer_type = optimizer_type

        self.batch_norm = batach_norm
        self.batch_norm_decay = batch_norm_decay

        self.verbose = verbose
        self.random_seed = random_seed
        self.loss_type = loss_type
        self.eval_metric = eval_metric
        self.greater_is_better = greater_is_better
        self.train_result, self.valid_result = [], []

        self._init_graph()

    def _init_graph(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.set_random_seed(self.random_seed)
            self.feat_index = tf.placeholder(tf.int32, shape=[None, None], name='feat_index')  # None*F
            self.feat_value = tf.placeholder(tf.float32, shape=[None, None], name='feat_value')  # None*F
            self.label = tf.placeholder(tf.float32, shape=[None, 1], name='label')
            self.dropout_keep_fm = tf.placeholder(tf.float32, shape=[None], name='dropout_keep_fm')
            self.dropout_keep_deep = tf.placeholder(tf.float32, shape=[None], name='dropout_keep_deep')
            self.train_phase = tf.placeholder(tf.bool, name='train_phase')
            self.weights = self._initialize_weights()

            # model
            # 将weights中对应feat特征向量部位0的index的weight值取出
            self.embedding = tf.nn.embedding_lookup(self.weights['feature_embeddings'], self.feat_index)  # None*F*K
            # 将feat_value行向量转变成列向量，如果传进来就是列向量就不用变
            feat_value = tf.reshape(self.feat_value, shape=[-1, self.field_size, 1])
            # wx 只是点乘中的一步乘，未求和
            self.embedding = tf.multiply(self.embedding, feat_value)

            # -----------------first order term------------------------------------
            # 取出bias
            self.y_first_order = tf.nn.embedding_lookup(self.weights['feature_bias'], self.feat_index)  # None*F*1
            # bias*feat_value lr中的wx
            self.y_first_order = tf.reduce_sum(tf.multiply(self.y_first_order, feat_value), 2)  # None*F
            # 对输出进行dropout
            self.y_first_order = tf.nn.dropout(self.y_first_order, self.dropout_keep_fm[0])  # None*F

            # ------------second order term------------------------------
            # <vi,vj>xixj
            # sum_square part 先求和后平方
            # 对列求和(不同的field值求和，x值求和)参考embedding做召回的u向量和i向量求和的形式
            self.summed_features_emb = tf.reduce_sum(self.embedding, 1)  # None*K
            self.summed_features_emb_square = tf.square(self.summed_features_emb)  # None*K

            # square_sum part 先求和后平方
            self.squared_features_emb = tf.square(self.embedding)
            self.squared_sum_features_emb = tf.reduce_sum(self.squared_features_emb, 1)  # None*K
            # second order 1/2 (求和平方-平方求和)
            self.y_second_order = 0.5 * tf.subtract(self.summed_features_emb_square, self.squared_sum_features_emb)  # None*K
            # 输出+dropout
            self.y_second_order = tf.nn.dropout(self.y_second_order, self.dropout_keep_fm[1])  # None*K
            # ------------------Deep component--------------深度部分
            self.y_deep = tf.reshape(self.embedding, shape=[-1, self.field_size * self.embedding_size])  # None*(F*K)
            # 这一层对于传入dnn中进行dropout，在fm里面没有dropout
            self.y_deep = tf.nn.dropout(self.y_deep, self.dropout_keep_deep[0])

            for i in range(0, len(self.deep_layers)):
                # wx+b加权求和
                self.y_deep = tf.add(tf.matmul(self.y_deep, self.weights['layer_%d' % i]), self.weights['bias_%d' % i])  # None*layer[i]*1
                # 在加权求和后，激励函数前增加batch norm
                if self.batch_norm:
                    self.y_deep = self.batch_norm_layer(self.y_deep, train_phase=self.train_phase, scope_bn='bn_%d' % i)  # None*layer[i]*1

                # 输入定义的relu激励函数
                self.y_deep = self.deep_layers_activation(self.y_deep)
                self.y_deep = tf.nn.dropout(self.y_deep, self.dropout_keep_deep[1 + i])  # dropout at each Deep layer
