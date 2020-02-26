# -*- coding: utf-8 -*-
import random
import time
import pandas as pd
import json
#import os

#data_path = 'D:\data\data'
#data_file = os.path.join(data_path,'orders.csv')

writeFileName = "./flume_test.txt"
# writeFileName="./flume_hive_text.txt"
cols=["order_id","user_id","eval_set","order_number","order_dow","hour","day"]

df = pd.read_csv('../../usrdata/orders.csv')

#print(df.head())
#print(df.columns)

df.columns = cols
df1 = df.fillna(0)

with open(writeFileName,'a+') as wf:
	for idx,row in df1.iterrows():
		d={}
		for col in cols:
			d[col]=row[col]
		js=json.dumps(d)
		wf.write(js+'\n')
