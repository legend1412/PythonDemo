import os
import math
import operator
import random
import re
from collections import Counter
from kmeans.k_means import load_data

print(os.getcwd())
print(math.cos(20))
print(operator.abs(1))

file_path = '../data/allfiles'

K = 3
doc_dict, doc_list = load_data()
doc1_dict = doc_dict['734business']
doc2_dict = doc_dict['1643auto']
words = set(doc1_dict).union(set(doc2_dict))
print(len(words))
print(words)
k_doc_list = random.sample(doc_list, K)
print(doc_list)
print(k_doc_list)
print(random.random() * 27)

label_pattern = re.compile(r'[a-z]')
print(label_pattern.findall('12business'))
print('------------------------------------------------------------')
a = dict()
for i in range(3):
    a[i] = '%s' % i
print([i for i in a.keys()])
print(Counter([i for i in a.keys()]))
print(abs(-1))

print('------------------------------------------------------------')
word_dict = dict()
word_freq = dict()
line = "business yule business it sports auto"
words = line.strip().split(' ')
for word in words:
    if word_dict.get(word, -1) == -1:
        word_dict[word] = len(word_dict)
    wid = word_dict.get(word, -1)
    if word_freq.get(wid, -1) == -1:
        word_freq[wid] = 1
    else:
        word_freq[wid] += 1

print(word_freq)
