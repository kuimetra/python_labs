from tkinter import filedialog, messagebox
from math import sqrt
from tkinter import *
import pandas as pd
import numpy as np
import random


def translate(text, alphabet, indexes):
    new_text, i = '', 0
    for ch in text:
        j = random.choice([0, 1])
        if not ch.isalpha():
            new_text += ch
        elif ch.isupper():
            letter = alphabet[int(indexes[i][1]), int(indexes[i][0])]
            if len(letter) == 2:
                new_text += letter[j]
            else:
                new_text += letter
            i += 1
        elif ch.islower():
            letter = alphabet[int(indexes[i][1]), int(indexes[i][0])].lower()
            if len(letter) == 2:
                new_text += letter[j]
            else:
                new_text += letter
            i += 1
    return new_text


def get_index(array, item):
    for ind, val in np.ndenumerate(array):
        if item in val:
            return ind[::-1]


def text_encryptor():
    def open_file():
        path = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*.txt"),))
        if path:
            with open(path, "r", encoding="utf-8-sig") as file:
                text = file.read().strip("\n ")
            input_scope.delete("1.0", END)
            input_scope.insert(END, text)

    def save_file():
        path = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*.txt"),),
                                            defaultextension=(("Text Files", "*.txt"),))
        if path:
            with open(path, "w+", encoding="utf-8-sig") as file:
                try:
                    file.write(','.join(shuffled_alphabet.flatten()) + '\n')
                    file.write(encrypted_text)
                except NameError:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def encrypt():
        global encrypted_text, shuffled_alphabet, size
        output_scope.delete("1.0", END)
        matrix_scope.delete("1.0", END)
        step1_scope.delete("1.0", END)
        step2_scope.delete("1.0", END)
        text = input_scope.get("1.0", END).strip("\n ")
        if text.isspace() or len(text) == 0:
            messagebox.showinfo("Info", "Insert some text please.")
        else:
            alphabet_exist = False
            if language.get() == "ENG":
                alphabet, size, alphabet_exist = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                                           'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                                           'QZ']), (5, 5), True
            elif language.get() == "UKR":
                alphabet, size, alphabet_exist = np.array(['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І',
                                                           'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
                                                           'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']), (6, 6), True
                add_3 = np.random.choice(alphabet, 3, replace=False)
                alphabet = np.append(alphabet, add_3)

            if alphabet_exist:
                if language.get() == "ENG" and any(letter not in ''.join(alphabet) for letter in text.upper()
                                                   if letter.isalpha()):
                    messagebox.showerror("Error", "The text should contain only English letters.")
                elif language.get() == "UKR" and any(letter not in ''.join(alphabet) for letter in text.upper()
                                                     if letter.isalpha()):
                    messagebox.showerror("Error", "The text should contain only Ukrainian letters.")
                else:
                    np.random.shuffle(alphabet)
                    shuffled_alphabet = alphabet.reshape(size)
                    text_indexes = ''
                    for letter in text.upper():
                        if letter in ''.join(shuffled_alphabet.flatten()):
                            text_indexes += ''.join(map(str, get_index(shuffled_alphabet, letter)))
                    row_wise_indexes = text_indexes[::2] + text_indexes[1::2]
                    text_indexes = tuple(text_indexes[i:i + 2] for i in range(0, len(text_indexes), 2))
                    ciphered_indexes = tuple(row_wise_indexes[i:i + 2] for i in range(0, len(row_wise_indexes), 2))

                    encrypted_text = translate(text, shuffled_alphabet, ciphered_indexes)

                    matrix_scope.insert(END, pd.DataFrame(shuffled_alphabet))
                    step1_scope.insert(END, ', '.join(map(str, text_indexes)) + '.')
                    step2_scope.insert(END, ', '.join(map(str, ciphered_indexes)) + '.')
                    output_scope.insert(END, encrypted_text)

    e_window = Toplevel(window)
    e_window.geometry("640x480")
    e_window.title("Text encryptor")

    Button(e_window, text="Browse file", font=("Century Gothic", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=open_file).place(x=25, y=-5, height=24, width=80)
    Button(e_window, text="Save file", font=("Century Gothic", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=save_file).place(x=105, y=-5, height=24, width=65)

    language = StringVar(value="ENG")
    Radiobutton(e_window, text="ENG", var=language, value="ENG", font=("Century Gothic", 8), fg="#775D8E").place(x=245,
                                                                                                                 y=16)
    Radiobutton(e_window, text="UKR", var=language, value="UKR", font=("Century Gothic", 8), fg="#775D8E").place(x=295,
                                                                                                                 y=16)

    input_scope = Text(e_window, bg="#F8F8F8", fg="#709fb0", selectbackground="#709fb0", padx=6, pady=2,
                       font=("Ubuntu Mono", 11))
    matrix_scope = Text(e_window, bg="#F8F8F8", fg="#99b898", selectbackground="#99b898", relief="groove", padx=12,
                        pady=2, font=("Ubuntu Mono", 11))
    step1_scope = Text(e_window, bg="#F8F8F8", fg="#99b898", selectbackground="#99b898", relief="groove", padx=5,
                       font=("Ubuntu Mono", 11))
    step2_scope = Text(e_window, bg="#F8F8F8", fg="#99b898", selectbackground="#99b898", relief="groove", padx=5,
                       font=("Ubuntu Mono", 11))
    output_scope = Text(e_window, bg="#F8F8F8", fg="#709fb0", selectbackground="#709fb0", padx=6, pady=2,
                        font=("Ubuntu Mono", 11))

    Button(e_window, text="ENCRYPT", font=("Century Gothic", 10, "bold"), bg="#F0F0F0", fg="#726a95", borderwidth=2,
           relief="groove", command=encrypt).place(x=356, y=16, height=25, width=70)

    Label(e_window, text="Given text", font=("Century Gothic", 10), fg="#414141").place(x=25, y=27)
    Label(e_window, text="Encrypted text", font=("Century Gothic", 10), fg="#414141").place(x=25, y=242)
    Label(e_window, text="Alphabet matrix", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441, y=28)
    Label(e_window, text="Text indexes", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441, y=171)
    Label(e_window, text="Encrypted text indexes", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441,
                                                                                                              y=315)

    input_scope.place(x=25, y=50, height=190, width=401)
    output_scope.place(x=25, y=265, height=190, width=401)
    matrix_scope.place(x=441, y=50, height=118, width=174)
    step1_scope.place(x=441, y=193, height=118, width=174)
    step2_scope.place(x=441, y=337, height=118, width=174)


def text_decryptor():
    def open_file():
        global encrypted_file
        path = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*.txt"),))
        if path:
            with open(path, "r", encoding="utf-8-sig") as file:
                encrypted_file = file.read().strip("\n ")
            encrypted_scope.delete("1.0", END)
            encrypted_scope.insert(END, '\n'.join(encrypted_file.split('\n')[1:]))

    def save_file():
        path = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*.txt"),),
                                            defaultextension=(("Text Files", "*.txt"),))
        if path:
            with open(path, "w+", encoding="utf-8-sig") as file:
                file.write('\n'.join(encrypted_file.split('\n')[1:]) + '\n\n')
                decrypted_text = decrypted_scope.get("1.0", END).strip("\n ")
                file.write(decrypted_text)
                if decrypted_text.isspace() or len(decrypted_text) == 0:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def decrypt():
        encrypted_scope.delete("1.0", END)
        decrypted_scope.delete("1.0", END)
        matrix_scope.delete("1.0", END)
        step1_scope.delete("1.0", END)
        step2_scope.delete("1.0", END)
        try:
            if encrypted_file.isspace() or len(encrypted_file) == 0:
                messagebox.showinfo("Info", "Empty file.")
            else:
                alphabet = np.array(encrypted_file.split('\n')[0].split(','))
                matrix_alphabet = np.reshape(alphabet, (int(sqrt(len(alphabet))), -1))
                encrypted_text = '\n'.join(encrypted_file.split('\n')[1:])

                encrypted_indexes = ''
                for letter in encrypted_text.upper():
                    if letter in ''.join(matrix_alphabet.flatten()):
                        encrypted_indexes += ''.join(map(str, get_index(matrix_alphabet, letter)))

                key_indexes = tuple(i + j for i, j in zip(encrypted_indexes[:len(encrypted_indexes) // 2],
                                                          encrypted_indexes[len(encrypted_indexes) // 2:]))
                encrypted_indexes = tuple(encrypted_indexes[i:i + 2] for i in range(0, len(encrypted_indexes), 2))
                decrypted_text = translate(encrypted_text, matrix_alphabet, key_indexes)

                encrypted_scope.insert(END, encrypted_text)
                matrix_scope.insert(END, pd.DataFrame(matrix_alphabet))
                step1_scope.insert(END, ', '.join(map(str, encrypted_indexes)) + '.')
                step2_scope.insert(END, ', '.join(map(str, key_indexes)) + '.')
                decrypted_scope.insert(END, decrypted_text)
        except NameError:
            messagebox.showinfo("Info", "Read the file first.")

    d_window = Toplevel(window)
    d_window.geometry("640x480")
    d_window.title("Text decryptor")

    Button(d_window, text="Browse file", font=("Century Gothic", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=open_file).place(x=25, y=-5, height=24, width=80)
    Button(d_window, text="Save file", font=("Century Gothic", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=save_file).place(x=105, y=-5, height=24, width=65)

    encrypted_scope = Text(d_window, bg="#F8F8F8", fg="#8C9E89", selectbackground="#8C9E89", padx=6, pady=2,
                           font=("Ubuntu Mono", 11))
    matrix_scope = Text(d_window, bg="#F8F8F8", fg="#DFB6B0", selectbackground="#DFB6B0", relief="groove", padx=12,
                        pady=2, font=("Ubuntu Mono", 11))
    step1_scope = Text(d_window, bg="#F8F8F8", fg="#DFB6B0", selectbackground="#DFB6B0", relief="groove", padx=5,
                       font=("Ubuntu Mono", 11))
    step2_scope = Text(d_window, bg="#F8F8F8", fg="#DFB6B0", selectbackground="#DFB6B0", relief="groove", padx=5,
                       font=("Ubuntu Mono", 11))
    decrypted_scope = Text(d_window, bg="#F8F8F8", fg="#8C9E89", selectbackground="#8C9E89", padx=6, pady=2,
                           font=("Ubuntu Mono", 11))

    Button(d_window, text="DECRYPT", font=("Century Gothic", 10, "bold"), bg="#F0F0F0", fg="#b67162", borderwidth=2,
           relief="groove", command=decrypt).place(x=356, y=16, height=25, width=70)

    Label(d_window, text="Encrypted text", font=("Century Gothic", 10), fg="#414141").place(x=25, y=27)
    Label(d_window, text="Decrypted text", font=("Century Gothic", 10), fg="#414141").place(x=25, y=242)
    Label(d_window, text="Alphabet matrix", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441, y=28)
    Label(d_window, text="Encrypted text indexes", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441,
                                                                                                              y=171)
    Label(d_window, text="Decrypted text indexes", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=441,
                                                                                                              y=315)

    encrypted_scope.place(x=25, y=50, height=190, width=401)
    decrypted_scope.place(x=25, y=265, height=190, width=401)
    matrix_scope.place(x=441, y=50, height=118, width=174)
    step1_scope.place(x=441, y=193, height=118, width=174)
    step2_scope.place(x=441, y=337, height=118, width=174)


window = Tk()
window.geometry("400x150")
window.title("Polybius square")
Label(window, text="I would like to", font=("Century Gothic", 13, "bold"), fg="#464646").place(x=139, y=35)
encrypt_text_button = Button(window, text="encrypt text", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                             fg="#5D5D5D", borderwidth=2, relief="ridge", command=text_encryptor)
decrypt_text_button = Button(window, text="decrypt text", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                             fg="#5D5D5D", borderwidth=2, relief="ridge", command=text_decryptor)
encrypt_text_button.place(x=75, y=75, height=25, width=100)
decrypt_text_button.place(x=225, y=75, height=25, width=100)
mainloop()
