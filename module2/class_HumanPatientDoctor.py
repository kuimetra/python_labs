# На основі базового класу “людина” (прізвище,  вік) побудувати похідні класи “пацієнт” (хвороба) і “лікар”
# (спеціальність). Дані вводити з файлу. Перевантажити необхідні для реалізації програми методи. Скористатись ними для
# створення єдиного списку пацієнтів і лікарів. Вивести на екран: 1)посортований список за прізвищем; 2)знайти найстаршу
# людину у цьому списку; 3)список пацієнтів, які хворіють заданою хворобою; 4)лікарів-хірургів, старших за 40 років.
class Human:
    def __init__(self, surname, age):
        self._surname = surname
        self._age = age

    @property
    def surname(self):
        return self._surname

    @property
    def age(self):
        return self._age

    def __gt__(self, other):
        return self._age > other._age

    def __str__(self):
        return f'{self._surname} {self._age}'


class Patient(Human):
    def __init__(self, surname, age, illness):
        super().__init__(surname, age)
        self._illness = illness

    @property
    def illness(self):
        return self._illness

    def __str__(self):
        return f'{self._surname} {self._age} {self._illness}'


class Doctor(Human):
    def __init__(self, surname, age, specialty):
        super().__init__(surname, age)
        self._specialty = specialty

    @property
    def specialty(self):
        return self._specialty

    def __str__(self):
        return f'{self._surname} {self._age} {self._specialty}'


class EmptyFileError(Exception):
    pass


try:
    file_name = input('File name: ')
    if open(f'{file_name}.txt').read().isspace() or len(open(f'{file_name}.txt').read()) == 0:
        raise EmptyFileError

    list_of_patients_and_doctors = []

    with open(f'{file_name}.txt', 'r') as file:
        for line in file:
            if line.split()[0].upper() == 'P':
                p = line.split()
                list_of_patients_and_doctors.append(Patient(p[1], int(p[2]), p[3]))
            elif line.split()[0].upper() == 'D':
                d = line.split()
                list_of_patients_and_doctors.append(Doctor(d[1], int(d[2]), d[3]))
            else:
                h = line.split()
                list_of_patients_and_doctors.append(Human(h[1], int(h[2])))

except FileNotFoundError:
    print(r"File doesn't exist!")
except EmptyFileError:
    print('File is empty!')
except Exception as ex:
    print('Something else broke:', ex)

else:
    def file_output():
        for person in list_of_patients_and_doctors:
            print(person)


    def sort_by_surname():
        for person in sorted(list_of_patients_and_doctors, key=lambda a: a.surname):
            print(person)


    def oldest_person():
        # oldest = max(list_of_patients_and_doctors, key=lambda a: a.age)
        # print(oldest.surname, 'is', oldest.age, 'y.o.')

        oldest = list_of_patients_and_doctors[0]
        for person in list_of_patients_and_doctors:
            if person > oldest:
                oldest = person
        print(oldest.surname, 'is', oldest.age, 'y.o.')


    def search_by_illness():
        amount_of_person_with_illness = 0
        input_illness = input('Enter the name of the illness: ')
        for person in list_of_patients_and_doctors:
            if isinstance(person, Patient):
                if person.illness == input_illness:
                    print(person.surname)
                    amount_of_person_with_illness += 1
        if not amount_of_person_with_illness:
            print('Illness was not found among patients.')


    def surgeons_40plus():
        amount_of_surgeons_40plus = 0
        for person in list_of_patients_and_doctors:
            if isinstance(person, Doctor):
                if person.specialty == 'surgeon' and person.age > 40:
                    print(person.surname, 'is', person.age, 'y.o.')
                    amount_of_surgeons_40plus += 1
        if not amount_of_surgeons_40plus:
            print('There are no surgeons over 40 years old.')


    def menu():
        print('-' * 15 + 'Menu' + '-' * 15,
              '\n1 - show info\n2 - sort by surname\n3 - the oldest person\n4 - search patients by illness'
              '\n5 - surgeons over 40 years of age\n0 - exit\n' + '-' * 34)
        while True:
            choices = {1: file_output, 2: sort_by_surname, 3: oldest_person, 4: search_by_illness, 5: surgeons_40plus}
            ch = int(input('\nOption: '))
            if ch == 0:
                break
            elif ch in range(1, 6):
                choices[ch]()
            else:
                print('No such option. Try again or exit.')


    menu()
