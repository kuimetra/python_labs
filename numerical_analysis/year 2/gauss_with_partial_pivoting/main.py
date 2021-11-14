import numpy as np


def get_matrix():
    mat = []
    with open("data.txt", "r") as file:
        for line in file:
            mat.append([float(el) for el in line.split()])
    return mat


def is_singular(matrix):
    return np.any(np.diag(matrix) == 0)


def row_interchange(matrix, current_row, p):
    index_of_max_row = current_row + np.argmax(np.abs(matrix[current_row:, current_row]))
    if current_row != index_of_max_row:
        matrix[[current_row, index_of_max_row]] = matrix[[index_of_max_row, current_row]]
        p *= -1


def gauss(matrix):
    np.set_printoptions(suppress=True)
    file_with_results = open("results.txt", "a+")
    file_with_results.write("Given system: " + str(matrix) + "\n")
    row_size = matrix.shape[0]
    p = 1
    for fixed_row in range(row_size - 1):
        row_interchange(matrix, fixed_row, p)
        for row in range(fixed_row + 1, row_size):
            coefficient = matrix[row, fixed_row] / matrix[fixed_row, fixed_row]
            matrix[row, :] -= matrix[fixed_row, :] * coefficient

    file_with_results.write(f"A = {matrix[:, :matrix.shape[0]].round(3)}\n")
    file_with_results.write(f"b = {matrix[:, matrix.shape[0]:].round(3)}\n")

    if is_singular(matrix):
        file_with_results.write("There is no single solution.\n" + "-" * 50 + "\n")
        return

    x = np.mat([0.0 for _ in range(row_size)]).transpose()
    for k in range(row_size - 1, -1, -1):
        x[k, 0] = (matrix[k, -1] - matrix[k, k + 1:row_size] * x[k + 1:row_size, 0]) / matrix[k, k]

    file_with_results.write(f"x = {x.round(3)}\n")
    diag_prod = matrix[:, :matrix.shape[0]].diagonal().prod()
    file_with_results.write(f"detA = {round(p * diag_prod, 3)}\n" + "-" * 50 + "\n")


gauss(np.mat(get_matrix()))
