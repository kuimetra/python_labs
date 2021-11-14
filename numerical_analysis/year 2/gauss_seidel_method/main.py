import numpy as np
import sys


def get_matrix():
    try:
        file = np.loadtxt(input("File name: ") + ".txt")
    except IOError as e:
        sys.exit(e)
    else:
        return file


def is_symmetric(mat):
    return (mat.T == mat).all()


def is_positive_definite(mat, size):
    if all(np.linalg.det(mat[:i, :i]) > 0 for i in range(1, size + 1)):
        return True
    return False


def is_diagonally_dominant(mat, size):
    if any(abs(mat[i][i]) < np.absolute(mat).sum(axis=1)[i] - abs(mat[i][i]) for i in range(size)):
        return False
    return True


def gauss_seidel(A, b, size, eps):
    x, times = np.zeros(size), 0
    while True:
        print(times, x)
        previous_x = np.copy(x)
        for i in range(size):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i)) - sum(
                A[i][j] * previous_x[j] for j in range(i + 1, size))) / A[i][i]  # j!=i
        if np.sqrt(sum((x[i] - previous_x[i]) ** 2 for i in range(size))) <= eps:
            break
        times += 1


if __name__ == "__main__":
    matrix = get_matrix()
    matrix_size = matrix.shape[0]
    matrix_A, matrix_b = matrix[:, :matrix_size], matrix[:, matrix_size:]
    print("A =", matrix_A, "\nb =", matrix_b)

    if (is_symmetric(matrix_A) and is_positive_definite(matrix_A, matrix_size)) or is_diagonally_dominant(matrix_A,
                                                                                                          matrix_size):
        calc_accuracy = float(input("Calculation accuracy = "))
        gauss_seidel(matrix_A, matrix_b, matrix_size, calc_accuracy)
    else:
        print("Matrix A is not symmetric positive-definite or diagonally dominant.")
