from tkinter import filedialog, messagebox
from tkinter import *
import random


def sieve_of_eratosthenes(n):
    prime_numbers = [True for _ in range(n + 1)]
    num = 2
    while num * num <= n:
        if prime_numbers[num]:
            for i in range(num * num, n + 1, num):
                prime_numbers[i] = False
        num += 1
    return [p for p in range(2, n + 1) if prime_numbers[p]]


def is_prime(n):
    return n in sieve_of_eratosthenes(n)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_coprime(a, b):
    return gcd(a, b) == 1


def extended_euclid(a, b):
    if b == 0:
        return 1, 0
    else:
        s, t = extended_euclid(b, a % b)
        return t, s - (a // b) * t


def bin_pow(b, n, m):
    res = b
    for i in bin(n).replace('0b', '')[1:]:
        res = ((res ** 2) * (b ** int(i))) % m
    return res


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
                    file.write(f"({d}, {n})\n" + ", ".join(map(str, encrypted_indexes)))
                except NameError:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def encrypt():
        p_value_scope.delete("1.0", END)
        q_value_scope.delete("1.0", END)
        public_key_scope.delete("1.0", END)
        private_key_scope.delete("1.0", END)
        encrypted_indexes_scope.delete("1.0", END)
        text = input_scope.get("1.0", END).strip("\n ")
        global d, n, encrypted_indexes
        while True:
            p, q = random.getrandbits(16), random.getrandbits(16)
            if p != q and is_prime(p) and is_prime(q):
                break
        n = p * q
        phi_n = (p - 1) * (q - 1)

        while True:
            e = random.randint(2, phi_n)
            if is_coprime(e, phi_n):
                break

        d = extended_euclid(e, phi_n)[0]
        while d < 0:
            d += phi_n

        p_value_scope.insert(END, p)
        q_value_scope.insert(END, q)
        public_key_scope.insert(END, f"({e}, {n})")
        private_key_scope.insert(END, f"({d}, {n})")
        indexes = [ord(letter) for letter in text]
        encrypted_indexes = [bin_pow(i, e, n) for i in indexes]
        encrypted_indexes_scope.insert(END, ", ".join(map(str, encrypted_indexes)))

    e_window = Toplevel(window)
    e_window.geometry("520x390")
    e_window.title("RSA encryption")
    e_window.configure(background="#F1EBEB")
    Button(e_window, text="Open file", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", relief="groove",
           command=open_file).place(x=25, y=-4, height=26, width=80)
    Button(e_window, text="Save file", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", relief="groove",
           command=save_encrypted_file).place(x=105, y=-4, height=26, width=77)
    Button(e_window, text="Encrypt", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", borderwidth=2,
           relief="groove", command=encrypt).place(x=182, y=-4, height=26, width=74)
    Label(e_window, text="Message to encrypt", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=25,
                                                                                                               y=22)
    input_scope = Text(e_window, bg="#F8F8F8", fg="#BF8485", selectbackground="#BF8485", padx=4, pady=2,
                       font=("Cartograph CF", 10))
    Label(e_window, text="Prime p", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=264, y=22)
    p_value_scope = Text(e_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                         font=("Cartograph CF", 10))
    Label(e_window, text="Prime q", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=381, y=22)
    q_value_scope = Text(e_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                         font=("Cartograph CF", 10))
    Label(e_window, text="Public key (e, n)", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=264,
                                                                                                              y=70)
    public_key_scope = Text(e_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                            font=("Cartograph CF", 10))
    Label(e_window, text="Private key (d, n)", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=264,
                                                                                                               y=118)
    private_key_scope = Text(e_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                             font=("Cartograph CF", 10))
    Label(e_window, text="Encrypted indexes", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=264,
                                                                                                              y=166)
    encrypted_indexes_scope = Text(e_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                                   font=("Cartograph CF", 10))

    input_scope.place(x=25, y=45, height=320, width=231)
    p_value_scope.place(x=264, y=45, height=25, width=113)
    q_value_scope.place(x=381, y=45, height=25, width=114)
    public_key_scope.place(x=264, y=93, height=25, width=231)
    private_key_scope.place(x=264, y=141, height=25, width=231)
    encrypted_indexes_scope.place(x=264, y=189, height=176, width=231)


def text_decryptor():
    def open_encrypted_file():
        path = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*.txt"),))
        if path:
            with open(path, "r", encoding="utf-8-sig") as file:
                text = file.read().strip("\n ")
            private_key_scope.delete("1.0", END)
            encrypted_indexes_scope.delete("1.0", END)
            private_key_scope.insert(END, text.split("\n")[0])
            encrypted_indexes_scope.insert(END, text.split("\n")[1])

    def save_decrypted_file():
        path = filedialog.asksaveasfilename(title="Save file", filetypes=(("Text Files", "*.txt"),),
                                            defaultextension=(("Text Files", "*.txt"),))
        if path:
            with open(path, "w+", encoding="utf-8-sig") as file:
                try:
                    file.write(decrypted_message)
                except NameError:
                    messagebox.showinfo("Info", "Saved file is empty.")

    def decrypt():
        decrypted_indexes_scope.delete("1.0", END)
        decrypted_message_scope.delete("1.0", END)
        global decrypted_message
        if not private_key_scope.get("1.0", END).isspace() or len(private_key_scope.get("1.0", END)) == 0:
            d, n = map(int, private_key_scope.get("1.0", END).strip("\n ")[1:-1].split(", "))
            encrypted_indexes = map(int, encrypted_indexes_scope.get("1.0", END).strip("\n ").split(", "))
            decrypted_indexes = [bin_pow(i, d, n) for i in encrypted_indexes]
            decrypted_message = "".join(chr(i) for i in decrypted_indexes)
            decrypted_indexes_scope.insert(END, ", ".join(map(str, decrypted_indexes)))
            decrypted_message_scope.insert(END, decrypted_message)

    d_window = Toplevel(window)
    d_window.geometry("520x390")
    d_window.title("RSA decryption")
    d_window.configure(background="#F1EBEB")
    Button(d_window, text="Open file", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", relief="groove",
           command=open_encrypted_file).place(x=25, y=-4, height=26, width=80)
    Button(d_window, text="Save file", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", relief="groove",
           command=save_decrypted_file).place(x=105, y=-4, height=26, width=77)
    Button(d_window, text="Decrypt", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#445144", borderwidth=2,
           relief="groove", command=decrypt).place(x=182, y=-4, height=26, width=74)
    Label(d_window, text="Private key (d, n)", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=25,
                                                                                                               y=22)
    private_key_scope = Text(d_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                             font=("Cartograph CF", 10))
    Label(d_window, text="Encrypted indexes", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=25,
                                                                                                              y=70)
    encrypted_indexes_scope = Text(d_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                                   font=("Cartograph CF", 10))
    Label(d_window, text="Indexes for decryption", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=25,
                                                                                                                   y=217)
    decrypted_indexes_scope = Text(d_window, bg="#F8F8F8", fg="#AA7879", selectbackground="#AA7879", padx=4, pady=2,
                                   font=("Cartograph CF", 10))
    Label(d_window, text="Decrypted message", font=("GT Walsheim Pro", 12), bg="#F1EBEB", fg="#536353").place(x=264,
                                                                                                              y=22)
    decrypted_message_scope = Text(d_window, bg="#F8F8F8", fg="#BF8485", selectbackground="#BF8485", padx=4, pady=2,
                                   font=("Cartograph CF", 10))

    private_key_scope.place(x=25, y=45, height=25, width=231)
    encrypted_indexes_scope.place(x=25, y=93, height=124, width=231)
    decrypted_indexes_scope.place(x=25, y=240, height=125, width=231)
    decrypted_message_scope.place(x=264, y=45, height=320, width=231)


window = Tk()
window.geometry("220x165")
window.title("RSA")
window.configure(background="#F1EBEB")
Label(window, text="Open RSA", font=("GT Walsheim Pro Medium", 13), bg="#F1EBEB", fg="#445144").place(x=67, y=25)
Button(window, text="ENCRYPTION", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#AA7879", borderwidth=2,
       relief="groove", command=text_encryptor).place(x=52, y=52, height=28, width=115)
Button(window, text="DECRYPTION", font=("GT Walsheim Pro", 12), bg="#F6F2F2", fg="#AA7879", borderwidth=2,
       relief="groove", command=text_decryptor).place(x=52, y=85, height=28, width=115)

mainloop()
