# Створити клас, який репрезентує час на основі цілочислових хвилин та секунд. Відображення екземпляру класу на екран
# подати у форматі “Час: 05 хв. 30 с.” Реалізувати метод отримання часу в секундах. Перезавантажити оператор “-” так,
# щоб він правильнознаходив різницю часів.

class Time:
    def __init__(self, minutes, seconds):
        self._minutes = minutes
        self._seconds = seconds

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return self._seconds

    def __sub__(self, other):
        return abs((self._minutes * 60 + self._seconds) - (other._minutes * 60 + other._seconds))

    def __str__(self):
        return f'Time: {self.minutes} min. {self.seconds} sec.'


class EmptyFileError(Exception):
    pass


try:
    file_name = input('File name: ')
    if open(f'{file_name}.txt').read().isspace() or len(open(f'{file_name}.txt').read()) == 0:
        raise EmptyFileError

    list_of_time = []

    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            l = line.split(':')
            list_of_time.append(Time(int(l[0]), int(l[1])))

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def file_output():
        for time in list_of_time:
            print(time)


    def time_in_sec():
        for time in list_of_time:
            print(f'{time} in seconds --> {time.minutes * 60 + time.seconds}sec.')


    def time_difference():
        for i, time in enumerate(list_of_time):
            print(f'({i + 1}) {time}')
        first, second = map(int, input('Enter the sequence number of time you want to subtract: ').split())
        min = (list_of_time[first - 1] - list_of_time[second - 1]) // 60
        sec = list_of_time[first - 1] - list_of_time[second - 1] - min * 60
        print(f'{min} min. {sec} sec.')


    def menu():
        print('-' * 8 + 'Menu' + '-' * 8,
              '\n1 - show info\n2 - time in seconds\n3 - time difference\n0 - exit\n' + '-' * 20)
        while True:
            choices = {1: file_output, 2: time_in_sec, 3: time_difference}
            ch = int(input('\nOption: '))
            if ch == 0:
                break
            elif ch in range(1, 4):
                choices[ch]()
            else:
                print('No such option. Try again or exit.')


    menu()
