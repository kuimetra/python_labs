from tabulate import tabulate
import numpy as np
import math


def f(x):
    return x[0] ** 2 + 2 * x[1] ** 2 + pow(math.e, x[0] ** 2 + x[1] ** 2) - x[0] + 2 * x[1]


def df_x1(x1, x2):
    return 2 * x1 + 2 * pow(math.e, x1 ** 2 + x2 ** 2) * x1 - 1


def df_x2(x1, x2):
    return 4 * x2 + 2 * pow(math.e, x1 ** 2 + x2 ** 2) * x2 + 2


def norm(x1, x2):
    return math.sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2)


def steffensen(x_, x0):
    df1 = [df_x1(x0[0], x0[1]),
           df_x2(x0[0], x0[1])]
    df2 = [df_x1(x_[0], x_[1]),
           df_x2(x_[0], x_[1])]
    df3 = [df_x1(x0[0], x_[1]),
           df_x2(x0[0], x_[1])]
    df4 = [df_x1(x_[0], x0[1]),
           df_x2(x_[0], x0[1])]

    m = np.zeros((2, 2))
    for i in range(2):
        m[i][0] = ((df3[i] - df2[i]) / (x0[0] - x_[0]))
        m[i][1] = ((df4[i] - df3[i]) / (x0[1] - x_[1]))

    mul = alpha * np.linalg.inv(m).dot(df1)
    xk = [x0[0] - mul[0], x0[1] - mul[1]]
    x_ = [xk[0] - lambda_ * df_x1(xk[0], xk[1]), xk[1] - lambda_ * df_x2(xk[0], xk[1])]
    return xk, x_


lambda_, eps = 1e-4, 1e-5
alpha = 1
x0 = [1, 1]
x_ = [x0[0] - lambda_ * df_x1(x0[0], x0[1]), x0[1] - lambda_ * df_x2(x0[0], x0[1])]
x1, x_ = steffensen(x_, x0)

table = []
k = 0

while f(x1) >= f(x0):
    alpha = alpha / 2
    x1, x_ = steffensen(x_, x0)
x0 = x1
x1, x_ = steffensen(x_, x0)
table.append([k, x1, f(x1)])

while norm(x0, x1) > eps:
    k += 1
    alpha = 1
    while f(x1) >= f(x0):
        alpha = alpha / 2
        x1, x_ = steffensen(x_, x0)
    x0 = x1
    x1, x_ = steffensen(x_, x0)
    table.append([k, x1, f(x1)])
print(tabulate(table, headers=["k", "x[k]", "f(x[k])"]))
