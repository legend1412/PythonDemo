from cf.util import read_train_data


def item_sim(train_data):
    # 相似物品矩阵
    c = dict()  # {item:{item1:sim_score,item2:sim_score}}
    n = dict()  # {item:用户数}

    # 扫一遍数据集，统计相似物品矩阵的分子部分C和统计item拥有的user dict N
    for u, items in train_data.items():
        for i in items:
            # item有多少用户
            if n.get(i, -1) == -1:
                # N[i] = set()
                n[i] = 0
            # N[i].add(u)
            n[i] += 1
            if c.get(i, -1) == -1:
                c[i] = dict()
            for j in items:
                if i == j:
                    continue
                elif c[i].get(j, -1) == -1:
                    c[i][j] = 0
                c[i][j] += 1
    # 扫一遍相似物品矩阵C，将分母除进去
    for i, sim_items in c.items():
        for j, cij in sim_items.items():
            # C[i][j] = cij/len(N[i]|N[j])
            c[i][j] = 2 * cij / (n[i] + n[j] * 1.0)
    return c


def recomendation(train_data, user_id, C, k):
    # 存放最终结果
    rank = dict()
    sum_ = dict()
    ru = train_data[user_id]
    # for i, rating_old, time in ru.items():
        # rating = rating_old * fun(time)
    for i, rating in ru.items():
        for j, sim_score in sorted(C[i].items(), key=lambda x: x[1], reverse=True)[:k]:
            # 过滤这个user已经打过分的item
            if j in ru:
                continue
            elif rank.get(j, -1) == -1:
                rank[j] = 0
            # Ru中item1相似的集合和item2相似的集合中有相同的item，是分值相加的形式
            rank[j] += sim_score * rating

            # sum|cij| 对应PPT sum(|wij|) 只有在相同的itemj，不同的itemi进行ppt中多值相加
            if sum_.get(j, -1) == -1:
                sum_[j] = 0
            sum_[j] += sim_score
    for j in rank.keys():
        rank[j] /= sum_[j]
    return rank


# 时间衰减函数
def fun(time):
    print(time)


if __name__ == '__main__':
    # {user_id:{item_id:rating}}
    train_data1 = read_train_data()

    C = item_sim(train_data1)
    # print(sorted(C['196'].items(), key=lambda x: x[1], reverse=True)[:10])
    rank_r = recomendation(train_data1, user_id='196', c=C, k=10)
    print(sorted(rank_r.items(), key=lambda x: x[1], reverse=True))
