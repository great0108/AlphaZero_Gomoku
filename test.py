import numpy as np

a = np.random.dirichlet(100*np.ones(10))
print(a, sum(a))