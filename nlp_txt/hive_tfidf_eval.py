data_path = "../data/mid_data/data.train"

tf = dict()
with open(data_path, 'r', encoding='utf-8') as f:
    line = f.readline().strip()
    wd = line.split('#')
    wids, doc_name = wd[0], wd[1]
    wid_lst = wids.split(' ')
    for wid in wid_lst:
        if tf.get(wid, -1) == -1:
            tf[wid] = 0
        tf[wid] += 1
print(sorted(tf.items(), key=lambda x: x[1], reverse=True)[:20])
