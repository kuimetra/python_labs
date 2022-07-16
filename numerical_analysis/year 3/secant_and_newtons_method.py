import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np


def f(x):
    return x ** 4 - 10 * x ** 3 - 1


def f_1der(x):
    return 4 * x ** 3 - 30 * x ** 2


def f_2der(x):
    return 12 * x ** 2 - 60 * x


def get_secant_x(prev_x, c):
    return prev_x - f(prev_x) / (f(prev_x) - f(c)) * (prev_x - c)


def get_newtons_x(prev_x):
    return prev_x - f(prev_x) / f_1der(prev_x)


x = np.arange(-0.5, -0.3, 0.1)
y = [f(i) for i in x]
plt.plot(x, y)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.show()

a, b = map(float, input("Enter a, b: ").split())  # -0.46 -0.44
eps = float(input("Enter eps: "))


def get_secant_table():
    table = []
    c, x = None, None

    if f(a) * f_2der(a) > 0:
        c = a
    elif f(b) * f_2der(b) > 0:
        c = b

    if f(a) * f_2der(a) < 0:
        x = a
    elif f(b) * f_2der(b) < 0:
        x = b

    k = 0
    next_x = get_secant_x(x, c)

    while abs(x - next_x) > eps:
        table.append([k, a, b, abs(x - next_x), c, x])
        x = next_x
        next_x = get_secant_x(x, c)
        k += 1
    table.append([k, a, b, abs(x - next_x), c, x])

    return table


def get_newtons_table():
    table = []
    x = None

    if f(a) * f_2der(a) > 0:
        x = a
    elif f(b) * f_2der(b) > 0:
        x = b

    k = 0
    next_x = get_newtons_x(x)

    while abs(x - next_x) > eps:
        table.append([k, a, b, abs(x - next_x), x])
        x = next_x
        next_x = get_newtons_x(x)
        k += 1
    table.append([k, a, b, abs(x - next_x), x])

    return table


secant_table, newtons_table = get_secant_table(), get_newtons_table()
print("\n", tabulate(secant_table, headers=["k", "a", "b", "|x(k) - x(k+1)|", "нерухома точка", "x"]))
print("\n", tabulate(newtons_table, headers=["k", "a", "b", "|x(k) - x(k+1)|", "x"]))
