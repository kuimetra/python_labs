from tkinter import filedialog, messagebox
from tkinter import *
import numpy as np


def get_alphabet(text):
    eng_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    ukr_alphabet = ['А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л',
                    'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я']
    if all(letter in eng_alphabet for letter in text.upper() if letter.isalpha()):
        return eng_alphabet
    elif all(letter in ukr_alphabet for letter in text.upper() if letter.isalpha()):
        return ukr_alphabet
    else:
        messagebox.showerror("Error", "The text should contain only Eng/Ukr letters.")


def keys_to_text(text, keys):
    key_text, i = '', 0
    for char in text:
        if char.isalpha():
            if char.isupper():
                key_text += keys[i]
            else:
                key_text += keys[i].lower()
            i += 1
        else:
            key_text += char
    return key_text


def text_encryptor():
    def open_file():
        path = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*.txt"),))
        if path:
            with open(path, "r", encoding="utf-8-sig") as file:
                text = file.read().strip("\n ")
            input_scope.delete("1.0", END)
            input_scope.insert(END, text)

    def save_encrypted_file():
        path = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*.txt"),),
                                            defaultextension=(("Text Files", "*.txt"),))
        if path:
            with open(path, "w+", encoding="utf-8-sig") as file:
                try:
                    file.write(','.join(keys) + '\n')
                    file.write(encrypted_text)
                except NameError:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def encrypt():
        global keys, encrypted_text
        key_scope.delete("1.0", END)
        output_scope.delete("1.0", END)
        index_scope.delete("1.0", END)
        text = input_scope.get("1.0", END).strip("\n ")
        if get_alphabet(text):
            alphabet = get_alphabet(text)
            amount_of_letters = 0
            for char in text:
                if char.isalpha():
                    amount_of_letters += 1
            keys = np.random.choice(alphabet, amount_of_letters)
            key_text = keys_to_text(text, keys)

            encrypted_text = ''
            for text_letter, key_letter in zip(text, key_text):
                if text_letter.upper() in alphabet:
                    encrypted_index = (alphabet.index(text_letter.upper()) + alphabet.index(key_letter.upper())) % \
                                      len(alphabet)
                    if text_letter.isupper():
                        encrypted_text += alphabet[encrypted_index]
                    else:
                        encrypted_text += alphabet[encrypted_index].lower()
                else:
                    encrypted_text += text_letter
            key_scope.insert(END, key_text)
            output_scope.insert(END, encrypted_text)
            index_letter = ''
            for index, letter in zip(range(len(alphabet)), alphabet):
                index_letter += f'{index} - {letter}\n'
            index_scope.insert(END, index_letter.strip('\n'), 'tag-center')

    e_window = Toplevel(window)
    e_window.geometry("520x390")
    e_window.title("Text encryptor")
    e_window.configure(background="#ECECEC")
    Button(e_window, text="Browse file", font=("GT Walsheim Pro", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=open_file).place(x=25, y=-4, height=23, width=75)
    Button(e_window, text="Save file", font=("GT Walsheim Pro", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=save_encrypted_file).place(x=100, y=-4, height=23, width=60)

    input_scope = Text(e_window, bg="#F8F8F8", fg="#6ba8a9", selectbackground="#6ba8a9", padx=4, pady=2,
                       font=("Cartograph CF", 10))
    key_scope = Text(e_window, bg="#F8F8F8", fg="#6c7b95", selectbackground="#6c7b95", padx=4, pady=2,
                     font=("Cartograph CF Italic", 10))
    output_scope = Text(e_window, bg="#F8F8F8", fg="#6ba8a9", selectbackground="#6ba8a9", padx=4, pady=2,
                        font=("Cartograph CF", 10))
    index_scope = Text(e_window, bg="#F8F8F8", fg="#464159", selectbackground="#464159", padx=4, pady=2,
                       font=("Cartograph CF", 10))
    index_scope.tag_configure('tag-center', justify='center')
    Button(e_window, text="ENCRYPT", font=("GT Walsheim Pro Medium", 11), bg="#F0F0F0", fg="#464159", borderwidth=2,
           relief="groove", command=encrypt).place(x=415, y=11, height=25, width=80)

    Label(e_window, text="Given text", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=23)
    Label(e_window, text="Key", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=138)
    Label(e_window, text="Encrypted text", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=252)

    input_scope.place(x=25, y=46, height=90, width=375)
    key_scope.place(x=25, y=161, height=89, width=375)
    output_scope.place(x=25, y=275, height=90, width=375)
    index_scope.place(x=415, y=46, height=319, width=80)


def text_decryptor():
    def open_encrypted_file():
        global encrypted_file, encrypted_text
        path = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*.txt"),))
        if path:
            with open(path, "r", encoding="utf-8-sig") as file:
                encrypted_file = file.read().strip("\n ")
            encrypted_text = '\n'.join(encrypted_file.strip('\n').split('\n')[1:])
            encrypted_scope.delete("1.0", END)
            encrypted_scope.insert(END, encrypted_text)

    def save_decrypted_file():
        path = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*.txt"),),
                                            defaultextension=(("Text Files", "*.txt"),))
        if path:
            with open(path, "w+", encoding="utf-8-sig") as file:
                try:
                    file.write(encrypted_text + '\n')
                    file.write(','.join(keys) + '\n')
                    file.write(decrypted_text)
                except NameError:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def decrypt():
        global keys, decrypted_text
        key_scope.delete("1.0", END)
        decrypted_scope.delete("1.0", END)
        index_scope.delete("1.0", END)
        if get_alphabet(encrypted_text):
            alphabet = get_alphabet(encrypted_text)
            keys = encrypted_file.split('\n')[0].split(',')
            key_text = keys_to_text(encrypted_text, keys)

            decrypted_text = ''
            for text_letter, key_letter in zip(encrypted_text, key_text):
                if text_letter.upper() in alphabet:
                    decrypted_index = (len(alphabet) - alphabet.index(key_letter.upper()) +
                                       alphabet.index(text_letter.upper())) % len(alphabet)
                    if text_letter.isupper():
                        decrypted_text += alphabet[decrypted_index]
                    else:
                        decrypted_text += alphabet[decrypted_index].lower()
                else:
                    decrypted_text += text_letter
            key_scope.insert(END, key_text)
            decrypted_scope.insert(END, decrypted_text)
            index_letter = ''
            for index, letter in zip(range(len(alphabet)), alphabet):
                index_letter += f'{index} - {letter}\n'
            index_scope.insert(END, index_letter.strip('\n'), 'tag-center')

    d_window = Toplevel(window)
    d_window.geometry("520x390")
    d_window.title("Text decryptor")
    d_window.configure(background="#ECECEC")
    Button(d_window, text="Browse file", font=("GT Walsheim Pro", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=open_encrypted_file).place(x=25, y=-4, height=23, width=75)
    Button(d_window, text="Save file", font=("GT Walsheim Pro", 10), bg="#F0F0F0", fg="#414141", relief="groove",
           command=save_decrypted_file).place(x=100, y=-4, height=23, width=60)

    encrypted_scope = Text(d_window, bg="#F8F8F8", fg="#6c7b95", selectbackground="#6c7b95", padx=4, pady=2,
                           font=("Cartograph CF", 10))
    key_scope = Text(d_window, bg="#F8F8F8", fg="#6ba8a9", selectbackground="#6ba8a9", padx=4, pady=2,
                     font=("Cartograph CF Italic", 10))
    decrypted_scope = Text(d_window, bg="#F8F8F8", fg="#6c7b95", selectbackground="#6c7b95", padx=4, pady=2,
                           font=("Cartograph CF", 10))
    index_scope = Text(d_window, bg="#F8F8F8", fg="#1d4d4f", selectbackground="#1d4d4f", padx=4, pady=2,
                       font=("Cartograph CF", 10))
    index_scope.tag_configure('tag-center', justify='center')

    Button(d_window, text="DECRYPT", font=("GT Walsheim Pro Medium", 11), bg="#F0F0F0", fg="#1d4d4f", borderwidth=2,
           relief="groove", command=decrypt).place(x=415, y=11, height=25, width=80)

    Label(d_window, text="Encrypted text", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=23)
    Label(d_window, text="Key", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=138)
    Label(d_window, text="Decrypted text", font=("GT Walsheim Pro", 11), bg="#ECECEC", fg="#414141").place(x=25, y=252)

    encrypted_scope.place(x=25, y=46, height=90, width=375)
    key_scope.place(x=25, y=161, height=89, width=375)
    decrypted_scope.place(x=25, y=275, height=90, width=375)
    index_scope.place(x=415, y=46, height=319, width=80)


window = Tk()
window.geometry("400x150")
window.title("Vigenere cipher")
Label(window, text="I would like to", font=("GT Walsheim Pro Bold", 14), fg="#414141").place(x=135, y=35)
Button(window, text="encrypt text", font=("GT Walsheim Pro Medium", 11), bg="#F0F0F0", fg="#515151", borderwidth=2,
       relief="groove", command=text_encryptor).place(x=75, y=75, height=25, width=100)
Button(window, text="decrypt text", font=("GT Walsheim Pro Medium", 11), bg="#F0F0F0", fg="#515151", borderwidth=2,
       relief="groove", command=text_decryptor).place(x=225, y=75, height=25, width=100)
mainloop()
