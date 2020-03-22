# a = '\t a b c\n'
# print(a.strip())
# print(a)
# print(a.strip())

# data_path = './data/test.txt'
#
# with open(data_path, 'r',encoding='utf-8') as f:
#     # print(f.read())
#     # for i in range(2):
#     #     print(f.readline())
#     # print(f.readlines())
#     for line in f.readlines():
#         word_list = line.strip().split(' ')
#         print(word_list)

import re

word = 'granther?"1.'
# p = re.compile(r'\w+')
p = re.compile(r'[a-zA-Z0-9]')
# print(re.match('^[a-zA-Z0-9]+$',word))
# print(p.match(word))
word = p.findall(word)
print(word)
st = "hello,world!!%[545]你好234世界。。。"
result = ''.join(re.findall(r'[A-Za-z]', st))
print(result)
p = re.compile(r'[A-Za-z]')
print(p.findall(st))

pattern = re.compile(r'\d+')  # 查找数字
result1 = pattern.findall('runoob 123 google 456')
result2 = pattern.findall('run88oob123google456', 0, 10)

print(''.join(result1))
print(result2)

origin = "12 13 14"
res = re.match(r"(\d\d) (\d\d) (\d\d)", origin)
# input("dss")

print("=========================")
for i in range(10):
    if i==-1:
        print("进入")
        for j in range(5):
            print("j:"+str(j))
    print("i:"+str(i))
print("=========================")

def add(element: int) -> int:
    print(element)
    return 0


add(1)

