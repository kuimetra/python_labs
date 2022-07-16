import matplotlib.pyplot as plt
import math


def f(y, z):
    return 2 * y + z


def g(y, z):
    return 3 * y + 4 * z


def f_(x):
    return -math.e ** x + math.e ** (5 * x)


def g_(x):
    return math.e ** x + 3 * math.e ** (5 * x)


a, b = 0, 0.5
n = 50
h = (b - a) / n
x = [a + i * h for i in range(n + 1)]
y_euler_method, z_euler_method = [0], [4]
for i in range(n):
    y_euler_method.append(y_euler_method[-1] + h * f(y_euler_method[-1], z_euler_method[-1]))
    z_euler_method.append(z_euler_method[-1] + h * g(y_euler_method[-1], z_euler_method[-1]))

y_ = [f_(i) for i in x]
z_ = [g_(i) for i in x]

y_rk4_method, z_rk4_method = [0], [4]
for i in range(n):
    k1 = h * f(y_rk4_method[-1], z_rk4_method[-1])
    l1 = h * g(y_rk4_method[-1], z_rk4_method[-1])
    k2 = h * f(y_rk4_method[-1] + k1 / 2, z_rk4_method[-1] + l1 / 2)
    l2 = h * g(y_rk4_method[-1] + k1 / 2, z_rk4_method[-1] + l1 / 2)
    k3 = h * f(y_rk4_method[-1] + k2 / 2, z_rk4_method[-1] + l2 / 2)
    l3 = h * g(y_rk4_method[-1] + k2 / 2, z_rk4_method[-1] + l2 / 2)
    k4 = h * f(y_rk4_method[-1] + k3, z_rk4_method[-1] + l3)
    l4 = h * g(y_rk4_method[-1] + k3, z_rk4_method[-1] + l3)
    y_rk4_method.append(y_rk4_method[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    z_rk4_method.append(z_rk4_method[-1] + (l1 + 2 * l2 + 2 * l3 + l4) / 6)

plt.plot(x, y_, color='lightblue', linewidth=3)
plt.plot(x, y_euler_method, color='cornflowerblue', linestyle='--')
plt.plot(x, y_rk4_method, color='forestgreen', linestyle='--')
plt.plot(x, z_, color='pink', linewidth=3)
plt.plot(x, z_euler_method, color='mediumvioletred', linestyle='--')
plt.plot(x, z_rk4_method, color='darkviolet', linestyle='--')
plt.legend(['y*', 'y Euler method', 'y RK4 method', 'z*', 'z Euler method', 'z RK4 method'])
plt.grid(color='lightgray', linestyle='--', linewidth=0.75)
plt.show()
