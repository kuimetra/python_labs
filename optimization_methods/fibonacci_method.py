from tabulate import tabulate
import math


def f(x):
    return 2 * x ** 2 - 12 * x


x = float(input("Enter x0: "))
h = float(input("Enter h0: "))
eps = float(input("Enter eps: "))

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
    x_arr = [x]
    while f(x) >= f(x + h):
        x = x + h
        x_arr.append(x)
        h *= 2
    x_arr.append(x + h)
    x_arr.append(x_arr[-1] - h / 2)
    sorted_x_arr = sorted(x_arr[-4:])
    sorted_x_arr.pop(0 if f(sorted_x_arr[0]) > f(sorted_x_arr[-1]) else -1)
    a, b = sorted_x_arr[0], sorted_x_arr[-1]

print(f"\n{a = }, {b = }")

fibonacci_seq = [1, 1]
while fibonacci_seq[-1] < (b - a) / eps:
    fibonacci_seq.append(fibonacci_seq[-2] + fibonacci_seq[-1])
n = len(fibonacci_seq) - 1
print(fibonacci_seq, f"{n = }\n")

x1 = a + fibonacci_seq[n - 2] / fibonacci_seq[n] * (b - a)
x2 = a + fibonacci_seq[n - 1] / fibonacci_seq[n] * (b - a)

table = []
for k in range(1, n):
    table.append([*map(lambda val: round(val, ndigits=5), [k, x1, x2, f(x1), f(x2), a, b, abs(a - b)])])
    if f(x1) > f(x2):
        a = x1
        x1 = x2
        x2 = a + fibonacci_seq[n - k] / fibonacci_seq[n - k + 1] * (b - a)
    else:
        b = x2
        x2 = x1
        x1 = a + fibonacci_seq[n - k - 1] / fibonacci_seq[n - k + 1] * (b - a)

print(tabulate(table, headers=["k", "x1", "x2", "f(x1)", "f(x2)", "a", "b", "|a - b|"]))
print(f"Approximate value of the function is {round((x1 + x2) / 2, 5)}")
