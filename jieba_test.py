# import jieba
#
# a = '我今天要上Map Reduce，我今天上午已经上了课。'
# # cut_list = jieba.cut(a, cut_all=False)
# # print(','.join(cut_list))
# cut_list = [x for x in jieba.cut(a, cut_all=False)]
# print(cut_list)
# print([hash(x) % 3 for x in cut_list])
#
# a1 = '我'
# a2 = '今天'
# a3 = '要'
# a4 = '我'
# print(a1, hash(a1), hash(a1) % 3)
# print(a2, hash(a2), hash(a2) % 3)
# print(a3, hash(a3), hash(a3) % 3)
# print(a4, hash(a4), hash(a4) % 3)

import sys
import re

p = re.compile(r'\w+')
for line in sys.stdin:
    ss = line.strip().split(' ')
    for s in ss:
        if len(p.findall(s)) < 1:
            continue
        s_low = p.findall(s)[0].lower()
        print(s_low + ',' + '1')
