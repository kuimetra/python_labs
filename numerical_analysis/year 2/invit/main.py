import numpy as np
import math
import sys


def get_matrix():
    try:
        mat = np.loadtxt(input("File name: ") + ".txt")
    except IOError as e:
        sys.exit(e)
    else:
        return mat


def sp_inverse_iteration(A, y, eps, lambda_value):
    previous_lambda_value, i = lambda_value, 1
    x = y / math.sqrt(np.dot(y, y))

    while True:
        y = np.dot(np.linalg.inv(A), x)
        s, t = np.dot(y, y), np.dot(y, x)
        x = y / math.sqrt(s)
        new_lambda_value = s / t

        print(f"{i})", new_lambda_value, x)
        if abs(new_lambda_value - previous_lambda_value) > eps:
            previous_lambda_value = new_lambda_value
            i += 1
        else:
            break
    return new_lambda_value, x


A = get_matrix()
print("A =", A)
y = np.array(list(map(float, input("y = ").split())))
eps = float(input("eps = "))
lambda_value = float(input("lambda = "))
smallest_eigenvalue, eigenvector = sp_inverse_iteration(A, y, eps, lambda_value)
print(f"\nSmallest eigenvalue = {smallest_eigenvalue}, eigenvector = {eigenvector}")
