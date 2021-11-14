from matplotlib import pyplot as plt
import numpy as np
import math


def f(func, x):
    return eval(func.lower(), {"x": x, "math": math})


def newton(x, y, n, value):
    coef = np.zeros([n, n + 1])
    coef[:, 0] = x
    coef[:, 1] = y
    for i in range(2, n + 1):
        for j in range(n + 1 - i):
            coef[j, i] = (coef[j + 1, i - 1] - coef[j, i - 1]) / (x[j + i - 1] - x[j])

    p = 0
    for k in range(1, n + 1):
        l = 1
        for i in range(0, k - 1):
            l *= (value - x[i])
        p += coef[0][k] * l
    return p


def get_plot_data(nodes, values, n, func):
    x = np.linspace(np.min(nodes), np.max(nodes), 100)
    y = [newton(nodes, values, int(n) + 1, i) for i in x]
    _y = [f(func, i) for i in x]
    return x, y, _y


a, b, amount_of_nodes = [float(i) for i in input("Enter a, b, amount of nodes (delimiter is \", \"): ").split(", ")]
chebychev_nodes = [(a + b) / 2 + (b - a) / 2 * math.cos((2 * k + 1) * math.pi / (2 * amount_of_nodes + 2))
                   for k in range(int(amount_of_nodes) + 1)]
equally_spaced_nodes = [a + (b - a) * k / amount_of_nodes for k in range(int(amount_of_nodes) + 1)]

function = input("Enter function (string parsed and evaluated as a Python expression): ")
interpolation_point = float(input("Enter interpolation point: "))

chebyshev_values = [f(function, node) for node in chebychev_nodes]
chebyshev_approx_val = newton(chebychev_nodes, chebyshev_values, int(amount_of_nodes) + 1, interpolation_point)
chebyshev_tolerance = math.fabs(f(function, interpolation_point) - chebyshev_approx_val)
print(f"\nChebyshev: {chebyshev_approx_val} is an approximate value of a function at the point {interpolation_point}")
chebyshev_x, chebyshev_y, chebyshev__y = get_plot_data(chebychev_nodes, chebyshev_values, amount_of_nodes, function)
print(f"Tolerance = {chebyshev_tolerance}")

equally_spaced_values = [f(function, node) for node in equally_spaced_nodes]
equally_spaced_approx_val = newton(equally_spaced_nodes, equally_spaced_values, int(amount_of_nodes) + 1,
                                   interpolation_point)
equally_spaced_tolerance = math.fabs(f(function, interpolation_point) - equally_spaced_approx_val)
print(f"Equally spaced: {equally_spaced_approx_val} is an approximate value of a function at the point "
      f"{interpolation_point}")
equally_spaced_x, equally_spaced_y, equally_spaced__y = get_plot_data(equally_spaced_nodes, equally_spaced_values,
                                                                      amount_of_nodes, function)
print(f"Tolerance = {equally_spaced_tolerance}")

if chebyshev_tolerance < equally_spaced_tolerance:
    print("\nThe approximate value of the function obtained with Chebyshev nodes is more accurate")
elif chebyshev_tolerance > equally_spaced_tolerance:
    print("\nThe approximate value of the function obtained with equally spaced nodes is more accurate")
else:
    print("\nChebyshev and equally spaced nodes provide the same approximate value of the function")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.set_title("Chebychev")
ax1.plot(chebyshev_x, chebyshev__y, color="steelblue")
ax1.plot(chebychev_nodes, chebyshev_values, '.', chebyshev_x, chebyshev_y, color="palevioletred")
ax2.set_title("Equally spaced")
ax2.plot(equally_spaced_x, equally_spaced__y, color="cadetblue")
ax2.plot(equally_spaced_nodes, equally_spaced_values, '.', equally_spaced_x, equally_spaced_y, color="lightcoral")
ax1.grid(color='silver', linestyle=':')
ax2.grid(color="silver", linestyle=':')
plt.show()
