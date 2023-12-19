from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)

def call_key():
    return open("pass.key", "rb").read()

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("800x400")  # Set the initial window size

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
            
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Exposys Lab", font=controller.title_font, fg='red')
        label.pack(side="top", fill="x", pady=10)

        lbl_username = tk.Label(self, text="Username:", font=("Helvetica", 14))
        lbl_username.pack(pady=10)
        txtfld_username = tk.Entry(self, bd=5, font=("Helvetica", 14))
        txtfld_username.pack()

        lbl_password = tk.Label(self, text="Password:", font=("Helvetica", 14))
        lbl_password.pack(pady=10)
        txtfld_password = tk.Entry(self, show="*", bd=5, font=("Helvetica", 14))
        txtfld_password.pack()

        button_login = tk.Button(self, text="Login", command=lambda: [self.controller.show_frame("PageOne"), self.getvalue(txtfld_username, txtfld_password)])
        button_login.pack(pady=20)

    def getvalue(self, username_entry, password_entry):
        result1 = username_entry.get()
        result2 = password_entry.get()
        print("Username:", result1)
        print("Password:", result2)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Encrypt and Decrypt Messages", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button_login = tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("StartPage"))
        button_login.pack(padx=100, pady=10)

        label_encrypt = tk.Label(self, text="Enter text to encrypt:", font=("Helvetica", 14))
        label_encrypt.pack(pady=10)
        txtfld_encrypt = tk.Entry(self, bd=5, font=("Helvetica", 14), width=50)
        txtfld_encrypt.pack()

        button_encrypt = tk.Button(self, text="Encrypt", command=lambda: [self.encrypt_text(txtfld_encrypt, txtfld_decrypt)])
        button_encrypt.pack(pady=10)

        label_decrypt = tk.Label(self, text="Decrypted message:", font=("Helvetica", 14))
        label_decrypt.pack(pady=10)
        txtfld_decrypt = tk.Entry(self, bd=5, font=("Helvetica", 14), width=50)
        txtfld_decrypt.pack()

    def encrypt_text(self, encrypt_entry, decrypt_entry):
        result = encrypt_entry.get()
        genwrite_key()
        key = call_key()
        slogan = result.encode()
        a = Fernet(key)
        coded_slogan = a.encrypt(slogan)
        decrypt_entry.delete(0, "end")
        decrypt_entry.insert(tk.END, coded_slogan.decode())

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
