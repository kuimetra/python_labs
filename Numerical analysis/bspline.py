from matplotlib import pyplot as plt
import numpy as np

a, b = map(float, input("Enter a, b: ").split())
n = int(input("n = "))
x = [a + k * (b - a) / n for k in range(n + 1)]


def div(dividend, divisor):
    try:
        return dividend / divisor
    except ZeroDivisionError:
        return 0


def B(i, p, u, t):
    if p == 0:
        if t[i] <= u < t[i + 1]:
            return 1
        return 0
    return div((u - t[i]) * B(i, p - 1, u, t), (t[i + p] - t[i])) + div((t[i + p + 1] - u) * B(i + 1, p - 1, u, t),
                                                                        (t[i + p + 1] - t[i + 1]))


u_points = np.linspace(a, b, 250)
point, curve, plots = [], [], []
for degree in range(4):
    for m in range(n - degree):  # n = m + degree + 1 => m = n - degree - 1
        for u_point in u_points:
            point.append(B(m, degree, u_point, x))
        curve.append(point)
        point = []
    plots.append(curve)
    curve = []

fig, ax = plt.subplots(2, 2)
plot_index = 0
for row in range(2):
    for col in range(2):
        for cur in range(len(plots[plot_index])):
            ax[row, col].title.set_text(f'$B_{plot_index}(x)$')
            ax[row, col].set_xticks(np.arange(0, 251, 250 / n))
            ax[row, col].set_xticklabels(np.around(np.array(x), 3), rotation=45)
            ax[row, col].plot(plots[plot_index][cur])
        plot_index += 1
fig.suptitle(f'Curves on the interval [{a}, {b}] with {n + 1} equally spaced knots')
fig.tight_layout()
plt.show()
