x = 'ABCBDAD'
y = 'BDCABA'

n = len(x)
m = len(y)
k = [[0] * (m + 1) for i in range(n + 1)]
print([0] * 3)  # [0,0,0]
print(k)

for i in range(1, n + 1):
    for j in range(1, m + 1):
        if x[i - 1] == y[j - 1]:
            k[i][j] = k[i - 1][j - 1] + 1
        else:
            k[i][j] = max(k[i - 1][j], k[i][j - 1])
print(k[-1][-1])

for i in range(len(k)):
    print(k[i])
