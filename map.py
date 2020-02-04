import sys
import re

p = re.compile(r'\w+')
# data_path = './data/test.txt'
data_path = './data/The_man_of_property.txt'
with open(data_path, 'r', encoding='utf-8') as f:
    # print(f.read())
    # for i in range(2):
    #     print(f.readline())
    # print(f.readlines())
    for line in f.readlines():
        word_list = line.strip().split(' ')
        # print(word_list)
        for word in word_list:
            re_word = p.findall(word)
            if len(re_word) == 0:
                continue
            word = re_word[0].lower()
            print('%s,%s' % (word, 1))
