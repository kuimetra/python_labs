from tabulate import tabulate
import numpy as np
import math


def f(x):
    return x[0] ** 2 + 2 * x[1] ** 2 + pow(math.e, x[0] ** 2 + x[1] ** 2) - x[0] + 2 * x[1]


def derivative(x):
    return 2 * x[0] + 2 * pow(math.e, x[0] ** 2 + x[1] ** 2) * x[0] - 1, \
           4 * x[1] + 2 * pow(math.e, x[0] ** 2 + x[1] ** 2) * x[1] + 2


alpha = 1
x = [1, 1]
xk = [a - b for a, b in zip(x, [alpha * d for d in derivative(x)])]
while f(xk) >= f(x):
    alpha /= 2
    xk = [a - b for a, b in zip(x, [alpha * d for d in derivative(x)])]

eps = 1e-6
k = 1
table = [[k, alpha, (round(x[0], 5), round(x[1], 5)), (round(xk[0], 5), round(xk[1], 5)), f(x), f(xk),
          abs(f(xk) - f(x)) <= eps]]

if np.linalg.norm(derivative(x)) <= eps:
    table.append([k, alpha, (round(x[0], 5), round(x[1], 5)), (round(xk[0], 5), round(xk[1], 5)), f(x), f(xk),
                  abs(f(xk) - f(x)) <= eps])
else:
    while abs(f(xk) - f(x)) > eps:
        alpha = 1
        x = xk
        xk = [a - b for a, b in zip(x, [alpha * d for d in derivative(x)])]
        while f(xk) >= f(x):
            alpha /= 2
            xk = [a - b for a, b in zip(x, [alpha / 2 * d for d in derivative(x)])]
        k += 1
        table.append([k, alpha, (round(x[0], 5), round(x[1], 5)), (round(xk[0], 5), round(xk[1], 5)), f(x), f(xk),
                      abs(f(xk) - f(x)) <= eps])

    print(tabulate(table,
                   headers=["k", "alpha", "x[k]", "x[k+1]", "f(x[k])", "f(x[k+1])", "|f(x[k+1]) - f(x[k])| <= eps"]))
