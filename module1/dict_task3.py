# Ввести інформацію  про  результати  іспиту n студентів
# (прізвище  і  оцінка  у  100-бальній системі, наприклад, Васьків,76)
# і записати у словник. Замінити оцінку у 100-бальній  системі для кожного  студента
# відповідною оцінкою у  5-ти  бальній. Вивести прізвища тих, хто одержав 4 або 5 за іспит.
n = int(input('Number of students: '))
d = {}


def input_dict():
    for _ in range(n):
        surname, mark = input().split()
        d[surname] = int(mark)


def _100to5():
    for k, v in d.items():
        if 90 <= v <= 100:
            d[k] = 5
        elif 75 <= v <= 89:
            d[k] = 4
        elif 51 <= v <= 74:
            d[k] = 3
        else:
            d[k] = 2


def print_5or4():
    v = ', '.join([k for k, v in d.items() if v == 4 or v == 5])
    if v:
        print('Surnames of those who received 4 or 5 for the exam:', v)
    else:
        print('There are no students who received 4 or 5 for the exam.')


input_dict()
_100to5()
print_5or4()
