import numpy as np

a = [[np.array([[1,],[1,],[1,]]), np.array([[11,],[11,]])], [np.array([[2,],[2,],[2,]]), np.array([[22,],[22,]])]]
b1 = np.row_stack(n[0].reshape([1,3]) for n in a)
b2 = np.row_stack(n[1].reshape([1,2]) for n in a)
b = [b1, b2]
print(a)
print(b)