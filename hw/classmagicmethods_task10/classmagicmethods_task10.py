# Описати клас для визначення трапеції. Включити в нього методи для обчислення периметра та площі трапеції, перевірки,
# чи задана трапеція є рівнобічною. Перевантажити методи __eq__() і __ne__() для перевірки на рівність та нерівність двох
# трапецій, __gt__() і __lt__() для порівняння площ двох трапецій, __str__() для виведення інформації про об’єкт на екран.
# Використати його для розв’язування наступної задачі. Ввести послідовність трапецій. Обчислити периметр усіх трапецій.
# Впорядкувати послідовність в порядку зменшення периметрів. Визначити, які з трапецій є рівнобічними.

from math import *


class Trapezoid:
    def __init__(self, a, b, c, d, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.h = h

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d

    def __ne__(self, other):
        return self.a != other.a or self.b != other.b or self.c != other.c or self.d != other.d

    def __gt__(self, other):
        return self.area() > other.area()

    def __lt__(self, other):
        return self.area() < other.area()

    def __str__(self):
        return f'a = {self.a};\tb = {self.b};\tc = {self.c};\td = {self.d};\th = {self.h};'

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        return (self.a + self.c) / 2 * self.h

    def is_isosceles_trapezoid(self):
        return self.b == self.d and self.h == sqrt(self.b ** 2 - (self.c - self.a) ** 2 / 4)


class EmptyFileError(Exception):
    pass


try:
    f = input('File name: ')
    if open(f'{f}.txt').read().isspace() or len(open(f'{f}.txt').read()) == 0:
        raise EmptyFileError

    list_of_trapezoid = []
    skipped = 0
    with open(f'{f}.txt', 'r') as file:
        for line in file:
            sides = [float(i) for i in line.split()]
            if all(side > 0 for side in sides):
                list_of_trapezoid.append(Trapezoid(sides[0], sides[1], sides[2], sides[3], sides[4]))
            else:
                skipped += 1
    if skipped:
        print('!!!', skipped, 'trapezoids skipped from the file because of the negative value of the side !!!')

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)
else:
    print('1 - show info\n2 - equality of two trapezoids\n3 - calculate the perimeter\n4 - sort by perimeter'
          '\n5 - calculate the area\n6 - compare the areas of two trapezoids\n7 - isosceles trapezoids\n0 - exit')
    while True:
        option = int(input('\nOption: '))
        if option == 0:
            break

        elif option == 1:
            for i in range(len(list_of_trapezoid)):
                print(f'({i + 1}) {list_of_trapezoid[i]}')

        elif option == 2:
            first, second = map(int, input('Enter the sequence number of trapezoids you want to compare: ').split())
            if list_of_trapezoid[first - 1] == list_of_trapezoid[second - 1]:
                print('Trapezoids are equal.')
            elif list_of_trapezoid[first - 1] != list_of_trapezoid[second - 1]:
                print('Trapezoids are not equal.')

        elif option == 3:
            for trapezoid in list_of_trapezoid:
                print(f'{trapezoid}\tP = {trapezoid.perimeter()}.')

        elif option == 4:
            for trapezoid in sorted(list_of_trapezoid, key=lambda i: i.perimeter(), reverse=True):
                print(f'{trapezoid}\tP = {trapezoid.perimeter()}.')

        elif option == 5:
            for trapezoid in list_of_trapezoid:
                print(f'{trapezoid}\tS = {trapezoid.area()}.')

        elif option == 6:
            first, second = map(int, input('Enter the sequence number of trapezoids you want to compare: ').split())
            if list_of_trapezoid[first - 1] > list_of_trapezoid[second - 1]:
                print('Area of first trapezoid > area of second', end=' ')
            elif list_of_trapezoid[first - 1] < list_of_trapezoid[second - 1]:
                print('Area of first trapezoid < area of second', end=' ')
            else:
                print('Area of first trapezoid = area of second', end=' ')
            print(f'(S1 = {list_of_trapezoid[first - 1].area()}, S2 = {list_of_trapezoid[second - 1].area()})')

        elif option == 7:
            for trapezoid in list_of_trapezoid:
                if trapezoid.is_isosceles_trapezoid():
                    print(trapezoid)

        else:
            print('No such option. Try again or exit.')
