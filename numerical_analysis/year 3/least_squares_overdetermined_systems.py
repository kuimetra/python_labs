import numpy as np
import sys


def get_matrix():
    try:
        matrix = np.loadtxt(input("File name: ") + ".txt")
    except IOError as e:
        sys.exit(e)
    else:
        return matrix[:, :matrix.shape[1] - 1], matrix[:, matrix.shape[1] - 1:]


A, b = get_matrix()
AT = A.T
ATA, ATb = AT @ A, AT @ b
x = np.linalg.inv(ATA) @ ATb
eps = b - A @ x
print("A =", A, "\nb =", b, "\n\nATA =", ATA, "\nATb =", ATb)
print("\nx =", x, "\neps =", eps, "\nMaximum absolute error:", np.abs(eps).max())
