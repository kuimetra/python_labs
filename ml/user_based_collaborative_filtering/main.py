import numpy as np
import math

product_rating = [
    [0.5, None, None, 2, 1, 2.5, 3, 3, 3, 4.5],
    [4, 3.5, 1, None, 1, 2.5, None, 2, 1, 2.5],
    [0.5, 2.75, 4, 2, 0.5, 2.75, 3.5, None, 2, None],
    [1, 4, 2, 4, None, 1, 4.5, 2.5, None, 2.5],
    [1.5, 4, 1, None, 2, 1, None, 4.5, 2.5, 1],
    [2, None, 0.5, 2.5, None, 1, 1.5, 0.5, 1, 1],
    [None, 3, 4.5, 2.5, 1, None, 3, 4, 2.5, 5],
    [2, 3.5, None, 4, 1.5, 1, 4.5, 3.5, 3, None],
    [None, 3.5, 1.5, 3.5, 2, 3, 2, 1, 2, None],
    [1, None, 1.5, None, 1, 1.5, 4.5, 2, 2.5, 1]
]
user_index = 0
amount_of_items = 10


def get_none_indexes(list):
    return [i for i, v in enumerate(list) if v is None]


def get_not_none_indexes(list):
    return [i for i, v in enumerate(list) if v is not None]


def sim(a, b):
    n = len(a)
    mean_a, mean_b = np.mean(a), np.mean(b)
    numerator = sum(np.array(a) * np.array(b)) - n * mean_a * mean_b
    denominator = math.sqrt(sum(np.power(a, 2)) - n * mean_a ** 2) * math.sqrt(sum(np.power(b, 2)) - n * mean_b ** 2)
    return numerator / denominator


user_none_indexes = get_none_indexes(product_rating[user_index])

correlation_coefficients = {}
for i, user in enumerate(product_rating):
    if i == user_index:
        continue
    none_indexes = list(set(get_none_indexes(user) + user_none_indexes))
    x = [product_rating[i][ind] for ind in range(amount_of_items) if ind not in none_indexes]
    y = [product_rating[user_index][ind] for ind in range(amount_of_items) if ind not in none_indexes]
    correlation_coefficients[i] = sim(x, y)

most_similar_users = {k: v for (k, v) in correlation_coefficients.items() if v >= 0.5}
most_similar_users_keys = [*most_similar_users.keys()]
most_similar_users_values = np.array([*most_similar_users.values()])

result = {}
for user_none_i in user_none_indexes:
    user_rating = np.array(product_rating)[most_similar_users_keys, user_none_i]
    not_none_indexes = get_not_none_indexes(user_rating)
    k = 1 / sum(most_similar_users_values[not_none_indexes])
    result[user_none_i + 1] = \
        round(k * sum(user_rating[not_none_indexes] * most_similar_users_values[not_none_indexes]), 1)
print(result)
