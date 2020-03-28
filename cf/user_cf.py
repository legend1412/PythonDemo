from cf.util import read_train_data

# 1.获取用户和用户之间的相似度
# 1.1 正常逻辑，用户相似度计算


train_data = read_train_data()
# 相似度字典
w = dict()
for u in train_data.keys():
    if w.get(u, -1) == -1:
        w[u] = dict()
        for v in train_data.keys():
            if u == v: continue
            # 相似度计算，通过两个用户共同拥有的物品集合数量
            w[u][v] = len(set(train_data[u]) & set(train_data[v]))  # jaccard distance
            w[u][v] = 2 * w[u][v] / (len(train_data[u]) + len(train_data[v]))

# print(w['196'])
# 发现相似度为0的数据 '826':0.0 复杂度:O(n^2)
print('all user cnt:', len(w.keys()))
print('user_196 sim user cnt', len(w['196']))
