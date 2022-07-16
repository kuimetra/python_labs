import numpy as np
import math


def f(x):
    return 1 / x


def F(x):
    return math.log(abs(x))


def get_parameters(rule_index, a, b, n):
    h = (b - a) / n
    x = np.arange(a, b + h, h)
    if rule_index == 0:
        y = [f(x_i + (h / 2)) for x_i in x]
        approx_integral = sum(h * np.array([y_i for y_i in y]))
    elif rule_index == 1:
        y = [f(x_i) for x_i in x]
        approx_integral = sum(h / 2 * np.array([y[i] if i == 0 or i == len(y) - 1 else 2 * y[i]
                                                for i in range(len(y))]))
    elif rule_index == 2:
        y = [f(x_i) for x_i in x]
        approx_integral = sum(h / 3 * np.array([y[i] if i == 0 or i == len(y) - 1 else
                                                2 * y[i] if i % 2 == 0 else 4 * y[i] for i in range(len(y))]))
    return h, x, y, approx_integral


amount_of_intervals = int(input("Enter amount of intervals: "))
a, b = 1, 2
tolerance = 1e-6
definite_integral = F(b) - F(a)
rule_details = {"Rectangle": 2, "Trapezoid": 2, "Simpson's": 4}

for rule_index, (rule_name, p) in enumerate(rule_details.items()):
    step = 1
    n = amount_of_intervals
    h1, x1, fx1, approx_integral1 = get_parameters(rule_index, a, b, n)
    while True:
        n *= 2
        h2, x2, fx2, approx_integral2 = get_parameters(rule_index, a, b, n)
        eps = abs(approx_integral1 - approx_integral2) / (2 ** p - 1)
        if eps <= tolerance:
            break
        step += 1
        h1, x1, fx1, approx_integral1 = h2, x2, fx2, approx_integral2

    print(f"""\n[ {rule_name} rule ]
It took {step} {"steps" if step > 1 else "step"}
Approximate integral: {approx_integral2}
Amount of intervals: {n}
Tolerance: {eps}
Definite integral: {definite_integral}
Diff between definite and approximate integral: {abs(definite_integral - approx_integral2)}""")
