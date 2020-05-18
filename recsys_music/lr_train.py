import recsys_music.gen_cf_data as gcd
import recsys_music.config as conf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 特征映射表，交叉特诊，模型，输出
cross_file = conf.cross_file
user_feat_map_file = conf.user_feat_map_file
model_file = conf.model_file

# label标记，打印正负样本比例
# def analysis_avg_score():
#     df_user_watch = conf.user_watch()
#     df_music_watch = conf.music_data()
#     data = df_user_watch.merge(df_music_watch, how='inner', on='item_id')
#     del df_user_watch
#     del df_music_watch
#     data['score'] = data.apply(lambda x: float(x['stay_seconds']) / float(x['total_timelen']), axis=1)
#     data = data.groupby(['user_id', 'item_id'])['score'].mean().reset_index()
#     data['more_than_one'] = data['score'].apply(lambda x: 1 if x > 0.9 else 0)
#     ana = data.groupby('more_than_one')['score'].count()
#     print(ana)
#
#
# analysis_avg_score()

initdata = gcd.user_item_score(10000000, tag='avg')
# 定义label 0/1规则，希望给用户推荐的音乐，是用户能完整听完的
# 具体分析可以参考analysis_avg_score这个方法
initdata['label'] = initdata['score'].apply(lambda x: 1 if x >= 0.9 else 0)

"""
user_id,item_id,label
加入用户和item信息
"""

# user信息
user_profile = conf.user_profile()
# item信息
music_meta = conf.music_data()

# 关联用户和item的信息到initdata中
initdata = initdata.merge(user_profile, how='inner', on='user_id').merge(music_meta, how='inner', on='item_id')
# 基于字段归属，特征分类
user_feat = ['gender', 'age', 'salary', 'province']
item_feat = ['totla_timelen', 'location']
item_text_feat = ['item_name', 'tags']
watch_feat = ['hours', 'stay_seconds', 'score']

# 基于字段类型，特征分类
category_feat = user_feat + ['location']
continuous_feat = ['score']

labels = initdata['label']
del initdata['label']

# 特征处理
# 1.离散特征ont-hot处理（word2vec->embeddiing[continuous])
df = pd.get_dummies(initdata[category_feat])  # 特征_特征值
ont_hot_columns = df.columns  # ['gender_男'，'gender_女']
# print(df.head())
# 2.连续特征不处理直接带入[一般做离散GBDT（xgboot）叶子结点做离散化编码 GBDT+LR]
df[continuous_feat] = initdata[continuous_feat].astype(float)  # 转换数据类型 cast（as float）

# cross feat save（交叉特征）
# 交叉特征线要对user_id和item_id 做一个组合key
initdata['ui-key'] = initdata['user_id'].astype(str) + "_" + initdata['item_id'].astype(str)
cross_feat_map = dict()  # 存储到线上，这样线上也能获取到对应的特诊（用户的历史行为统计类型的特征，交叉，item历史特征）
for _, row in initdata[['ui-key', 'score']].iterrows():
    cross_feat_map[row['ui-key']] = row['score']
# 存储交叉特征{userid_itemid:score}
with open(cross_file, 'w', encoding='utf-8') as f:
    f.write(str(cross_feat_map))

# print('样本中的X，特征')  # 10条数据
# print(df.values[:10])

# 随机划分训练集train test split[0.7,0.3]
X_train, X_test, Y_train, Y_test = train_test_split(df.values, labels, test_size=0.3, random_state=2019)
lr = LogisticRegression(penalty='l2', dual=False, tol=1e-4, C=1.0, fit_intercept=True, intercept_scaling=1,
                        class_weight=None, random_state=None, solver='liblinear', max_iter=100,
                        multi_class='ovr', verbose=1, warm_start=False, n_jobs=-1)

model = lr.fit_tranform(X_train, Y_train)
print('w:%s,b:%s' % (lr.coef_, lr.intercept_))
print('score:%.4f' % lr.score(X_test, Y_test))

# 存储特征map[key(字段名+'_'+字段值):index]
feat_map = {}
for i in range(len(ont_hot_columns)):
    key = ont_hot_columns[i]
    feat_map[key] = i
print(feat_map)

# 特征映射表存储
with open(user_feat_map_file, 'w', encoding='utf-8') as ohf:
    ohf.write(str(feat_map))
# model save
model_dict = {'W': lr.coef_.tolist()[0], 'b': lr.intercept_.tolist()[0]}
with open(model_file, 'w', encoding='utf-8') as mf:
    mf.write(str(model_dict))
