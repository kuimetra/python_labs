from math import exp, sin, cos, pi
import matplotlib.pyplot as plt
import numpy as np


def f(func, x):
    if func == "g":
        return exp(sin(x) + cos(x))
    elif func == "h":
        return 3 * cos(15 * x)


def get_x(n):
    return [pi * i / n for i in range(2 * n)]


def get_y(func, x):
    return [f(func, i) for i in x]


def get_a(x, y, n):
    return [sum(round((y[i] * cos(x[i] * k)) / n, 10) for i in range(2 * n)) for k in range(n + 1)]


def get_b(x, y, n):
    return [sum(round((y[i] * sin(x[i] * k)) / n, 10) for i in range(2 * n)) for k in range(1, n)]


def get_q(a, b, n, t):
    return a[0] / 2 + sum(a[k] * cos(k * t) + b[k - 1] * sin(k * t) for k in range(1, n)) + a[n] / 2 * cos(n * t)


def get_plot_data(a, b, option, n):
    x = np.linspace(0, 2 * pi, 500)
    y = [get_q(a, b, n, t) for t in x]
    _y = [f(option, i) for i in x]
    return x, y, _y


n = int(input("Enter degree of a polynomial (even number only): "))
if n % 2 == 0:
    x = get_x(n)
    g_y, h_y = get_y("g", x), get_y("h", x)
    g_a, g_b = get_a(x, g_y, n), get_b(x, g_y, n)
    h_a, h_b = get_a(x, h_y, n), get_b(x, h_y, n)
    g_x, g__y, g___y = get_plot_data(g_a, g_b, "g", n)
    h_x, h__y, h___y = get_plot_data(h_a, h_b, "h", n)
    print(f"\na_i of g(x): {g_a}\nb_i of g(x): {g_b}\n\na_i of h(x): {h_a}\nb_i of h(x): {h_b}")

    fig, (g_func, h_func) = plt.subplots(1, 2, figsize=(11, 4))
    g_func.set_title("g(x) = exp(sin(x) + cos(x))")
    g_func.plot(g_x, g___y, color="lightblue")  # polynomial plot
    g_func.plot(x, g_y, 'o', g_x, g__y, '--', color="palevioletred")  # function plot
    h_func.set_title("h(x) = 3 * cos(15 * x)")
    h_func.plot(h_x, h___y, color="lightblue")  # polynomial plot
    h_func.plot(x, h_y, 'o', h_x, h__y, '--', color="palevioletred")  # function plot
    g_func.grid(color='silver', linestyle=':')
    h_func.grid(color="silver", linestyle=':')
    plt.show()
