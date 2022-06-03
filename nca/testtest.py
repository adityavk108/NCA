from pyexpat import model
import numpy as np
from sklearn.linear_model import LinearRegression
inp = np.array([[1 ,2 ,3], [4, 5, 6,], [7, 8, 9]])

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

w = w_ass

out = np.sum(w_ass * inp)
print(out)
