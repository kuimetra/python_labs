# Клас “Відділ кадрів” (поле: назва ВУЗу у вигляді однієї стрічки). Написати програму, що моделює роботу системи обліку
# відділу кадрів. Потрібно створити такі сервіси: наповнення інформації з файлу про викладачів; визначення людей, у яких
# виповнилася кругла дата; визначення професорів пенсійного віку; визначення найстаршого і наймолодшого викладачів;
# долучення та вилучення нових працівників.

from datetime import date


class Teacher:
    def __init__(self, name_surname, date_of_birth, identification_number, sex, work_experience):
        self._name_surname = name_surname
        self._date_of_birth = date_of_birth
        self._identification_number = identification_number
        self._sex = sex.upper()
        self._work_experience = work_experience

    @property
    def name_surname(self):
        return self._name_surname

    @property
    def n_surname(self):
        return f'{self._name_surname.split()[0][0]}. {self._name_surname.split()[1]}'

    @property
    def date_of_birth(self):
        return self._date_of_birth.split('.')

    @property
    def identification_number(self):
        return self._identification_number

    @property
    def sex(self):
        return self._sex

    @property
    def work_experience(self):
        return self._work_experience

    def __str__(self):
        return f'{self._name_surname} {self._date_of_birth} ' \
               f'{self._identification_number} {self._sex} {self._work_experience}'


class AssociateProfessor(Teacher):
    def __init__(self, name_surname, date_of_birth, identification_number, sex, work_experience, rank):
        super().__init__(name_surname, date_of_birth, identification_number, sex, work_experience)
        self._rank = rank

    @property
    def rank(self):
        return self._rank

    def __str__(self):
        return f'{self._name_surname} {self._date_of_birth} {self._identification_number} ' \
               f'{self._sex} {self._work_experience} {self._rank}'


class FullProfessor(Teacher):
    def __init__(self, name_surname, date_of_birth, identification_number, sex, work_experience, additional_load):
        super().__init__(name_surname, date_of_birth, identification_number, sex, work_experience)
        self._additional_load = additional_load

    @property
    def additional_load(self):
        return self._additional_load

    def __str__(self):
        return f'{self._name_surname} {self._date_of_birth} {self._identification_number} ' \
               f'{self._sex} {self._work_experience} {self._additional_load}'


class EmptyFileError(Exception):
    pass


class HumanResources:
    def __init__(self, name_of_university=''):
        self._name_of_university = name_of_university
        self._human_resources = []

    def read_file(self, file_name):
        try:
            if open(f'{file_name}.txt').read().isspace() or len(open(f'{file_name}.txt').read()) == 0:
                raise EmptyFileError

            self._name_of_university = open(f'{file_name}.txt').readline()

            with open(f'{file_name}.txt', 'r') as file:
                for line in file:
                    flag = line.split()[0]
                    if flag == 'T':
                        f, n, sur, d_o_b, i_n, s, w_e = line.split()
                        self._human_resources.append(Teacher(' '.join([n, sur]), d_o_b, i_n, s, int(w_e)))
                    if flag == 'AP':
                        f, n, sur, d_o_b, i_n, s, w_e, r = line.split()
                        self._human_resources.append(AssociateProfessor(' '.join([n, sur]), d_o_b, i_n, s, int(w_e), r))
                    if flag == 'FP':
                        f, n, sur, d_o_b, i_n, s, w_e, a_l = line.split()
                        self._human_resources.append(
                            FullProfessor(' '.join([n, sur]), d_o_b, i_n, s, int(w_e), int(a_l)))
        except FileNotFoundError:
            print(r"File doesn't exist!")
            exit()
        except EmptyFileError:
            print('File is empty!')
            exit()
        except Exception as ex:
            print('Something else broke:', ex)
            exit()

    def final_info(self, file_name):
        with open(f'{file_name}.txt', 'w') as file:
            file.write(self._name_of_university)
            for person in self._human_resources:
                if isinstance(person, AssociateProfessor):
                    file.write(f'AP {person}\n')
                elif isinstance(person, FullProfessor):
                    file.write(f'FP {person}\n')
                elif isinstance(person, Teacher):
                    file.write(f'T {person}\n')

    def file_info(self):
        print('Name of the university:', self._name_of_university, end='')
        for person in self._human_resources:
            print(person)

    def info_sorting(self):
        print('Select the sorting criteria:\n1 - by name\n2 - surname\n3 - date of birth'
              '\n4 - identification number\n5 - work experience\n0 - exit')
        while True:
            sort_criteria = int(input('--> '))
            sorted_info = {1: sorted(self._human_resources, key=lambda a: a.name_surname.split()[0]),
                           2: sorted(self._human_resources, key=lambda a: a.name_surname.split()[1]),
                           3: sorted(self._human_resources,
                                     key=lambda a: (a.date_of_birth[2], a.date_of_birth[1], a.date_of_birth[0])),
                           4: sorted(self._human_resources, key=lambda a: a.identification_number),
                           5: sorted(self._human_resources, key=lambda a: a.work_experience)}
            if sort_criteria == 0:
                break
            elif sort_criteria in range(1, 6):
                for info in sorted_info[sort_criteria]:
                    print(info)
            else:
                print('No such option. Try again.')
                break

    def anniversary(self):
        for employee in self._human_resources:
            if age_calculation(employee.date_of_birth) % 10 == 0:
                print(employee.name_surname, age_calculation(employee.date_of_birth), 'y.o.')

    def fp_of_retirement_age(self):
        any_ret = False
        for employee_info in self._human_resources:
            if isinstance(employee_info, FullProfessor):
                age = age_calculation(employee_info.date_of_birth)
                if age > 58 and employee_info.sex == 'F' or age > 59 and employee_info.sex == 'M':
                    print(employee_info.name_surname, age, 'y.o.')
                    any_ret = True
        if not any_ret:
            print('There are no retirees among full professors.')

    def oldest_youngest(self):
        oldest = min(self._human_resources, key=lambda a: (a.date_of_birth[2], a.date_of_birth[1], a.date_of_birth[0]))
        youngest = max(self._human_resources,
                       key=lambda a: (a.date_of_birth[2], a.date_of_birth[1], a.date_of_birth[0]))
        print('The oldest:', ' '.join(str(oldest).split()[0:2]),
              '\nThe youngest:', ' '.join(str(youngest).split()[0:2]))

    def add_employee(self):
        try:
            marker = input(
                'Enter T - to add teacher\n      AP - associate professor\n      FP - full professor\n----> ').upper()
            if marker == 'T':
                t = input('Name / Surname / Date of birth / Identification number / Sex / Work experience\n').split()
                self._human_resources.append(Teacher(' '.join([t[0], t[1]]), t[2], t[3], t[4], int(t[5])))

            elif marker == 'AP':
                ap = input(
                    'Name / Surname / Date of birth / Identification number / Sex / Work experience / Rank\n').split()
                self._human_resources.append(
                    AssociateProfessor(' '.join([ap[0], ap[1]]), ap[2], ap[3], ap[4], int(ap[5]), ap[6]))

            elif marker == 'FP':
                fp = input('Name / Surname / Date of birth / Identification number / Sex / Work experience / '
                           'Additional load\n').split()
                self._human_resources.append(
                    FullProfessor(' '.join([fp[0], fp[1]]), fp[2], fp[3], fp[4], int(fp[5]), int(fp[6])))
            else:
                print('No such option. Try again.')
        except Exception as ex:
            print('Error!', ex)

    def del_employee(self):
        surname = input('Enter surname of employee you want to delete: ')
        ident_num = input('Enter identification number to confirm: ')
        for employee in self._human_resources:
            if employee.name_surname.split()[1] == surname and employee.identification_number == ident_num:
                self._human_resources.remove(employee)
                print('Destructor called, employee deleted.')


def age_calculation(date_of_birth):
    today = date.today()
    dd, mm, yyyy = date_of_birth
    age = today.year - int(yyyy) - ((today.month, today.day) < (int(mm), int(dd)))
    return age


def menu():
    file_name = input('File name: ')
    hr_obj = HumanResources()
    hr_obj.read_file(file_name)
    print('-' * 5 + 'Personnel Accounting System' + '-' * 5,
          '\n1 - show info\n2 - sorting\n3 - anniversaries\n4 - full professors of retirement age'
          '\n5 - the oldest and youngest teacher\n6 - add employee\n7 - remove employee\n0 - exit\n' + '-' * 37)
    while True:
        choices = {1: hr_obj.file_info, 2: hr_obj.info_sorting, 3: hr_obj.anniversary, 4: hr_obj.fp_of_retirement_age,
                   5: hr_obj.oldest_youngest, 6: hr_obj.add_employee, 7: hr_obj.del_employee}
        ch = int(input('\nOption: '))
        if ch == 0:
            hr_obj.final_info(file_name)
            break
        elif ch in range(1, 8):
            choices[ch]()
        else:
            print('No such option. Try again or exit.')


menu()
