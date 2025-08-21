# Import modules for GUI, clipboard, randomization, and JSON file handling
from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

# Constants for UI configuration
DEFAULT_GEOMETRY = "410x470"
FONT_NAME = "Courier"
BLUE = "#19A2D7"

# All possible characters for password generation
CHARACTERS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}:;'\"<>,.?/"

# ---------------------------- PASSWORD COUNT ---------------- #
def count_passwords():
    """Return the number of saved passwords in data.json"""
    file_name = "data.json"
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return str(len(data))
    except FileNotFoundError:
        return "0"

# ---------------------------- PASSWORD GENERATOR ---------------- #
def generate_password():
    """Generate a random 16-character password, display it, and copy to clipboard"""
    new_password = ""
    for i in range(16):
        random_character = random.choice(CHARACTERS)
        new_password += random_character
    password_input_field.delete(0, END)
    password_input_field.insert(0, new_password)
    pyperclip.copy(new_password)
    messagebox.showinfo(title="Password Generated", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ---------------- #
def save_credentials():
    """Validate input and save credentials to data.json, notify if new or updated."""
    website = website_input_field.get()
    email = email_input_field.get()
    password = password_input_field.get()
    if len(website) == 0:
        messagebox.showerror(title="Error", message="Website cannot be empty!")
    elif len(email) == 0:
        messagebox.showerror(title="Error", message="Username cannot be empty!")
    elif len(password) == 0:
        messagebox.showerror(title="Error", message="Password cannot be empty!")
    else:
        file_name = "data.json"
        new_entry = {
            website: {
                "Email": email,
                "Password": password
            }
        }
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        is_update = website in data  # Check if website already exists

        data.update(new_entry)
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        website_input_field.delete(0, END)
        email_input_field.delete(0, END)
        password_input_field.delete(0, END)
        website_input_field.focus()
        count_passwords_label.config(text=f"Passwords saved ({count_passwords()})")
        if is_update:
            messagebox.showinfo(title="Updated", message=f"{website} credential updated!")
        else:
            messagebox.showinfo(title="Success", message="New credential saved!")

# ---------------------------- SEARCH PASSWORD ---------------- #
def search_creddentials():
    """Search for credentials by website name and display them"""
    search_website = website_input_field.get()
    file_name = "data.json"
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
        if len(search_website) == 0:
            messagebox.showerror(title="Error", message="Please enter a website")
        else:
            for website in data:
                if search_website not in data.keys():
                    messagebox.showerror(title="Error", message="Website not found")
                    break
                elif search_website == website:
                    username = data[website]["Email"]
                    password = data[website]["Password"]
                    messagebox.showinfo(title="Success!", message=f"Credentials found for: {website}\nUsername: {username}\nPassword : {password}")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Website not found")

# ---------------------------- UI SETUP ---------------- #
window = Tk()
window.title("Lazy Password Manager")
window.geometry(DEFAULT_GEOMETRY)
window.minsize(width=410, height=470)
window.maxsize(width=410, height=470)
window.config(padx=10, pady=10)

# Canvas for logo image
bg_image = PhotoImage(file="logo.png")
canvas = Canvas(window, highlightthickness=0, bg=BLUE)
image_id = canvas.create_image(0, 0, image=bg_image)

def center_image(event):
    """Center the logo image on window resize"""
    canvas.coords(image_id, event.width / 2, event.height / 2)

canvas.bind("<Configure>", center_image)
canvas.grid(column=0, row=0, columnspan=3, pady=30)

# Website input
website_label = Label(text="Website  ", font=(FONT_NAME, 12, "bold"))
website_label.grid(column=0, row=1, sticky="e", padx=(2, 0))
website_input_field = Entry(width=35)
website_input_field.grid(column=1, row=1, sticky="w")
website_input_field.focus()

# Username input
email_label = Label(text="Username ", font=(FONT_NAME, 12, "bold"))
email_label.grid(column=0, row=2, sticky="e", padx=(2, 0))
email_input_field = Entry(width=35)
email_input_field.grid(column=1, row=2, sticky="w")

# Password input
password_label = Label(text="Password ", font=(FONT_NAME, 12, "bold"))
password_label.grid(column=0, row=3, sticky="e", padx=(2, 0))
password_input_field = Entry(width=35)
password_input_field.grid(column=1, row=3, sticky="w")

# Password count display
count_passwords_label = Label(text=f"Passwords saved ({count_passwords()})", font=(FONT_NAME, 12, "bold"))
count_passwords_label.grid(column=0, row=0, columnspan=3, sticky="n")

# Buttons
search_button = Button(text="Search", command=search_creddentials)
search_button.grid(column=2, row=1)
generate_password_button = Button(text="Generate\npassword", command=generate_password)
generate_password_button.config(height=2)
generate_password_button.grid(column=2, row=3, padx=10)
add_button = Button(text="Save credential", command=save_credentials)
add_button.grid(column=1, row=4, sticky="w")

# Start the GUI event loop
email_input_field = Entry(width=35)
email_input_field.grid(column=1, row=2, sticky="w")

# Create and position the password input section
password_label = Label(text="Password ", font=(FONT_NAME, 12, "bold"))
password_label.grid(column=0, row=3, sticky="e", padx=(2, 0))

password_input_field = Entry(width=35)
password_input_field.grid(column=1, row=3, sticky="w")

# Display how many passwords are currently saved
count_passwords_label = Label(text=f"Passwords saved ({count_passwords()})", font=(FONT_NAME, 12, "bold"))
count_passwords_label.grid(column=0, row=0, columnspan=3, sticky="n")

# Create buttons for generating passwords and saving data
search_button = Button(text="Search", command=search_creddentials)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate\npassword", command=generate_password)
generate_password_button.config(height=2)
generate_password_button.grid(column=2, row=3, padx=10)

add_button = Button(text="Save credential", command=save_credentials)
add_button.grid(column=1, row=4, sticky="w")

# Start the GUI event loop - keeps the window open and responsive
window.mainloop()
