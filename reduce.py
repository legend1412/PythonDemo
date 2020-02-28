data_path = './data/reduce_test.txt'
cur_word = None
_sum = 0
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        word, val = line.strip().split(',')
        if cur_word is None:
            cur_word = word
        if cur_word != word:
            print('%s,%s' % (cur_word, _sum))
            cur_word = word
            _sum = 0
        _sum += int(val)
    print('%s,%s' % (cur_word, _sum))
