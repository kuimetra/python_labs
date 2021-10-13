from matplotlib import pyplot as plt
import numpy as np
import math


def f(func, x):
    return eval(func.lower(), {"x": x, "math": math})


def lagrange(ip, nodes, values):
    L_x = 0
    for i in range(len(nodes)):
        fraction = 1
        for j in range(len(nodes)):
            if i != j:
                fraction *= (ip - nodes[j]) / (nodes[i] - nodes[j])
        L_x += values[i] * fraction
    return L_x


def get_plot_data(nodes, values, func):
    x = np.linspace(np.min(nodes), np.max(nodes), 100)
    y = [lagrange(i, nodes, values) for i in x]
    _y = [f(func, i) for i in x]
    return x, y, _y


a, b, amount_of_nodes = [float(i) for i in input("Enter a, b, amount of nodes (delimiter is \", \"): ").split(", ")]
chebychev_nodes = [(a + b) / 2 + (b - a) / 2 * math.cos((2 * k + 1) * math.pi / (2 * amount_of_nodes + 2))
                   for k in range(int(amount_of_nodes) + 1)]
equally_spaced_nodes = [a + (b - a) * k / amount_of_nodes for k in range(int(amount_of_nodes) + 1)]

function = input("Enter function (string parsed and evaluated as a Python expression): ")
interpolation_point = float(input('Enter interpolation point: '))

chebyshev_values = [f(function, node) for node in chebychev_nodes]
chebyshev_approx_val = lagrange(interpolation_point, chebychev_nodes, chebyshev_values)
chebyshev_tolerance = math.fabs(f(function, interpolation_point) - chebyshev_approx_val)
print(f"\nChebyshev: {chebyshev_approx_val} is an approximate value of a function at the point {interpolation_point}")
chebyshev_x, chebyshev_y, chebyshev__y = get_plot_data(chebychev_nodes, chebyshev_values, function)
print(f"Tolerance = {chebyshev_tolerance}")

equally_spaced_values = [f(function, node) for node in equally_spaced_nodes]
equally_spaced_approx_val = lagrange(interpolation_point, equally_spaced_nodes, equally_spaced_values)
equally_spaced_tolerance = math.fabs(f(function, interpolation_point) - equally_spaced_approx_val)
print(f"Equally spaced: {equally_spaced_approx_val} is an approximate value of a function at the point "
      f"{interpolation_point}")
equally_spaced_x, equally_spaced_y, equally_spaced__y = get_plot_data(equally_spaced_nodes, equally_spaced_values,
                                                                      function)
print(f"Tolerance = {equally_spaced_tolerance}")

if chebyshev_tolerance < equally_spaced_tolerance:
    print("\nThe approximate value of the function obtained with Chebyshev nodes is more accurate")
elif chebyshev_tolerance > equally_spaced_tolerance:
    print("\nThe approximate value of the function obtained with equally spaced nodes is more accurate")
else:
    print("\nChebyshev and equally spaced nodes provide the same approximate value of the function")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(chebyshev_x, chebyshev__y, color="steelblue")
ax1.plot(chebychev_nodes, chebyshev_values, '.', chebyshev_x, chebyshev_y, color="palevioletred")
ax1.set_title("Chebychev")
ax2.plot(equally_spaced_x, equally_spaced__y, color="cadetblue")
ax2.plot(equally_spaced_nodes, equally_spaced_values, '.', equally_spaced_x, equally_spaced_y, color="lightcoral")
ax2.set_title("Equally spaced")
ax1.grid(color='silver', linestyle=':')
ax2.grid(color="silver", linestyle=':')
plt.show()

################################################ Input&Output Example ################################################

# Enter a, b, amount of nodes (delimiter is ", "): -1, 1, 6
# Enter function (string parsed and evaluated as a Python expression): 1/(1+25*x**2)
# Enter interpolation point: 0.25
#
# Chebyshev: 0.6440178680580554 is an approximate value of a function at the point 0.25
# Tolerance = 0.253773965619031
# Equally spaced: 0.5296524670517079 is an approximate value of a function at the point 0.25
# Tolerance = 0.13940856461268347
#
# The approximate value of the function obtained with equally spaced nodes is more accurate


# Enter a, b, amount of nodes (delimiter is ", "): -1, 1, 4
# Enter function (string parsed and evaluated as a Python expression): math.log(x+2)
# Enter interpolation point: 0.863
#
# Chebyshev: 1.052192716667551 is an approximate value of a function at the point 0.863
# Tolerance = 0.0003226905515731904
# Equally spaced: 1.052510802589207 is an approximate value of a function at the point 0.863
# Tolerance = 0.0006407764732290211
#
# The approximate value of the function obtained with Chebyshev nodes is more accurate
