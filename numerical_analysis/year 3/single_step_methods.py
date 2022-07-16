import matplotlib.pyplot as plt
import math


def f(x, y):
    return math.cos(y - x)


def f_(x):
    return x + 2 * math.atan(1 / x)


a, b = 1, 2
n = 10
h = (b - a) / n
x = [a + i * h for i in range(n + 1)]
y0 = 2.57
y = [f_(i) for i in x]

y_euler_method = [y0]
for i in range(n):
    y_euler_method.append(y_euler_method[-1] + h * f(x[i], y_euler_method[-1]))

y_rk4_method = [y0]
for i in range(n):
    k1 = h * f(x[i], y_rk4_method[-1])
    k2 = h * f(x[i] + h / 2, y_rk4_method[-1] + k1 / 2)
    k3 = h * f(x[i] + h / 2, y_rk4_method[-1] + k2 / 2)
    k4 = h * f(x[i] + h, y_rk4_method[-1] + k3)
    y_rk4_method.append(y_rk4_method[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)

plt.plot(x, y, color='yellowgreen', linewidth=3)
plt.plot(x, y_euler_method, color='mediumpurple')
plt.plot(x, y_rk4_method, color='lightcoral')
plt.legend(['f*', 'Euler method', 'RK4 method'])
plt.grid(color='lightgray', linestyle='--', linewidth=0.75)
plt.show()
