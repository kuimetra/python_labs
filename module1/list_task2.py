# Ввести  масив  цілих  чисел.
# Елементи  в  першій  половині  масиву  посортувати  за зростанням, а в другій –за спаданням.
print('Enter elements of the list:', end=' ')
l = [int(i) for i in input().split()]
sorted_l = sorted(l[:len(l) // 2]) + sorted(l[len(l) // 2:], reverse=True)
print(sorted_l)
