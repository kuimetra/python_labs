from tabulate import tabulate
import math


def f(x):
    return x ** 2 - x + 2


x = float(input("Enter x0: "))  # 0
h = float(input("Enter h0: "))  # 0.5

a, b = None, None
move_to_next_step = False

f_x, f_xh = f(x), f(x + h)
if f_x < f_xh:
    h = -h
    if f(x - h) <= f_x >= f_xh:
        print("Function is not unimodal on a given interval.")
    else:
        move_to_next_step = True

if f_x > f_xh or move_to_next_step:
    x_arr = []
    while f(x) >= f(x + h):
        x = x + h
        x_arr.append(x)
        h *= 2
    x_arr.append(x + h)
    x_arr.append(x_arr[-1] - h / 2)
    sorted_x_arr = sorted(x_arr[-4:])
    sorted_x_arr.pop(0 if f(sorted_x_arr[0]) > f(sorted_x_arr[-1]) else -1)
    a, b = sorted_x_arr[0], sorted_x_arr[-1]

print(f"{a = }, {b = }")
delta = float(input("\nEnter delta: "))  # 1e-8
eps = 0.2

table = []
k = 1
while abs(a - b) > eps:
    y, z = (a + b - delta) / 2, (a + b + delta) / 2
    f_y, f_z = f(y), f(z)
    if f_y <= f_z:
        b = z
    else:
        a = y

    table.append([k, y, z, f_y, f_z, a, b, abs(a - b)])
    k += 1

print(tabulate(table, headers=["k", "y", "z", "f(y)", "f(z)", "a", "b", "|a - b|"]))
print(f"Approximate value of the function with the accuracy of {eps} is {(a + b) / 2}")
