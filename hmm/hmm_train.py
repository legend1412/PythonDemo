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


#  将词转换成单个字的列表:'动态规划'=>['动','态','规','划']
def get_word_ch(word):
    ch_lst = []
    for ch in word:
        ch_lst.append(ch)
    return ch_lst


f_txt = open(data_path, 'r', encoding='utf-8')

while True:
    line = f_txt.readline()  # 读一行相当于一篇文章
    # print(line)
    # 读完所有文章退出循环
    if not line:
        break

    words = line.strip().split()
    # print(words)

    ch_lst = []  # 每个词所对应的中文单个字的数组 '动态规划'=>'动','态','规','划'
    status_lst = []  # 对应单个中文字的状态 [B,M,E,S]=>[0,1,2,3]
    for word in words[:-1]:
        # print(word)
        cur_ch_lst = get_word_ch(word)
        cur_ch_num = len(cur_ch_lst)  # 这个词有多少个字

        # for循环可以都初始化成1，那面下面的赋值M那段就可以去掉
        # 初始化字符状态
        cur_status_lst = [0 for ch in range(cur_ch_num)]
        # S:3
        if cur_ch_num == 1:
            cur_status_lst[0] = 3
        else:  # 否则就是BME
            # 标识B:0
            cur_status_lst[0] = 0
            # 标识E:2
            cur_status_lst[-1] = 2
            # 标识M：1，中间的全部为M
            for i in range(1, cur_ch_num - 1):
                cur_status_lst[i] = 1
        ch_lst.extend(cur_ch_lst)
        status_lst.extend(cur_status_lst)
    # ch_lst,status_lst 每篇文章的字和状态
    # print(ch_lst)
    # print(status_lst)

    # 做模型统计：count：分子部分，sum：分母部分
    for i in range(len(ch_lst)):  # 遍历文字序列，对状态序列进行统计
        cur_status = status_lst[i]  # 获取当前文字的状态
        cur_ch = ch_lst[i]  # 获取当前文字
        # 统计初始概率π
        if i == 0:
            # 为什么不用BMES，而用0123，就是方便状态可以直接作为索引形式
            pi[cur_status] += 1.0  # 这里是状态分子部分想加
            pi_sum += 1.0  # 分母求和 不管哪个状态，分母都加1，为了求概率
        # 统计发射概率B
        if B[cur_status].get(cur_ch, -1) == -1:
            B[cur_status][cur_ch] = 0.0
        B[cur_status][cur_ch] += 1.0
        B_sum[cur_status] += 1.0
        # 状态转移概率A
        if i + 1 < len(ch_lst):
            A[cur_status][status_lst[i + 1]] += 1.0
            A_sum[cur_status] += 1.0

    # break
f_txt.close()

# print("π")
# print(pi)
# print(pi_sum)
# print("A")
# print(A)
# print(A_sum)
# print("B")
# print(B)
# print(B_sum)

# 将统计结果转换成概率形式
