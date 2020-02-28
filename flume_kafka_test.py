# -*- coding:utf-8 -*-

readFileName = "/usr/usrdata/orders.csv"
writeFileName = "./flume_kafka_test.txt"
with open(writeFileName, 'a+') as wf:
    with open(readFileName, 'rb') as f:
        for line in f.readlines():
            for word in str(line).split(" "):
                ss = str(line).strip()
                if len(ss) < 1:
                    continue
                wf.write(ss + "\n")
            # rand_num = random.random()
            # time.sleep(rand_num)
