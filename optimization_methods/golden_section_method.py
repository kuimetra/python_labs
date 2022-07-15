from tabulate import tabulate
import math


def f(x):
    return 2 * x ** 2 - 12 * x


a, b = 1, 5
eps = 1

x1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
x2 = a + b - x1
table = [[0, x1, x2, f(x1), f(x2), [a, b], abs(a - b)]]
k = 1

while abs(a - b) > eps:
    if f(x1) > f(x2):
        a = x1
        x1 = x2
        x2 = a + b - x1
    else:
        b = x2
        x2 = x1
        x1 = a + b - x2

    table.append([k, x1, x2, f(x1), f(x2), [a, b], abs(a - b)])
    k += 1

print(tabulate(table, headers=["k", "x1", "x2", "f(x1)", "f(x2)", "[a, b]", "|a - b|"]))
print(f"Approximate value of the function is {round((x1 + x2) / 2, 5)}")
