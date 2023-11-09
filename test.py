import numpy as np
from renju import Renju_Rule

a = [1,2]
b = [3,4]
print(a + b)
rule = Renju_Rule([
    [2,0,0,0,0,0,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,0,1,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,0,0,0,0,0,2],
], 7)
print(rule.get_forbidden_points(1))