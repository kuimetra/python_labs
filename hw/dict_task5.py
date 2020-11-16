# Відомі дані про працівників фірми (прізвище, стать, вік і відношення до військової служби).
# Надрукувати прізвища всіх військовозобов’язаних працівників.
# Визначити прізвище найстаршого чоловіка серед військовозобов’язаних
n = int(input('Number of employees in the company: '))
d = {}


def input_dict():
    for _ in range(n):
        surname, sex, age, conscript = input().split()
        d[surname] = [sex, int(age), int(conscript)]


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


input_dict()
surnames()
oldest()
