import matplotlib.pyplot as plt

h = float(input("Enter h: "))
n = int(input("Enter n: "))
eps = 1e-4


def u(x):
    return 1 / (x ** 2 + 1)


def u_(x, u):
    return -2 * x * u ** 2


x0, y0 = 0, 1
x = [x0]
for i in range(n - 1):
    x.append(x[-1] + h)

y_definite = [y0]
for i in range(1, 4):
    y_definite.append(u(x[i]))

y_rk4 = [y0]
for i in range(3):
    k1 = h * u_(x[i], y_rk4[-1])
    k2 = h * u_(x[i] + (h / 2), y_rk4[-1] + (k1 / 2))
    k3 = h * u_(x[i] + (h / 2), y_rk4[-1] + (k2 / 2))
    k4 = h * u_(x[i] + h, y_rk4[-1] + k3)
    y_rk4.append(y_rk4[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)

y_euler = [y0]
for i in range(3):
    y_euler.append(y_euler[-1] + h * u_(x[i], y_euler[-1]))


def adams(y):
    for i in range(len(x)):
        u = y[i + 3] + (h / 24) * (55 * u_(x[i + 3], y[i + 3]) - 59 * u_(x[i + 2], y[i + 2]) +
                                   37 * u_(x[i + 1], y[i + 1]) - 9 * u_(x[i], y[i]))
        y.append(round(u, 4))
        if len(y) == n:
            break
    return y


definite_adams, euler_adams, rk4_adams = adams(y_definite), adams(y_euler), adams(y_rk4)
print("\nx:", x)
print("\nDefinite:", definite_adams)
print("Tolerance:", abs(u(x[-1]) - definite_adams[-1]))
print("\nEuler:", euler_adams)
print("Tolerance:", abs(u(x[-1]) - euler_adams[-1]))
print("\nRK4:", rk4_adams)
print("Tolerance:", abs(u(x[-1]) - rk4_adams[-1]))

plt.plot(x, euler_adams, color='yellowgreen', label="Ейлера")
plt.plot(x, rk4_adams, color='plum', label="Рунге")
plt.plot(x, definite_adams, linestyle='--', color='royalblue', label="Точні")
plt.grid(color='lightgray', linestyle='--', linewidth=0.75)
plt.legend()
plt.show()
