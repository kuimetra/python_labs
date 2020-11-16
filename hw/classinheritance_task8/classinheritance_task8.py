# Похідні класи “Доцент” (поле: звання) та “Професор” (поле: наявність додаткового навантаження).
# Перевизначити метод обчислення заробітної плати для обох класів з урахуванням надбавки за стаж і звання
# (для доцента – 20 %, для професора – 30 %). Для доцента описати метод, який визначає,
# чи виповнилося людині 50, 60 або 70 років.
from datetime import date


class Teacher:
    def __init__(self, name_surname, date_of_birth, identification_number, sex, work_experience):
        self._name_surname = name_surname
        self._date_of_birth = date_of_birth
        self._identification_number = identification_number
        self._sex = sex
        self._work_experience = work_experience

    @property
    def name_surname(self):
        return self._name_surname.split()

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
        self._rank = rank.replace('_', ' ')

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


try:
    file_name = input('File name: ')
    if open(f'{file_name}.txt').read().isspace() or len(open(f'{file_name}.txt').read()) == 0:
        raise EmptyFileError

    list_of_uni_employees = []

    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            flag = line.split()[0]
            if flag == 'T':
                f, n, sur, d_o_b, i_n, s, w_e = line.split()
                list_of_uni_employees.append(Teacher(' '.join([n, sur]), d_o_b, i_n, s, int(w_e)))
            if flag == 'AP':
                f, n, sur, d_o_b, i_n, s, w_e, r = line.split()
                list_of_uni_employees.append(AssociateProfessor(' '.join([n, sur]), d_o_b, i_n, s, int(w_e), r))
            if flag == 'FP':
                f, n, sur, d_o_b, i_n, s, w_e, a_l = line.split()
                list_of_uni_employees.append(FullProfessor(' '.join([n, sur]), d_o_b, i_n, s, int(w_e), int(a_l)))

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def file_output():
        for uni_employee in list_of_uni_employees:
            print(uni_employee)


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
        for uni_employee in list_of_uni_employees:
            print(uni_employee.n_surname, category_of_experience(uni_employee.work_experience))


    def salary_calculation():
        starting_salary = float(input('Enter starting salary: '))
        for uni_employee in list_of_uni_employees:
            uni_employee_salary = starting_salary
            salaries = {1: uni_employee_salary, 2: uni_employee_salary * 1.05,
                        3: uni_employee_salary * 1.1, 4: uni_employee_salary * 1.15}
            salary = salaries[category_of_experience(uni_employee.work_experience)]

            if isinstance(uni_employee, AssociateProfessor):
                salary += starting_salary * 0.2

            if isinstance(uni_employee, FullProfessor):
                salary += starting_salary * 0.3

            print(uni_employee.identification_number, uni_employee.n_surname, f'${salary}')


    def age_calculation(date_of_birth):
        today = date.today()
        dd, mm, yyyy = date_of_birth
        age = today.year - int(yyyy) - ((today.month, today.day) < (int(mm), int(dd)))
        return age


    def retirement_age():
        any_ret = False
        for uni_employee in list_of_uni_employees:
            age = age_calculation(uni_employee.date_of_birth)
            if age > 58 and uni_employee.sex == 'F' or age > 59 and uni_employee.sex == 'M':
                print(' '.join(uni_employee.name_surname), age, 'y.o.')
                any_ret = True
        if not any_ret:
            print('There are no retirees among teachers.')


    def ap_50or60or70():
        any_ap = False
        for uni_employee in list_of_uni_employees:
            if isinstance(uni_employee, AssociateProfessor):
                age = age_calculation(uni_employee.date_of_birth)
                if age > 69:
                    print(uni_employee.n_surname, 'turned 70 y.o.')
                    any_ap = True
                elif age > 59:
                    print(uni_employee.n_surname, 'turned 60 y.o.')
                    any_ap = True
                elif age > 49:
                    print(uni_employee.n_surname, 'turned 50 y.o.')
                    any_ap = True
        if not any_ap:
            print('There are no such associate professors.')


    def menu():
        print('-' * 12 + 'Menu' + '-' * 12,
              '\n1 - show info\n2 - category of experience\n3 - salaries\n4 - list of retirees'
              '\n5 - associate professors who\n    turned 50, 60 or 70 y.o\n0 - exit\n' + '-' * 28)
        while True:
            choices = {1: file_output, 2: category_of_experience_output,
                       3: salary_calculation, 4: retirement_age, 5: ap_50or60or70}
            ch = int(input('\nOption: '))
            if ch == 0:
                break
            elif 0 < ch < 6:
                choices[ch]()
            else:
                print('No such option. Try again or exit.')


    menu()
