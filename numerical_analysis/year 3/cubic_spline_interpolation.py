import matplotlib.pyplot as plt
import numpy as np
import math


def f(func, x):
    return eval(func.lower(), {"x": x, "math": math})


def tridiagonal_matrix_algorithm(arr, e):
    n = len(arr)
    a_diag, b_diag, c_diag = [arr[i][i - 1] for i in range(1, n)], [arr[i][i] for i in range(n)], \
                             [arr[i][i + 1] for i in range(n - 1)],
    a, b, c, d = map(np.array, (a_diag, b_diag, c_diag, e))
    for k in range(1, n):
        m = a[k - 1] / b[k - 1]
        b[k] = b[k] - m * c[k - 1]
        d[k] = d[k] - m * d[k - 1]
    z = b
    z[-1] = d[-1] / b[-1]
    for k in range(n - 2, -1, -1):
        z[k] = (d[k] - c[k] * z[k + 1]) / b[k]
    return z


def get_tridiagonal_matrix(f, h, n):
    matrix, vector = [[1] + [0] * (n - 1), [0] * (n - 1) + [1]], [0, 0]
    for k in range(2, n):
        arr = [0] * n
        arr[k - 2] = h[k - 2]
        arr[k - 1] = 2 * (h[k - 2] + h[k - 1])
        arr[k] = h[k - 1]
        matrix.insert(-1, arr)
        vector.insert(-1, 3 * (f[k - 1] - f[k - 2]))
    return matrix, vector


def get_d_coefficient(c, h, n):
    return [(c[k] - c[k - 1]) / (3 * h[k - 1]) for k in range(1, n)]


def get_b_coefficient(c, f, h, n):
    return [f[k - 1] + 2 / 3 * h[k - 1] * c[k] + 1 / 3 * h[k - 1] * c[k - 1] for k in range(1, n)]


def get_g_function(x_k, a, b, c, d, x):
    return a + b * (x - x_k) + c * (x - x_k) ** 2 + d * (x - x_k) ** 3


option = int(input("Enter (1) - function and x or (2) - x and y: "))
if option == 1:
    function = input("Enter function (string parsed and evaluated as a Python expression): ")  # 3 * math.cos(15 * x)
    x = list(map(float, input("Enter x: ").split(", ")))  # -4.25, -2, -1, 0, 1, 1.5, 2, 3
    y = [f(function, x_i) for x_i in x]
    print("y:", np.round(y, 3))
elif option == 2:
    x = list(map(float, input("Enter x: ").split(", ")))  # -2, -1, 0, 1, 1.5, 2, 3
    y = list(map(float, input("Enter y: ").split(", ")))  # 3, 1, 1, 2, 3, 1, 4

if option == 1 or option == 2:
    if len(x) == len(y) and len(x) > 1 and len(y) > 1:
        n = len(x)
        h = [x[k] - x[k - 1] for k in range(1, n)]
        f = [(y[k + 1] - y[k]) / h[k] for k in range(n - 1)]
        H, e = get_tridiagonal_matrix(f, h, n)
        c = tridiagonal_matrix_algorithm(H, e)
        d = get_d_coefficient(c, h, n)
        b = get_b_coefficient(c, f, h, n)

        y_points, x_new, y_new = [], [], []
        for k in range(1, n):
            for x_r in np.linspace(x[k - 1], x[k], 50):
                y_points.append(get_g_function(x[k], y[k], b[k - 1], c[k], d[k - 1], x_r))
            x_new.append(np.linspace(x[k - 1], x[k], 50))
            y_new.append(y_points)
            y_points = []

        for x_n, y_n in zip(x_new, y_new):
            plt.plot(x_n, y_n)

        plt.plot(x, y, 'o')
        plt.title("Cubic Spline Interpolation")
        plt.grid(color='silver', linestyle=':')
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()