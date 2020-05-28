import numpy as np

a = (0, 0)
b = (1, -1)

print(max(a, b))

# .npy文件是numpy专用的二进制文件
arr = np.array([[1, 2], [3, 4]])

# 保存.npy文件
np.save("../data/test.npy", arr)
print("save .npy done")

# 读取.npy文件
pre_train = np.load("../data/labels.npy")
print(pre_train)
# print("load .npy done")
