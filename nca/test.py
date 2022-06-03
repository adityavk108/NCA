import numpy as np
from sklearn.linear_model import LinearRegression
# x = np.random.randint(10, size=(5, 5))
# x = np.ones((5, 5))
# print(x)
# filter = np.ones((3, 3))

# new = x.copy()
# target = np.zeros((3, 3), dtype=np.float64)
# maxrow = x.shape[0] - 1
# maxcol = x.shape[1] - 1
# for j in range(x.shape[1]): #[0, 2, 4, 0, 2, 4, 0, 2, 4]:
#     for i in range(x.shape[0]): #[0, 0, 0, 2, 2, 2, 4, 4, 4]:
#         if i == 0 or j == 0 or i == maxrow or j == maxcol:
#             for tr in range(3):
#                 for tc in range(3):
#                     r = i - 1 + tr
#                     c = j - 1 + tc
#                     if r < 0:
#                         r = maxrow
#                     if c < 0:
#                         c = maxcol

#                     if r > maxrow:
#                         r = 0
#                     if c > maxcol:
#                         c = 0

#                     target[tr, tc] = x[r, c]
#         else:
#             target = x[i-1:i+2, j-1:j+2]
#         prod = target * filter
#         out = float(prod.sum())
#         new[i, j] = out
#         target = np.zeros((3, 3), dtype=np.float64)
# canvas = new

# print(canvas)

"""algorithm converts 3,3 matrix into a value y (center value- value) and a vector x (surrounding values- vector) for linear regression.
x is converged to give y as hypothesis, and weight and bias values are reassembled into 3,3 and returned."""
def regression(inp):
    #extract key value pairs
    x = np.zeros((9))
    x[0:3] = inp[0, :]
    x[3:5] = inp[1, ::2]
    x[5:8] = inp[2, :]
    x[8] = 1
    y = inp[1, 1]

    #train model and extract weights
    model = LinearRegression(fit_intercept=False)
    model.fit([x], [y])
    w = model.coef_
    #assemble theta
    w_ass = np.zeros((3, 3))
    w_ass[0, :] = w[0:3]
    w_ass[1, ::2] = w[3:5]
    w_ass[2, :] =  w[5:8]
    return w_ass
