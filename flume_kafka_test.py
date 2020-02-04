# -*- coding:utf-8 -*-
import random
import time

readFileName = "/usr/usrdata/orders.csv"
writeFileName = "./flume_kafka_test.txt"
with open(writeFileName, 'a+') as wf:
    with open(readFileName, 'rb') as f:
        for line in f.readline():
            for word in line.split(" "):
                ss = line.strip()
                if len(ss) < 1:
                    continue
                wf.write(ss + "\n")
            # rand_num = random.random()
            # time.sleep(rand_num)
