# Задано дійсну квадратну матрицю. Знайти найбільший елемент серед мінімальних
# елементів тих рядків, в яких є від’ємний елемент на головній діагоналі
s = int(input('Matrix size: '))
print(f'Enter {s}*{s} matrix:')

mat, m = [], []

for i in range(s):
    mat.append([int(j) for j in input().split()])

print('\nRows with negative element on the main diagonal:')
for i in range(s):
    if mat[i][i] < 0:
        row_elements = [mat[i][j] for j in range(s)]
        print(f'{i + 1}: {row_elements}')
        m.append(min(row_elements))

if m:
    print(f'''Min elements of these rows {m}
Max element = {max(m)}''')
