data_path = '../data/allfiles.txt'

# 一、初始化模型参数（π初始状态，a转移矩阵，b发射矩阵）
# 其中状态为：B，M，E，S，每个中文字都会对应其中的一个状态
STATUS_NUM = 4
# 1、初始状态概率π
pi = [0.0 for pi in range(STATUS_NUM)]  # count
pi_sum = 0.0
# print(pi)

# 2、状态转移概率 a：M*M 矩阵
# [0.0, 0.0, 0.0, 0.0] 分母1
# [0.0, 0.0, 0.0, 0.0] 分母2
# [0.0, 0.0, 0.0, 0.0] 分母3
# [0.0, 0.0, 0.0, 0.0] 分母4
A = [[0.0 for col in range(STATUS_NUM)] for row in range(STATUS_NUM)]  # count
# print(A)
# for i in range(STATUS_NUM):
#     print(A[i])

A_sum = [0.0 for row in range(STATUS_NUM)]  # 存储每一行数据的分母，用作求概率

# 3、发射概率 b:M*N 矩阵 本身矩阵相对比较稀疏，因为是4个状态到对应每个中文字的概率
# N是中文字典大小，每个字不一定都会有4个状态，或者有些字在对应状态中没有出现过，导致数据稀疏
# 所以这个不需要矩阵，用字典稀疏存储减少空间浪费
B = [dict() for row in range(STATUS_NUM)]
B_sum = [0.0 for row in range(STATUS_NUM)]

f_txt = open(data_path, 'r', encoding='utf-8')

while True:
    line = f_txt.readline()  # 读一行相当于一篇文章
    print(line)

    break
