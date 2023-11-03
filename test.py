import numpy as np

# a = np.zeros((2,2))
# a[0] = (1,2)
# print(a)

import sys
input=sys.stdin.readline
L=[0.500, 0.333, 0.090]
a=len(L)
for count in range(1,1000) :
    possible=0
    for i in range(a) :
        if L[i]==0 :
            possible+=1
            continue
        if L[i]*count>=1 :
            if L[i]*count<=round(L[i]*count) and ((L[i]+0.0009)*count)>=round((L[i]+0.0009)*count) and round(L[i]*count)==round((L[i]+0.0009)*count) :
                possible+=1
    if possible==a :
        print(count)
        break

# for i in range(1, 100):
#     print(1/i)