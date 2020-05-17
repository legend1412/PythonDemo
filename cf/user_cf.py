from cf.util import read_train_data


# 1.获取用户和用户之间的相似度
# 1.1 正常逻辑，用户相似度计算 jaccard distance =交集/并集
# 复杂度 n^2*l^2 l<m
def user_normal_simmilarity(train_data):
    # 相似度字典
    w = dict()

    for u in train_data.keys():
        if w.get(u, -1) == -1:
            w[u] = dict()
            for v in train_data.keys():
                if u == v: continue
                # 相似度计算，通过两个用户共同拥有的物品集合数量
                w[u][v] = len(set(train_data[u]) & set(train_data[v]))  # l<m l^2 # jaccard distance
                w[u][v] = w[u][v] / (len(set(train_data[u]) | set(train_data[v])))
    return w
    # print(w['196'])
    # 发现相似度为0的数据 '826':0.0 复杂度:O(n^2)
    # print('all user cnt:', len(w.keys()))
    # print('user_196 sim user cnt', len(w['196']))
    # print(sorted(w['196'].items(), key=lambda x: x[1], reverse=False)[:10])


# 1.2 优化计算用户与用户之间的相似度 user->item => item->user
# 复杂度 n*m+m*k^2 m>nl
def user_sim(train_data):
    # 建立item->user的倒排表 n*m
    item_users = dict()
    for u, items in train_data.items():  # n # items item,rating
        for i in items.keys():  # m
            if item_users.get(i, -1) == -1:
                item_users[i] = set()
            item_users[i].add(u)

    # 计算共同的items数量
    c = dict()

    # 复杂度 m*k^2
    for i, users in item_users.items():  # m
        for u in users:  # k<n
            if c.get(u, -1) == -1:
                c[u] = dict()
            for v in users:  # k<n
                if u == v:
                    continue
                if c[u].get(v, -1) == -1:
                    c[u][v] = 0
                c[u][v] += 1

    del item_users  # 从内存中删除
    for u, sim_users in c.items():
        for v, cuv in sim_users.items():
            c[u][v] = 2 * c[u][v] / (float(len(train_data[u]) + len(train_data[v])))
    return c
    # print(C['196'])
    # 发现相似度为0的数据 '826':0.0 复杂度:O(n^2)
    # print('all user cnt:', len(C.keys()))
    # print('user_196 sim user cnt', len(C['196']))
    # print(sorted(C['196'].items(), key=lambda x: x[1], reverse=False)[:10])


def recommend(user, train_data, c, k=5):
    rank = dict()
    # 用户之前评论过的电影
    watched_items = train_data[user].keys()
    # 取相似的k个用户的items
    for v, cuv in sorted(c[user].items(), key=lambda x: x[1], reverse=True)[:k]:
        # 相似k个用户的items ②rating
        for i, rating in train_data[v].items():
            # 过滤已经评论过的电影或购买过的商品
            if i in watched_items:
                continue
            elif rank.get(i, -1) == -1:
                rank[i] = 0
            # 物品的打分是①用户相似度[0-1]*②用户相似用户对电影的打分[0-5]
            # 相似用户评论了同一个物品是累加操作
            rank[i] += cuv * rating
    return  rank
    # return sorted(rank.items(), key=lambda x: x[1], reverse=True)[:10]


if __name__ == '__main__':
    train_data1 = read_train_data()
    # w = user_normal_simmilarity(train_data1)
    c1 = user_sim(train_data1)
    uid = '13'
    b = recommend(uid, train_data1, c1)
    print(b)
