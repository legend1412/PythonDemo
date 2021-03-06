import tensorflow as tf
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split

idir = 'E://GitHub//PythonDemo//data//'
feature_length = 18
tf.compat.v1.disable_eager_execution()


class FM(object):
    """Factorization Machine with FTRL optimization"""

    def __init__(self, config):
        """config:configuration of hyperparameters type of dict"""
        # number of latentfactors
        self.k = config['k']
        self.lr = config['lr']
        self.batch_size = config['batch_size']
        self.reg_l1 = config['reg_l1']
        self.reg_l2 = config['reg_l2']
        # num of features
        self.p = feature_length

    def add_placholders(self):
        """add_placholders"""
        self.X = tf.compat.v1.sparse_placeholder('float32', [None, self.p])
        self.y = tf.compat.v1.placeholder('int64', [None, ])
        self.keep_prob = tf.compat.v1.placeholder('float32')

    def inference(self):
        """
        forward propagation
        :return: labels for each sample
        """
        with tf.compat.v1.variable_scope('linear_layer'):
            b = tf.compat.v1.get_variable('bias', shape=[2], initializer=tf.zeros_initializer())
            w1 = tf.compat.v1.get_variable('w1', shape=[self.p, 2],
                                           initializer=tf.compat.v1.truncated_normal_initializer(mean=0, stddev=1e-2))

            # shape of [None,2]
            self.linear_terms = tf.add(tf.compat.v1.sparse_tensor_dense_matmul(self.X, w1), b)

        with tf.compat.v1.variable_scope('interaction_layer'):
            v = tf.compat.v1.get_variable('v', shape=[self.p, self.k],
                                          initializer=tf.compat.v1.truncated_normal_initializer(mean=0, stddev=0.01))
            # shape of [None,1]
            self.interaction_terms = tf.multiply(0.5, tf.reduce_mean(
                tf.subtract(tf.pow(tf.compat.v1.sparse_tensor_dense_matmul(self.X, v), 2),
                            tf.compat.v1.sparse_tensor_dense_matmul(self.X, tf.pow(v, 2))),
                1, keepdims=True))

        # shape of [None,2]
        self.y_out = tf.add(self.linear_terms, self.interaction_terms)
        self.y_out_prob = tf.nn.softmax(self.y_out)

    def add_loss(self):
        """addloss"""
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.y, logits=self.y_out)
        mean_loss = tf.reduce_mean(cross_entropy)
        self.loss = mean_loss
        tf.summary.scalar('loss', self.loss)

    def add_accuracy(self):
        """accuracy"""
        self.correct_prediction = tf.equal(tf.cast(tf.argmax(model.y_out, 1), tf.int64), model.y)
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
        # add summary to accuracy
        tf.summary.scalar('accuracy', self.accuracy)

    def train(self):
        """Applies exponential decay to learning rate"""
        self.global_step = tf.Variable(0, trainable=False)
        # define outimizer
        optimizer = tf.compat.v1.train.FtrlOptimizer(self.lr, l1_regularization_strength=self.reg_l1,
                                                     l2_regularization_strength=self.reg_l2)
        extra_update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(extra_update_ops):
            self.train_op = optimizer.minimize(self.loss, global_step=self.global_step)

    def build_graph(self):
        """build graph for model"""
        self.add_placholders()
        self.inference()
        self.add_loss()
        self.add_accuracy()
        self.train()


def check_restore_parameters(sess, saver):
    """Restore the previously parameter is there are any"""
    ckpt = tf.train.get_checkpoint_state('checkpoints')
    if ckpt and ckpt.model_checkpoint_path:
        logging.info('Loading parameters for the my CNN architectures...')
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        logging.info('Initializing fresh parameters for the my Factorization Machine')


# 有放回的采样，以采样一个batch_size大小的数据
def get_random_block_from_data(data, labels, batch_size):
    """
    :param data:
    :param labels:
    :param batch_size:
    :return:
    """
    start_index = np.random.randint(0, data.shape(0) - batch_size)  # bathc_size =2,len(data)=10 [0,9]
    return data.iloc[start_index:(start_index + batch_size), :], labels[start_index:(start_index + batch_size)]


if __name__ == '__main__':
    df_train = pd.read_csv(idir + 'train_feat.csv').fillna(0.)
    init_labels = np.load(idir + 'labels.npy')
    X_train, X_test, y_train, y_test = train_test_split(df_train, init_labels, test_size=0.2, random_state=2019)
    del df_train
    del init_labels
    f_to_use = ['user_total_orders', 'user_total_items', 'total_distinct_items',
                'user_average_days_between_orders', 'user_average_basket',
                'order_hour_of_day', 'days_since_prior_order', 'days_since_ratio',
                'aisle_id', 'department_id', 'product_orders', 'product_reorders',
                'product_reorder_rate', 'UP_orders', 'UP_orders_ratio',
                'UP_average_pos_in_cart', 'UP_orders_since_last',
                'UP_delta_hour_vs_last']

    config = {'lr': 0.01, 'batch_size': 512, 'reg_l1': 2e-2, 'reg_l2': 0, 'k': 40}

    # print(X_train.head())
    # print(X_train[f_to_use])
    num_batches = int(X_train.shape[1] / config['batch_size'])
    print(num_batches)
    # initialize FM model
    model = FM(config)
    # build graph for model
    model.build_graph()

    init_saver = tf.compat.v1.train.Saver(max_to_keep=15)
    with tf.compat.v1.Session() as init_sess:
        init_sess.run(tf.compat.v1.global_variables_initializer())
        # restore trained parameters
        check_restore_parameters(init_sess, init_saver)
        # train
        merged = tf.compat.v1.summary.merge_all()
        train_writer = tf.compat.v1.summary.FileWriter('train_logs', init_sess.graph)
        epochs = 30

        for e in range(epochs):
            num_samples = 0
            losses = []
            for ibatch in range(num_batches):
                batch_x, batch_y = get_random_block_from_data(X_train, y_train, config['batch_size'])
                feed_dict = {model.X: batch_x.to_sparse, model.y: batch_y, model.keep_prob: 0.5}
                batch_loss, acc, summary, global_step, _ = init_sess.run(
                    [model.loss, model.accuracy, merged, model.global_step, model.train_op], feed_dict=feed_dict)

                print(batch_loss)
                # aggregate performance stats
            #     losses.append(loss * config['batch_size'])
            #     num_samples += config['batch_size']
            #     # Record summaries and train.csv-set accuracy
            #     train_writer.add_summary(summary, global_step=global_step)
            #     # print training loss and accuracy
            #     if global_step % 50 == 0:
            #         logging.info(
            #             'Iteraction {0}:with minibathc training loss ={1} and accuracy of {2}'
            #                 .format(global_step, loss, accuracy))
            #         saver.save(sess, 'checkpoints/model', global_step=global_step)
            #         # print loss of one epoch
            #
            # total_less = np.sum(losses) / num_samples
            # print('Epoch {1},Overall loss ={0:.3g}'.format(total_less, e + 1))
