# Змінити завдання 5 наступним чином: всі дії оформити з використанням функцій;
# наповнення словника вводити з файлу; додати обробку винятку при відкритті файлу
class EmptyFileError(Exception):
    pass


try:
    f = input('File name: ')
    if open(f'{f}.txt').read().isspace() or len(open(f'{f}.txt').read()) == 0:
        raise EmptyFileError

    d = {}
    with open(f'{f}.txt', 'r') as file:
        for line in file:
            surname, sex, age, conscript = line.split()
            d[surname] = [sex, int(age), int(conscript)]

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def surnames():
        c_s = ', '.join([k for k, v in d.items() if bool(v[2]) is True])
        if c_s:
            print('Surnames of all conscripts:', c_s)
        else:
            print('There are no conscripts among employees.')
            exit()


    def oldest():
        m_c = {k: v for k, v in d.items() if v[0] == 'M' and bool(v[2]) is True}
        if m_c:
            o_c = max(m_c.items(), key=lambda a: a[1][1])
            print('The oldest man among conscripts -', o_c[0])
        else:
            print('There are no males among conscripts.')


    surnames()
    oldest()
