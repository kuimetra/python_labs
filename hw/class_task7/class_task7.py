# Клас “Викладач”. Поля: прізвище та ім’я, дата народження, ідентифікаційний номер, стать, стаж роботи.
# Методи: визначення категорії стажу (1 – стаж роботи до 3 років, 2 – 3-10 років, 3 – 10-20 років, 4 – більше 20 років),
# обчислення заробітної плати за визначеним початковим окладом, визначення чи викладач досяг пенсійного віку.
from datetime import date


class Teacher:
    def __init__(self, name_surname, date_of_birth, identification_number, sex, work_experience):
        self.__name_surname = name_surname
        self.__date_of_birth = date_of_birth
        self.__identification_number = identification_number
        self.__sex = sex
        self.__work_experience = work_experience

    @property
    def name_surname(self):
        return self.__name_surname.split()

    @property
    def n_surname(self):
        return f'{self.__name_surname.split()[0][0]}. {self.__name_surname.split()[1]}'

    @property
    def date_of_birth(self):
        return self.__date_of_birth.split('.')

    @property
    def identification_number(self):
        return self.__identification_number

    @property
    def sex(self):
        return self.__sex

    @property
    def work_experience(self):
        return self.__work_experience

    def __str__(self):
        return f'{self.__name_surname} {self.__date_of_birth} ' \
               f'{self.__identification_number} {self.__sex} {self.__work_experience}'


class EmptyFileError(Exception):
    pass


try:
    f = input('File name: ')
    if open(f'{f}.txt').read().isspace() or len(open(f'{f}.txt').read()) == 0:
        raise EmptyFileError

    list_of_teachers = []

    with open(f'{f}.txt', 'r') as file:
        for line in file:
            n, sur, d_o_b, i_n, s, w_e = line.split()
            list_of_teachers.append(Teacher(' '.join([n, sur]), d_o_b, i_n, s, int(w_e)))

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def file_output():
        for teacher in list_of_teachers:
            print(teacher)


    def category_of_experience(years_of_exp):
        if years_of_exp < 3:
            return 1
        elif years_of_exp < 10:
            return 2
        elif years_of_exp < 20:
            return 3
        else:
            return 4


    def category_of_experience_output():
        for teacher in list_of_teachers:
            print(teacher.n_surname, category_of_experience(teacher.work_experience))


    def salary():
        starting_salary = float(input('Enter starting salary: '))
        for teacher in list_of_teachers:
            teacher_salary = starting_salary
            salaries = {1: teacher_salary, 2: teacher_salary * 1.1, 3: teacher_salary * 1.2, 4: teacher_salary * 1.3}
            print(teacher.identification_number, teacher.n_surname,
                  f'${round(salaries[category_of_experience(teacher.work_experience)], 2)}')


    def retirement_age():
        any_ret = False
        for teacher in list_of_teachers:
            today = date.today()
            dd, mm, yyyy = teacher.date_of_birth
            age = today.year - int(yyyy) - ((today.month, today.day) < (int(mm), int(dd)))
            if age > 58 and teacher.sex == 'F' or age > 59 and teacher.sex == 'M':
                print(' '.join(teacher.name_surname), age, 'y.o.')
                any_ret = True
        if not any_ret:
            print('There are no retirees among teachers.')


    def menu():
        print('-' * 11 + 'Menu' + '-' * 11,
              '\n1 - show info\n2 - category of experience\n3 - salaries\n4 - list of retirees\n0 - exit\n' + '-' * 26)
        while True:
            choices = {1: file_output, 2: category_of_experience_output, 3: salary, 4: retirement_age}
            ch = int(input('\nOption: '))
            if ch == 0:
                break
            elif 0 < ch < 5:
                choices[ch]()
            else:
                print('No such option. Try again or exit.')


    menu()
