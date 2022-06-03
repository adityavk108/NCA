import numpy as np
from sklearn.linear_model import LinearRegression
from time import perf_counter
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

    c = inp[1, 1] - np.sum(inp * w_ass)
    return w_ass, c

x = np.random.rand(3, 3)
start = perf_counter()
y, c = regression(x)
end = perf_counter()
print("x:")
print(x)
print("y:")
print(y)
out = np.sum(x * y)
print("added:")
print(out + c)
print(f"time: {end - start}")

# filename = r"C:\newprojects\NCA_project\r_nca\test.png"
# np_image = np.asarray(Image.open(filename))

