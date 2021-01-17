# Дано послідовність чисел, які містять лише цифри 1 , 5 і 9, у порядку зростання: 1 5 9 11 15 19 51 55 59 і т. д.
# Вивести на екран N перших членів цієї послідовності.

N = int(input('N = '))
if N > 0:
    list_of_numbers = [1]
    num, n = 1, 1
    while n != N:
        num += 1
        for i in str(num):
            if int(i) not in [1, 5, 9]:
                break
        else:
            list_of_numbers.append(num)
            n += 1
    print(f'First {N} numbers with 1, 5, 9 digits: ', end='')
    print(*list_of_numbers, sep=', ', end='.')
else:
    print('The value of N cannot be negative or equal to zero.')
