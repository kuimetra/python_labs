from math import sqrt
import numpy as np

customer_numbers = [
    [1, 2, 4, 7, 9, 11, 13, 14, 15, 16, 17, 19, 21, 25, 26, 27, 29, 31, 34, 36, 37, 38, 39, 40, 41, 42, 44, 47, 49],
    [3, 5, 6, 8, 10, 12, 15, 16, 17, 19, 20, 22, 23, 24, 26, 29, 30, 32, 33, 35, 43, 45, 46, 48, 50],
    [1, 5, 6, 7, 8, 10, 12, 13, 15, 17, 18, 22, 23, 24, 26, 29, 31, 37, 38, 40, 41, 44, 50],
    [1, 2, 4, 7, 8, 10, 13, 14, 15, 16, 17, 18, 19, 21, 25, 26, 27, 29, 31, 34, 36, 37, 38, 39, 40, 41, 42, 44, 47, 49],
    [2, 3, 4, 7, 8, 10, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23, 24, 28, 30, 32, 33, 36, 43, 44, 45, 46, 48, 49],
    [1, 5, 6, 7, 8, 10, 12, 14, 21, 22, 25, 26, 27, 29, 31, 34, 35, 37, 38, 39, 40, 41, 42, 47, 50],
    [1, 2, 4, 7, 9, 11, 13, 14, 15, 16, 17, 19, 21, 25, 27, 29, 31, 32, 34, 36, 37, 38, 39, 40, 41, 42, 44, 47, 49],
    [2, 3, 4, 7, 8, 10, 12, 13, 15, 16, 17, 18, 19, 21, 25, 28, 30, 32, 33, 36, 43, 44, 45, 46, 48, 49]
]

amount_of_customers, product_index = 50, 0
bool_array = [[1 if i in product else 0 for i in range(1, amount_of_customers + 1)] for product in customer_numbers]
euclidean_norm = [sqrt(sum(i * i for i in product)) for product in bool_array]
dot_product = [sum(np.array(bool_array[product_index]) & np.array(product)) for product in bool_array]
length_product = [euclidean_norm[product_index] * norm for norm in euclidean_norm]
similarity = np.array(dot_product) / np.array(length_product)
similarity_dict = {i + 1: similarity[i] for i in range(len(customer_numbers)) if i != product_index}
sorted_similarity_dict = {k: v for k, v in sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)}

print(f"product id: similarity with t{product_index + 1}")
for i, (k, v) in enumerate(sorted_similarity_dict.items()):
    print(f"t{k}: {v}")
    if i == 2:
        print("-" * 25)
