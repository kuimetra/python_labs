from datetime import datetime
from tkinter import *
import pandas as pd
import logging


def get_encrypted_text():
    file_name = file_input_scope.get("1.0", END).strip("\n ")
    encrypted_text_scope.delete("1.0", END)
    if file_name:
        try:
            with open(f"{file_name}", "r", encoding="utf-8-sig") as file:
                global encrypted_text
                encrypted_text = file.read()
        except FileNotFoundError:
            encrypted_text_scope.insert(END, "NO SUCH FILE")
        else:
            if encrypted_text.isspace() or len(encrypted_text) == 0:
                encrypted_text_scope.insert(END, "FILE IS EMPTY")
            else:
                return encrypted_text
    else:
        encrypted_text_scope.insert(END, "ENTER A FILE NAME")


def get_decrypted_text(cipher_key, encrypted_text):
    encrypted_text_to_list = list(encrypted_text)
    for i, letter in enumerate(encrypted_text_to_list):
        if letter in cipher_key.keys():
            encrypted_text_to_list[i] = cipher_key.get(letter)
    return "".join(encrypted_text_to_list)


def decrypt_using_aver_freq(encrypted_text):
    global decrypted_text, cipher_key
    decrypted_df = pd.read_csv("average_frequency.csv")
    decrypted_df = decrypted_df.sort_values(by=decrypted_df.columns[1], ascending=False)

    encrypted_df = pd.DataFrame(decrypted_df["Letter"].to_list(), columns=["Letter"])
    letter_amount_dict = dict.fromkeys(decrypted_df["Letter"].to_list(), 0)
    amount_of_chars = 0
    for letter in encrypted_text:
        if letter in list(letter_amount_dict.keys()) + list(k.lower() for k in letter_amount_dict.keys()):
            letter_amount_dict[letter.upper()] += 1
            amount_of_chars += 1
    text_frequency = []
    for amount_of_char in letter_amount_dict.values():
        text_frequency.append(round(100 * amount_of_char / amount_of_chars, 2))
    encrypted_df["Frequency"] = text_frequency
    encrypted_df = encrypted_df.sort_values(by=encrypted_df.columns[1], ascending=False)

    cipher_key = {k: v for k, v in zip(encrypted_df["Letter"].to_list(),
                                       decrypted_df["Letter"].to_list())}
    cipher_key_lower = dict((k.lower(), v.lower()) for k, v in cipher_key.items())
    cipher_key = dict(sorted(cipher_key.items()))
    case_sensitive_cipher_key = {**cipher_key, **cipher_key_lower}
    # decrypted_text = encrypted_text.translate(str.maketrans(case_sensitive_cipher_key))
    decrypted_text = get_decrypted_text(case_sensitive_cipher_key, encrypted_text)

    encrypted_text_scope.insert(END, encrypted_text)
    decrypted_text_scope.insert(END, decrypted_text)
    encrypted_frequency_scope.insert(END, encrypted_df.to_string(index=False, header=False))
    decrypted_frequency_scope.insert(END, decrypted_df.to_string(index=False, header=False))
    encrypted_letters_scope.insert(END, " ".join(list(cipher_key.keys())))
    decrypted_letters_scope.insert(END, " ".join(list(cipher_key.values())))


def decrypt_using_file_keys(encrypted_text):
    global decrypted_text, cipher_key
    keys_df = pd.read_csv("keys.csv")
    cipher_key = dict(keys_df.values)
    cipher_key = dict(sorted(cipher_key.items()))
    cipher_key_lower = dict((k.lower(), v.lower()) for k, v in cipher_key.items())
    case_sensitive_cipher_key = {**cipher_key, **cipher_key_lower}
    decrypted_text = get_decrypted_text(case_sensitive_cipher_key, encrypted_text)

    encrypted_text_scope.insert(END, encrypted_text)
    decrypted_text_scope.insert(END, decrypted_text)
    encrypted_letters_scope.insert(END, " ".join(list(cipher_key.keys())))
    decrypted_letters_scope.insert(END, " ".join(list(cipher_key.values())))


def update():
    global encrypted_text, decrypted_text, cipher_key
    try:
        decrypted_text_scope.delete("1.0", END)
        encrypted_letters_scope.delete("1.0", END)
        decrypted_letters_scope.delete("1.0", END)

        encrypted_letter = from_scope.get("1.0", END).strip("\n ").upper()
        decrypted_letter = to_scope.get("1.0", END).strip("\n ").upper()
        if encrypted_letter in list(cipher_key.keys()) and decrypted_letter in list(cipher_key.keys()):
            cipher_key[encrypted_letter] = decrypted_letter
            logging.basicConfig(filename="{0}.log".format(datetime.now().strftime("%m_%d_%Y-%I_%M_%S_%p")),
                                format='%(message)s', level=logging.INFO)
            logging.info(f"{encrypted_letter} -> {decrypted_letter}")
        cipher_key_lower = dict((k.lower(), v.lower()) for k, v in cipher_key.items())
        case_sensitive_cipher_key = {**cipher_key, **cipher_key_lower}
        decrypted_text = get_decrypted_text(case_sensitive_cipher_key, encrypted_text)

        decrypted_text_scope.insert(END, decrypted_text)
        encrypted_letters_scope.insert(END, " ".join(list(cipher_key.keys())))
        decrypted_letters_scope.insert(END, " ".join(list(cipher_key.values())))
        from_scope.delete("1.0", END)
        to_scope.delete("1.0", END)
    except NameError:
        encrypted_text_scope.delete("1.0", END)
        encrypted_text_scope.insert(END, "DECRYPT TEXT FIRST")


def save_results():
    global decrypted_text
    try:
        with open("results.txt", "w") as file_with_decrypted_text:
            file_with_decrypted_text.write(encrypted_text + "-" * 100 + "\n")
            for k, v in cipher_key.items():
                file_with_decrypted_text.write(k + "," + v + "\n")
            file_with_decrypted_text.write("-" * 100 + "\n" + decrypted_text)
    except NameError:
        encrypted_text_scope.delete("1.0", END)
        encrypted_text_scope.insert(END, "DECRYPT TEXT FIRST")


def decrypt_output(option):
    encrypted_text_scope.delete("1.0", END)
    decrypted_text_scope.delete("1.0", END)
    encrypted_frequency_scope.delete("1.0", END)
    decrypted_frequency_scope.delete("1.0", END)
    encrypted_letters_scope.delete("1.0", END)
    decrypted_letters_scope.delete("1.0", END)

    if get_encrypted_text():
        if option == "aver_freq":
            decrypt_using_aver_freq(get_encrypted_text())
        elif option == "file_keys":
            decrypt_using_file_keys(get_encrypted_text())


window = Tk()
window.geometry("895x670")
window.title("Decrypting by a frequency table")

file_input_scope = Text(window, bg="#F8F8F8", fg="#204051", selectbackground="#204051", relief="groove", borderwidth=2,
                        padx=4, pady=3, font=("Ubuntu Mono", 11))
clear_button = Button(window, text="X", font=("Century Gothic", 10, "bold"), bg="#F0F0F0", fg="#414141", borderwidth=2,
                      relief="groove", command=lambda: file_input_scope.delete("1.0", END))
decrypt_with_aver_freq_button = Button(window, text="AV FREQ", font=("Century Gothic", 10), bg="#F0F0F0", fg="#204051",
                                       borderwidth=2, relief="ridge", command=lambda: decrypt_output("aver_freq"))
decrypt_with_file_keys_button = Button(window, text="FILE KEYS", font=("Century Gothic", 10), bg="#F0F0F0",
                                       fg="#204051", borderwidth=2, relief="ridge",
                                       command=lambda: decrypt_output("file_keys"))

encrypted_text_scope = Text(window, bg="#F8F8F8", fg="#84a9ac", selectbackground="#84a9ac", padx=6, pady=4,
                            borderwidth=2, font=("Ubuntu Mono", 11), relief="groove", wrap=NONE)
encrypted_xscrollbar = Scrollbar(encrypted_text_scope, orient=HORIZONTAL)
encrypted_xscrollbar.config(command=encrypted_text_scope.xview)
encrypted_text_scope.configure(xscrollcommand=encrypted_xscrollbar.set)
encrypted_xscrollbar.pack(side=BOTTOM, fill=X)

decrypted_text_scope = Text(window, bg="#F8F8F8", fg="#84a9ac", selectbackground="#84a9ac", padx=6, pady=4,
                            font=("Ubuntu Mono", 11), borderwidth=2, relief="groove", wrap=NONE)
decrypted_xscrollbar = Scrollbar(decrypted_text_scope, orient=HORIZONTAL)
decrypted_xscrollbar.config(command=decrypted_text_scope.xview)
decrypted_text_scope.configure(xscrollcommand=decrypted_xscrollbar.set)
decrypted_xscrollbar.pack(side=BOTTOM, fill=X)

encrypted_frequency_scope = Text(window, bg="#F0F0F0", fg="#3b6978", selectbackground="#3b6978", relief="groove",
                                 padx=6, pady=2, borderwidth=2, font=("Ubuntu Mono", 11))
decrypted_frequency_scope = Text(window, bg="#F0F0F0", fg="#3b6978", selectbackground="#3b6978", relief="groove",
                                 padx=6, pady=2, borderwidth=2, font=("Ubuntu Mono", 11))

encrypted_letters_scope = Text(window, bg="#F0F0F0", fg="#3b6978", selectbackground="#3b6978", padx=8, borderwidth=2,
                               font=("Ubuntu Mono", 9), relief="groove")
decrypted_letters_scope = Text(window, bg="#F0F0F0", fg="#3b6978", selectbackground="#3b6978", padx=8, borderwidth=2,
                               font=("Ubuntu Mono", 9), relief="groove")

from_scope = Text(window, bg="#F8F8F8", fg="#204051", selectbackground="#204051", padx=3, pady=3, relief="groove",
                  font=("Ubuntu Mono", 11))
to_scope = Text(window, bg="#F8F8F8", fg="#204051", selectbackground="#204051", padx=3, pady=3, relief="groove",
                font=("Ubuntu Mono", 11))

update_button = Button(window, text="UPDATE", font=("Century Gothic", 10), bg="#F0F0F0", fg="#204051", borderwidth=2,
                       relief="ridge", command=lambda: update())
save_button = Button(window, text="SAVE", font=("Century Gothic", 10), bg="#F0F0F0", fg="#204051", borderwidth=2,
                     relief="ridge", command=lambda: save_results())
exit_button = Button(window, text="EXIT", font=("Century Gothic", 10, "bold"), bg="#F0F0F0", fg="#204051",
                     borderwidth=2, relief="ridge", command=lambda: window.destroy())

Label(window, text="File name:", font=("Century Gothic", 11), fg="#161616").place(x=22, y=25)
Label(window, text="Decrypt with:", font=("Century Gothic", 11), fg="#161616").place(x=257, y=25)
Label(window, text="Encrypted text:", font=("Century Gothic", 11, "italic"), fg="#414141").place(x=23, y=51)
Label(window, text="Decrypted text:", font=("Century Gothic", 11, "italic"), fg="#414141").place(x=23, y=349)
Label(window, text="Frequency in the text:", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=541, y=53)
Label(window, text="Average frequency:", font=("Century Gothic", 10, "italic"), fg="#414141").place(x=717, y=53)
Label(window, text="To:", font=("Century Gothic", 11, "italic"), fg="#414141").place(x=634, y=620)
Label(window, text="From:", font=("Century Gothic", 11, "italic"), fg="#414141").place(x=543, y=620)

file_input_scope.place(x=105, y=25, height=25, width=123)
clear_button.place(x=228, y=25, height=25, width=25)
decrypt_with_aver_freq_button.place(x=363, y=25, height=25, width=70)
decrypt_with_file_keys_button.place(x=438, y=25, height=25, width=70)
encrypted_text_scope.place(x=25, y=75, height=272, width=483)
decrypted_text_scope.place(x=25, y=373, height=272, width=483)
encrypted_frequency_scope.place(x=543, y=75, height=451, width=151)
decrypted_frequency_scope.place(x=719, y=75, height=451, width=151)
encrypted_letters_scope.place(x=543, y=541, height=25, width=327)
decrypted_letters_scope.place(x=543, y=580, height=25, width=327)
from_scope.place(x=597, y=620, height=25, width=25)
to_scope.place(x=669, y=620, height=25, width=25)
update_button.place(x=719, y=620, height=25, width=62)
save_button.place(x=784, y=620, height=25, width=42)
exit_button.place(x=828, y=620, height=25, width=42)

mainloop()
