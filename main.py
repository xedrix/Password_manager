import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle

import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_list = []
    password_list += (choice(letters) for _ in range(randint(8, 10)))
    password_list += (choice(symbols) for _ in range(randint(2, 4)))
    password_list += (choice(numbers) for _ in range(randint(2, 4)))
    shuffle(password_list)
    password = "".join(password_list)
    entry_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    if len(website) > 0 and len(username) > 0 and len(password) > 0:
        new_entry = {
            website: {
                "Username": username,
                "Password": password,
            }
        }
        try:
            with open("passwords.json", "r") as password_file:
                data = json.load(password_file)

        except FileNotFoundError:
            with open("passwords.json", "w") as password_file:
                json.dump(new_entry, password_file, indent=4)
        else:
            data.update(new_entry)
            with open("passwords.json", "w") as password_file:
                json.dump(data, password_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_username.delete(0, END)
            entry_password.delete(0, END)
    else:
        messagebox.showinfo(title="Oops", message="Please do not leave any empty fields!")


# ---------------------------- SEARCH CREDENTIALS ------------------------------- #
def search_account():
    website = entry_website.get()
    try:
        with open("passwords.json", "r") as password_file:
            passwords = json.load(password_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="You currently have no accounts being stored!")
    else:
        if website in passwords:
            username = passwords[website]["Username"]
            password = passwords[website]["Password"]
            messagebox.showinfo(title=website, message=f"Username: {username} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"You do not have credentials stored for {website}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

# Labels
label_website = Label(text="Website:", font=("Arial", 12))
label_website.grid(column=0, row=1)
label_username = Label(text="Email/Username:", font=("Arial", 12))
label_username.grid(column=0, row=2)
label_password = Label(text="Password:", font=("Arial", 12))
label_password.grid(column=0, row=3)

# Buttons
button_password = Button(text="Generate Password", command=generate_password, width=14)
button_password.grid(column=2, row=3)
button_add = Button(text="Add", command=save_password, width=43)
button_add.grid(column=1, row=4, columnspan=2)
button_search = Button(text="Search", command=search_account, width=14)
button_search.grid(column=2, row=1)

# Text boxes
entry_website = Entry(window, width=32)
entry_website.grid(column=1, row=1)
entry_website.focus()
entry_username = Entry(window, width=50)
entry_username.grid(column=1, row=2, columnspan=2)
entry_username.insert(0, "example@email.com")
entry_password = Entry(window, width=32, show="*")
entry_password.grid(column=1, row=3)

window.mainloop()
