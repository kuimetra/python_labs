# Дано послідовність слів, відокремлених пропусками. Утворити нову стрічку зі слів,
# які починаються і закінчуються однією і тією ж буквою. Знайти найдовше слово
# утвореної стрічки.
s1 = input('Enter word sequence: ').split()
s2 = ' '.join([word for word in s1 if word[0] == word[len(word) - 1]])
print('Words which begins&ends with the same letter:', s2)
print('Word with the longest length:', max(s2.split(), key=len))
