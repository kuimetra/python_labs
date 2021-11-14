import numpy as np
from math import sqrt


def get_matrix():
    return np.loadtxt("test.txt")


def is_symmetric(matrix):
    return (matrix.T == matrix).all()


def is_positive_definite(n, matrix):
    for i in range(1, n + 1):
        if np.linalg.det(matrix[:i, :i]) > 0:
            continue
        else:
            return False
    return True


def get_matrix_u(n, matrix):
    u = np.zeros_like(matrix)
    for i in range(n):
        for j in range(n):
            if i == j:
                u[i, j] = sqrt(matrix[i, j] - np.sum(u[:i, j] ** 2))
            elif i < j and j > 0:
                u[i, j] = (matrix[i, j] - np.sum(u[:i, i] * u[:i, j])) / u[i, i]
            elif i > j:
                u[i, j] = 0
    return u


def find_y(n, b, u):
    y = np.mat([0.0 for _ in range(n)]).T
    for i in range(n):
        y[i, 0] = (b[i, 0] - np.sum(u[:i, i] * y[:i, 0])) / u[i, i]
    return y


def find_x(n, y, u):
    x = np.mat([0.0 for _ in range(n)]).T
    for i in range(n - 1, -1, -1):
        x[i, 0] = (y[i, 0] - np.sum(u[i, i + 1:] * x[i + 1:, 0])) / u[i, i]
    return x


mat = get_matrix()
size = mat.shape[0]
A, b = mat[:, :size], mat[:, size:]
print("A =", A, "\nb =", b)

if not is_symmetric(A):
    print("Matrix is not symmetric.")
elif not is_positive_definite(size, A):
    print("Matrix is not positive definite.")
else:
    u = get_matrix_u(size, A)
    y = find_y(size, b, u)
    x = find_x(size, y, u)
    print("\nU =", u, "\nU.T =", u.T)
    print("\ny =", y.T, "\nx =", x.T)
