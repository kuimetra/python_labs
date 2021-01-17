# У файлі задана дійсна матриця А розмірності m x n. Визначити кількість “особливих” елементів масиву А.
# Елемент вважається “особливим”, якщо він більший за суму решти елементів свого стовпця.

import numpy as np

with open('f1.txt', 'r') as file:
    mat = [[float(element) for element in line.split()] for line in file]

amount_of_special_elements = 0

for row in range(np.shape(mat)[0]):
    for column in range(np.shape(mat)[1]):
        if np.array(mat)[row][column] > np.array(mat).sum(axis=0)[column] - np.array(mat)[row][column]:
            amount_of_special_elements += 1

print('A =', np.array(mat))
if amount_of_special_elements:
    print(f'There is {amount_of_special_elements} special elements.')
else:
    print('Matrix A doesn\'t contain special elements.')
