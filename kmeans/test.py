
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
