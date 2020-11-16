# Задано натуральне n і дійсне x. Обчислити: S = sinx + sin(sinx) + ... + sin(sin(..(sinx)))
import math

n = int(input('Enter n: '))
x = float(input('Enter x: '))
S = 0
for i in range(n):
    S += math.sin(x)
    x = math.sin(x)
print(f'S = {round(S, 3)}')
