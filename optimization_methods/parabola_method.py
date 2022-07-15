from tabulate import tabulate


def f(x):
    return (x + 3) ** 2


a, b = map(float, input("Enter a, b: ").split())
c = float(input("Enter c: "))
eps = 0.2
table = []
delta_minus, delta_plus = f(a) - f(c), f(b) - f(c)

if delta_minus < 0 or delta_plus < 0 or delta_minus + delta_plus <= 0:
    print("Invalid point c")
    exit()

k = 1
while abs(a - b) > eps:
    delta_minus, delta_plus = f(a) - f(c), f(b) - f(c)
    s = c + (1 / 2) * (((b - c) ** 2 * delta_minus - (c - a) ** 2 * delta_plus) /
                       ((b - c) * delta_minus + (c - a) * delta_plus))

    t = s if s != c else (c + a) / 2

    table.append([*map(lambda val: round(val, ndigits=5),
                       [k, a, b, c, f(a), f(b), f(c), delta_minus, delta_plus, s, t, f(t), abs(b - a)])])
    k += 1
    if f(c) < f(t):
        a = t
    else:
        b = c

print(tabulate(table,
               headers=["k", "a", "b", "c", "f(a)", "f(b)", "f(c)", "delta-", "delta+", "s", "t", "f(t)", "|a - b|"]))
