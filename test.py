import numpy as np

a = np.zeros((2,2))
a[0] = (1,2)
print(a)

# import sys
# input = sys.stdin.readline

# def similar(a, b):
#     for i in range(min(len(a), len(b))):
#         if a[i] != b[i]:
#             return i
#     return min(len(a), len(b))


# n = 5
# aa = """abab
# abaa
# abcdab
# abcda
# abcdaa""".split("\n")
# arr = []
# for i in range(n):
#     arr.append([aa[i].strip(), i])
# arr2 = sorted(arr)
# print(arr2)
# result = 0
# idx = [0, 0]
# for i in range(n-1):
#     s = similar(arr2[i][0], arr2[i+1][0])
#     min_idx = min(arr2[i][1], arr2[i+1][1])
#     max_idx = max(arr2[i][1], arr2[i+1][1])
#     if s > result:
#         result = s
#         idx = [min_idx, max_idx]
#     elif s == result and idx[0] > min_idx:
#         idx = [min_idx, max_idx]
#     elif s == result and idx[0] == min_idx and idx[1] > max_idx:
#         idx = [min_idx, max_idx]
# print(idx)
# print(arr[idx[0]][0])
# print(arr[idx[1]][0])