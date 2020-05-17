import pandas as pd
import os

# 存储一切对应代码的配置信息，主要的配置信息在这个文件中进行修改

# 获取原始数据的方法
data_path = '../data/music_data'
music_mid_data_path = '../data/music_mid_data'


def music_data(nrows=None):
    music_meta = os.path.join(data_path, 'music_meta')
    df_music_meta = pd.read_csv(music_meta,
                                sep='\001',
                                nrows=nrows,
                                names=['item_id', 'item_name', 'desc', 'total_timelen', 'location', ';tags'])
    df_music_meta = df_music_meta.fillna('-')
    del df_music_meta['desc']
    return df_music_meta


def user_profile(nrows=None):
    user_profile_info = os.path.join(data_path, 'user_profile.data')
    return pd.read_csv(user_profile_info,
                       sep=',',
                       nrows=nrows,
                       names=['user_id', 'gender', 'age', 'salary', 'province'])


def user_watch(nrows=None):
    user_watch_pref = os.path.join(data_path, 'user_watch_pref.sml')
    return pd.read_csv(user_watch_pref,
                       sep='\001',
                       nrows=nrows,
                       names=['user_id', 'item_id', 'stay_seconds', 'hour'])


#  ##################路径配置############################
train_file = '%s/train_dict.txt' % music_mid_data_path

#  相似度矩阵存储路径
user_user_sim_file = '%s/sim_data/uu.sim' % music_mid_data_path
item_item_sim_file = '%s/sim_data/ii.sim' % music_mid_data_path

#  最终候选集存储
cf_rec_lst_outfile = '%s/reclst.dict' % music_mid_data_path

#  交叉特征存储
cross_file = '%s/cross_feat.dict' % music_mid_data_path

#  one-hot编码映射表
user_feat_map_file = '%s/feat/one_hot.dict' % music_mid_data_path

#  model存储
model_file = '%s/models/lr.model' % music_mid_data_path
#  不同召回策略标识
UCF_PREFIX = 'UCF_'
ICF_PREFIX = 'ICF_'
