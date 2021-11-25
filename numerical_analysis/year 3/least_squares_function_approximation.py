import matplotlib.pyplot as plt
import numpy as np
import math


def f(func, x):
    return eval(func.lower(), {"x": x, "math": math})


option = int(input("Enter (1) - function and x or (2) - x and y: "))
if option == 1:
    function = input("Enter function (string parsed and evaluated as a Python expression): ")  # 4 * math.cos(4 * x)
    x = list(map(float, input("Enter x: ").split(", ")))  # -3.25, -2, -1, 0, 1, 1.5, 2, 4.6
    y = [f(function, x_i) for x_i in x]
    print("y:", np.round(y, 3))
elif option == 2:
    x = list(map(float, input("Enter x: ").split(", ")))  # -3, -1, 0, 1, 3
    y = list(map(float, input("Enter y: ").split(", ")))  # -4, -0.8, 1.6, 2.3, 1.5

if option == 1 or option == 2:
    if not all(x[i] <= x[i + 1] for i in range(len(x) - 1)):
        y = [y[i] for i in np.argsort(x)]
        x.sort()

    for d in range(1, 4):
        s = [sum(x[i] ** k for i in range(len(x))) for k in range(2 * d + 1)]
        t = [sum((x[i] ** k) * y[i] for i in range(len(x))) for k in range(d + 1)]
        mat = [s[i:i + d + 1] for i in range(d + 1)]
        a = np.linalg.inv(mat) @ t
        print("-" * 20, "Degree =", d, "-" * 20)
        print("matrix:", mat, "\nvector:", t)
        print("a:", a, "\n")
        new_x = np.linspace(min(x), max(x), 250)
        new_y = [sum(a[i] * (x_i ** i) for i in range(d + 1)) for x_i in new_x]
        plt.plot(new_x, new_y, '-', label=f"degree = {d}")

    plt.plot(x, y, '--', label="function")
    plt.legend(loc="lower right")
    plt.grid(color='silver', linestyle=':')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
