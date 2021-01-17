# Описати клас Student, який містить наступні поля: прізвище та ім'я, номер групи, успішність(масив із п’яти елементів)
# Написати програму, що виконує наступні дії: Ввід з файлу даних в масив, який складається із 5 екземплярів класу
# Student; Вивід на екран прізвищ і номерів груп студентів, якщо середній бал студента більший ніж 4.0, якщо таких
# студентів немає то вивести відповідне повідомлення.

import numpy as np


class Student:
    def __init__(self, name_surname, group, progress):
        self._name_surname = name_surname
        self._group = group
        self._progress = list(map(float, progress.split(' ')))

    @property
    def name_surname(self):
        return self._name_surname

    @property
    def group(self):
        return self._group

    @property
    def progress(self):
        return self._progress

    def __str__(self):
        return f'{self._name_surname} {self._group} {self._progress}'


class EmptyFileError(Exception):
    pass


try:
    file_name = input('File name: ')
    if open(f'{file_name}.txt').read().isspace() or len(open(f'{file_name}.txt').read()) == 0:
        raise EmptyFileError

    list_of_students = []

    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            l = line.split(',')
            list_of_students.append(Student(l[0], l[1], l[2]))

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def file_output():
        for student in list_of_students:
            print(student)


    def average_more_than4():
        amount_of_students = 0
        for student in list_of_students:
            if np.mean(student.progress) > 4:
                print(round(np.mean(student.progress), 2), '-', student)
                amount_of_students += 1
        if not amount_of_students:
            print('Students with an average score of more than 4 are absent.')


    def menu():
        print('-' * 10 + 'Menu' + '-' * 10,
              '\n1 - show info\n2 - average more than 4\n0 - exit\n' + '-' * 24)
        while True:
            choices = {1: file_output, 2: average_more_than4}
            ch = int(input('\nOption: '))
            if ch == 0:
                break
            elif ch in range(1, 3):
                choices[ch]()
            else:
                print('No such option. Try again or exit.')


    menu()
