from datetime import datetime
from tkinter import *
import pandas as pd
import numpy as np
import random
import math

window = Tk()
window.geometry("400x150")
window.title("Encrypting and decrypting")


def shuffle(size):
    index_arr, i = [], 0
    while i < size:
        index = random.randint(0, size - 1)
        if index not in index_arr:
            index_arr.append(index)
            i += 1
    return index_arr


def factors(text_length):
    return [f"({i}*{text_length / i})" for i in range(1, text_length + 1) if text_length % i == 0]


def recommended_size(text_length):
    return math.ceil(math.sqrt(text_length))


def text_encryptor():
    def encrypt():
        encrypted_text_scope.delete("1.0", END)
        encryption_steps_scope.delete("1.0", END)
        global row_size, row_indexes, col_size, col_indexes, encrypted_text
        if read_from.get() == "file":
            file_name = file_input_scope.get("1.0", END).strip("\n ")
            if file_name:
                try:
                    with open(f"{file_name}.txt", "r", encoding="utf-8-sig") as file:
                        text = file.read().strip("\n ")
                    if text.isspace() or len(text) == 0:
                        text_scope.delete("1.0", END)
                        encrypted_text_scope.insert(END, "File is empty.\n")
                        text = 0
                    else:
                        text_scope.delete("1.0", END)
                        text_scope.insert(END, text)
                except FileNotFoundError:
                    text_scope.delete("1.0", END)
                    encrypted_text_scope.insert(END, "No such file.\n")
                    text = 0
            else:
                encrypted_text_scope.insert(END, "Enter a file name.\n")
                text_scope.delete("1.0", END)
                text = 0
        elif read_from.get() == "text_scope":
            text = text_scope.get("1.0", END).strip("\n ")
            if text.isspace() or len(text) == 0:
                encrypted_text_scope.insert(END, "Enter text.\n")
                text = 0
        if text:
            try:
                row_size, col_size = int(row_size_scope.get("1.0", END).strip("\n")), int(
                    col_size_scope.get("1.0", END).strip("\n "))
            except ValueError:
                encrypted_text_scope.insert(END, "The size of the matrix is missing.\n")
            else:
                if row_size * col_size < len(text):
                    encrypted_text_scope.insert(END,
                                                "Incorrect size of matrix.\n\n\n* Size of the matrix without empty "
                                                "cells:\n" + " or ".join(factors(len(text))) + ".\n\n* The square "
                                                "matrix with the least number of empty cells: " +
                                                f"{recommended_size(len(text))}*{recommended_size(len(text))}."
                                                f"\n\n* You can also enter your own matrix size option but row*col"
                                                f" must be greater than or equal to {len(text)}.")
                else:
                    if row_size * col_size > len(text):
                        matrix = np.reshape(
                            np.array(list(text) + [' ' for _ in range(row_size * col_size - len(text))]),
                            (row_size, col_size))
                    elif row_size * col_size == len(text):
                        matrix = np.reshape(np.array(list(text)), (row_size, col_size))
                    # row_indexes = list(range(row_size))
                    # col_indexes = list(range(col_size))
                    # random.shuffle(row_indexes)
                    # random.shuffle(col_indexes)
                    row_indexes = shuffle(row_size)
                    col_indexes = shuffle(col_size)

                    swapped_rows_of_encrypted = matrix[row_indexes]
                    swapped_columns_of_encrypted = swapped_rows_of_encrypted[:, col_indexes]
                    encrypted_text = ''.join(swapped_columns_of_encrypted.flatten())
                    encrypted_text_scope.insert(END, encrypted_text)
                    encryption_steps_scope.insert(END, "(0) Given text to matrix.\n")
                    encryption_steps_scope.insert(END, matrix)
                    encryption_steps_scope.insert(END, "\n\n(1) Swap rows using keys (" +
                                                  ', '.join(map(str, row_indexes)) + ").\n")
                    encryption_steps_scope.insert(END, swapped_rows_of_encrypted)
                    encryption_steps_scope.insert(END, "\n\n(2) Swap columns using keys (" +
                                                  ', '.join(map(str, col_indexes)) + ").\n")
                    encryption_steps_scope.insert(END, swapped_columns_of_encrypted)
                    encryption_steps_scope.insert(END, '\n')

    def save_to_file():
        file_output_name = file_output_scope.get("1.0", END).strip("\n ")
        if file_output_name:
            file_with_results = open(f"{file_output_name}.txt", "w+", encoding="utf-8-sig")
        else:
            file_with_results = open("{0}.txt".format(datetime.now().strftime("%m_%d_%Y-%I_%M_%S_%p")), "w+",
                                     encoding="utf-8-sig")
        file_with_results.write(f"{row_size} " + ','.join(map(str, row_indexes)) + f"\n{col_size} " +
                                ','.join(map(str, col_indexes)) + f"\n{encrypted_text}")
        file_with_results.close()

    encryptor_window = Toplevel(window)
    encryptor_window.title("Text encryptor")
    encryptor_window.geometry("800x600")

    file_input_scope = Text(encryptor_window, bg="#F8F8F8", fg="#527174", selectbackground="#527174",
                            relief="groove", borderwidth=2, padx=4, pady=3, font=("Ubuntu Mono", 11))
    clear_file_input_button = Button(encryptor_window, text="X", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                                     fg="#455054", borderwidth=2, relief="groove",
                                     command=lambda: file_input_scope.delete("1.0", END))
    file_output_scope = Text(encryptor_window, bg="#F8F8F8", fg="#527174", selectbackground="#527174",
                             relief="groove", borderwidth=2, padx=4, pady=3, font=("Ubuntu Mono", 11))
    clear_file_output_button = Button(encryptor_window, text="X", font=("Century Gothic", 10, "bold"),
                                      bg="#F0F0F0", fg="#455054", borderwidth=2, relief="groove",
                                      command=lambda: file_output_scope.delete("1.0", END))
    row_size_scope = Text(encryptor_window, bg="#F8F8F8", fg="#527174", selectbackground="#527174",
                          relief="groove", borderwidth=2, padx=4, pady=3, font=("Ubuntu Mono", 11))
    col_size_scope = Text(encryptor_window, bg="#F8F8F8", fg="#527174", selectbackground="#527174",
                          relief="groove", borderwidth=2, padx=4, pady=3, font=("Ubuntu Mono", 11))
    encrypt_button = Button(encryptor_window, text="ENCRYPT", font=("Century Gothic", 11, "bold"), bg="#F0F0F0",
                            fg="#437681", borderwidth=2, relief="ridge", command=lambda: encrypt())
    save_button = Button(encryptor_window, text="SAVE", font=("Century Gothic", 11, "bold"), bg="#F0F0F0",
                         fg="#437681", borderwidth=2, relief="ridge", command=lambda: save_to_file())

    read_from = StringVar(value=0)
    read_from.set("file")
    Radiobutton(encryptor_window, text="file text", var=read_from, value="file",
                font=("Century Gothic", 10), fg="#527174").place(x=320, y=20)
    Radiobutton(encryptor_window, text="input text", var=read_from, value="text_scope",
                font=("Century Gothic", 10), fg="#527174").place(x=320, y=38)

    text_scope = Text(encryptor_window, bg="#F8F8F8", fg="#7DB5AE", selectbackground="#7DB5AE", padx=6, pady=4,
                      borderwidth=2, font=("Ubuntu Mono", 11), relief="groove")
    encrypted_text_scope = Text(encryptor_window, bg="#F8F8F8", fg="#7DB5AE", selectbackground="#7DB5AE", padx=6,
                                pady=4, borderwidth=2, font=("Ubuntu Mono", 11), relief="groove")
    encryption_steps_scope = Text(encryptor_window, bg="#F8F8F8", fg="#609698", selectbackground="#609698", padx=6,
                                  pady=4, borderwidth=2, font=("Ubuntu Mono", 11), relief="groove", wrap=NONE)
    encryption_steps_xscrollbar = Scrollbar(encryption_steps_scope, orient=HORIZONTAL)
    encryption_steps_xscrollbar.config(command=encryption_steps_scope.xview)
    encryption_steps_scope.configure(xscrollcommand=encryption_steps_xscrollbar.set)
    encryption_steps_xscrollbar.pack(side=BOTTOM, fill=X)

    Label(encryptor_window, text="Read from (.txt)", font=("Century Gothic", 11, "bold"), fg="#455054").place(x=23, y=6)
    Label(encryptor_window, text="Save to (.txt)", font=("Century Gothic", 11, "bold"), fg="#455054").place(x=523, y=6)
    Label(encryptor_window, text="Matrix size", font=("Century Gothic", 11, "bold"), fg="#455054").place(x=214, y=6)
    Label(encryptor_window, text="x", font=("Century Gothic", 13), fg="#455054").place(x=250, y=27)
    Label(encryptor_window, text="Text", font=("Century Gothic", 11), fg="#455054").place(x=23, y=54)
    Label(encryptor_window, text="Encrypted text", font=("Century Gothic", 11), fg="#455054").place(x=23, y=314)
    Label(encryptor_window, text="Encryption steps", font=("Century Gothic", 11), fg="#455054").place(x=523, y=54)

    file_input_scope.place(x=25, y=30, height=25, width=140)
    clear_file_input_button.place(x=165, y=30, height=25, width=25)
    row_size_scope.place(x=212, y=30, height=25, width=35)
    col_size_scope.place(x=267, y=30, height=25, width=35)
    encrypt_button.place(x=420, y=30, height=25, width=80)
    file_output_scope.place(x=525, y=30, height=25, width=150)
    clear_file_output_button.place(x=675, y=30, height=25, width=25)
    save_button.place(x=710, y=30, height=25, width=65)
    text_scope.place(x=25, y=80, height=235, width=475)
    encrypted_text_scope.place(x=25, y=340, height=235, width=475)
    encryption_steps_scope.place(x=525, y=80, height=495, width=250)


def text_decoder():
    def decrypt():
        decrypted_text_scope.delete("1.0", END)
        decryption_steps_scope.delete("1.0", END)
        file_name = file_input_scope.get("1.0", END).strip("\n ")
        if file_name:
            try:
                with open(f"{file_name}.txt", "r", encoding="utf-8-sig") as file:
                    file_text = file.readlines()
                if ''.join(file_text).isspace() or len(file_text) == 0:
                    decrypted_text_scope.insert(END, "File is empty.\n")
                else:
                    text_scope.delete("1.0", END)
                    text_scope.insert(END, "".join(file_text[2:]).strip("\n "))
            except FileNotFoundError:
                decrypted_text_scope.insert(END, "No such file.\n")
            else:
                row_size, col_size = int(file_text[0].split()[0]), int(file_text[1].split()[0])
                row_indexes, col_indexes = file_text[0].split()[1].split(','), file_text[1].split()[1].split(',')
                encrypted_text = ''.join(file_text[2:])

                df = pd.DataFrame(np.reshape(np.array(list(encrypted_text)), (row_size, col_size)))
                df.index, df.columns = row_indexes, col_indexes
                df.index, df.columns = df.index.astype(int), df.columns.astype(int)
                swapped_columns_of_decrypted = df.sort_index(axis=1)
                swapped_rows_of_decrypted = swapped_columns_of_decrypted.sort_index(axis=0)
                decrypted_text_scope.insert(END, ''.join(swapped_rows_of_decrypted.to_numpy().flatten()).rstrip('\n '))

                decryption_steps_scope.insert(END, "(0) Given text to matrix.\n")
                decryption_steps_scope.insert(END, df)
                decryption_steps_scope.insert(END, "\n\n(1) Swap columns in ascending order of indexes.\n")
                decryption_steps_scope.insert(END, swapped_columns_of_decrypted)
                decryption_steps_scope.insert(END, "\n\n(2) Swap rows in ascending order of indexes.\n")
                decryption_steps_scope.insert(END, swapped_rows_of_decrypted)
                decryption_steps_scope.insert(END, '\n')

                with open(f"{file_name}_decrypted.txt", "w+") as file_with_decrypted_text:
                    file_with_decrypted_text.write(
                        ''.join(swapped_rows_of_decrypted.to_numpy().flatten()).rstrip('\n '))
        else:
            decrypted_text_scope.insert(END, "Enter a file name.\n")

    decryptor_window = Toplevel(window)
    decryptor_window.title("Text decryptor")
    decryptor_window.geometry("800x600")
    file_input_scope = Text(decryptor_window, bg="#F8F8F8", fg="#6E6B8F", selectbackground="#6E6B8F",
                            relief="groove", borderwidth=2, padx=4, pady=3, font=("Ubuntu Mono", 11))
    clear_button = Button(decryptor_window, text="X", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                          fg="#414141", borderwidth=2, relief="groove",
                          command=lambda: file_input_scope.delete("1.0", END))
    decrypt_button = Button(decryptor_window, text="DECRYPT", font=("Century Gothic", 11, "bold"), bg="#F0F0F0",
                            fg="#715F8F", borderwidth=2, relief="ridge", command=lambda: decrypt())

    text_scope = Text(decryptor_window, bg="#F8F8F8", fg="#D7A2AF", selectbackground="#D7A2AF", padx=6, pady=4,
                      borderwidth=2, font=("Ubuntu Mono", 11), relief="groove")
    decrypted_text_scope = Text(decryptor_window, bg="#F8F8F8", fg="#D7A2AF", selectbackground="#D7A2AF", padx=6,
                                pady=4, borderwidth=2, font=("Ubuntu Mono", 11), relief="groove")
    decryption_steps_scope = Text(decryptor_window, bg="#F8F8F8", fg="#6B778E", selectbackground="#6B778E", padx=6,
                                  pady=4, borderwidth=2, font=("Ubuntu Mono", 11), relief="groove", wrap=NONE)
    decryption_steps_xscrollbar = Scrollbar(decryption_steps_scope, orient=HORIZONTAL)
    decryption_steps_xscrollbar.config(command=decryption_steps_scope.xview)
    decryption_steps_scope.configure(xscrollcommand=decryption_steps_xscrollbar.set)
    decryption_steps_xscrollbar.pack(side=BOTTOM, fill=X)

    Label(decryptor_window, text="File name (.txt)", font=("Century Gothic", 11, "bold"), fg="#635B67").place(x=23,
                                                                                                              y=29)
    Label(decryptor_window, text="Encrypted text", font=("Century Gothic", 11), fg="#635B67").place(x=23, y=54)
    Label(decryptor_window, text="Decrypted text", font=("Century Gothic", 11), fg="#635B67").place(x=23, y=314)
    Label(decryptor_window, text="Decryption steps", font=("Century Gothic", 11), fg="#635B67").place(x=523, y=54)

    file_input_scope.place(x=145, y=30, height=25, width=240)
    clear_button.place(x=385, y=30, height=25, width=25)
    decrypt_button.place(x=420, y=30, height=25, width=80)
    text_scope.place(x=25, y=80, height=235, width=475)
    decrypted_text_scope.place(x=25, y=340, height=235, width=475)
    decryption_steps_scope.place(x=525, y=80, height=495, width=250)


Label(window, text="I would like to", font=("Century Gothic", 13, "bold"), fg="#464646").place(x=139, y=35)
encrypt_text_button = Button(window, text="encrypt text", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                             fg="#5D5D5D", borderwidth=2, relief="ridge", command=text_encryptor)
decrypt_text_button = Button(window, text="decrypt text", font=("Century Gothic", 10, "bold"), bg="#F0F0F0",
                             fg="#5D5D5D", borderwidth=2, relief="ridge", command=text_decoder)
encrypt_text_button.place(x=75, y=75, height=25, width=100)
decrypt_text_button.place(x=225, y=75, height=25, width=100)
mainloop()
