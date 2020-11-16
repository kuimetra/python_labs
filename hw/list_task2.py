# Задано масив цілих чисел. Обчислити кількість елементів масиву,
# які задовольняють умову a[k] < (a[k - 1] + a[k + 1]) / 2, і вивести їх на екран
import random

f = int(input('''Enter
1 - to generate a list of random numbers
2 - to create your list
'''))

if f == 1:
    n = int(input('Amount of elements: '))
    a = []
    for i in range(n):
        el = random.randint(1, 100)
        a.append(el)
    print('List:', a)

elif f == 2:
    print('Enter elements of the list:', end=' ')
    a = [int(k) for k in input().split()]
    n = len(a)
    print('List:', a)

if f == 1 or f == 2:
    c = 0
    print('\na[k]  a[k-1]  a[k+1]')
    for k in range(1, n - 1):
        if a[k] < (a[k - 1] + a[k + 1]) / 2:
            print(f'{a[k]}\t\t{a[k - 1]}\t\t{a[k + 1]}')
            c += 1
    print(f'{c}/{n} array elements satisfy the inequality')
