"""
Tensorflow implementation of DeepFM [1]
Reference:
[1] DeepFM: A Factorization-Machine based Neural Network for CTR Prediction,
    Huifeng Guo,Ruiming Tang,Yunming Yey,Zhenguo Li,Xiuqiang He.
"""
import numpy as np
import tensorflow as tf
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.metrics import roc_auc_score
from time import time
from tensorflow.contrib.layers.python.layers import batch_norm as batch_norm

# from yellowfin import YROptimizer

class DeepFM(BaseEstimator,TransformerMixin):
    def __init__(self,feature_size,field_size,embedding_size=8,dropout_fm=[1.0,1.0],
                 deep_layers=[32,32],dropout_deep=[0.5,0.5,0.5],deep_layers_activation=tf.nn.relu,
                 epoch=10,batch_size=256,learing_rate=0.001,optimizer_type='adam',batach_norm=0,
                 batch_norm_decay=0.995,verbose=False,random_seed=2016,use_fm=True,usr_deep=True,
                 loss_type='logloss',eval_metric=roc_auc_score,l2_reg=0.0,greater_is_better=True):
        assert (use_fm or usr_deep)
        assert loss_type in ['logloss','mse'],"loss_type can be either 'logloss' for calssification task or 'mse' for regression task"

        self.feature_fm = feature_size # denote as M,size of the feature dictionary
        self.field_size = field_size # denote as F,size of the feature fields


        self.dropout_fm = dropout_fm

