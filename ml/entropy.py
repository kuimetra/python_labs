from tabulate import tabulate
import numpy as np
import math

slot = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1]
n = len(slot)
table = []
i_list = []
j = 1
for s in range(1, n):
    l, r = slot[:s], slot[s:]
    w_l, b_l, w_r, b_r = l.count(1), l.count(0), r.count(1), r.count(0)
    p1_l, p2_l, p1_r, p2_r = w_l / (w_l + b_l), b_l / (w_l + b_l), w_r / (w_r + b_r), b_r / (w_r + b_r)
    i_l = (-p1_l * math.log2(p1_l) if p1_l else 0) - (p2_l * math.log2(p2_l) if p2_l else 0)
    i_r = (-p1_r * math.log2(p1_r) if p1_r else 0) - (p2_r * math.log2(p2_r) if p2_r else 0)
    i = (w_l + b_l) / n * i_l + (w_r + b_r) / n * i_r
    i_list.append(i)
    table.append([*map(lambda x: round(x, ndigits=3), [j, w_l, b_l, i_l, w_r, b_r, i_r, i])])
    j += 1

print(tabulate(table, headers=["x", "n_l", "m_l", "I_l", "n_r", "m_r", "I_r", "I_x"]))
print("Min index =", np.argmin(i_list) + 1)
