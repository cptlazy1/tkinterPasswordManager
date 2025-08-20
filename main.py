# Import necessary modules for GUI, file operations, and data handling
from tkinter import *
from tkinter import messagebox
import os
import pandas as pd
import random
import string
import pyperclip
import json

# Constants - values that won't change during program execution
DEFAULT_GEOMETRY = "410x470"
FONT_NAME = "Courier"
BLUE = "#19A2D7"

# Create a string of all possible characters for password generation
# Includes letters (a-z, A-Z), numbers (0-9), and special symbols
CHARACTERS = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}:;'\"<>,.?/"

# ---------------------------- SHOW HOW MANY PASSWORDS ARE SAVED ---------------- #
def count_passwords():
    """Count how many passwords are stored in the JSON file"""
    file_name = "data.json"
    try:
        # Try to read the JSON file and count the entries
        with open(file_name, "r") as file:
            data = json.load(file)
            return str(len(data))
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist yet, return "0"
        return "0"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a random 16-character password and put it in the password field"""
    new_password = ""
    # Loop 16 times to create a 16-character password
    for i in range(16):
        # Pick a random character from our character list
        random_character = random.choice(CHARACTERS)
        new_password += random_character
    
    # Clear the password field and insert the new password
    password_input_field.delete(0, END)
    password_input_field.insert(0, new_password)
    
    # Copy the generated password to clipboard for easy pasting
    pyperclip.copy(new_password)
    # Show a message that password was copied
    messagebox.showinfo(title="Password Generated", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_credentials():
    """Get input from fields, validate them, and save credentials to JSON file"""
    # Get the text from each input field
    website = website_input_field.get()
    email = email_input_field.get()
    password = password_input_field.get()
    
    # Check if any field is empty and show error message
    if len(website) == 0:
        messagebox.showerror(title="Error", message="Website cannot be empty")
    elif len(email) == 0:
        messagebox.showerror(title="Error", message="Email cannot be empty")
    elif len(password) == 0:
        messagebox.showerror(title="Error", message="Password cannot be empty")
    else:
        # All fields have data, so save the credentials to JSON file
        file_name = "data.json"
        new_entry = {website: {
            "Email": email, 
            "Password": password
            }
        }
        try:
            # Try to read existing data from JSON file
            with open(file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is empty, start with empty dict
            data = {}
        # Update data with new entry and write back to JSON file
        data.update(new_entry)
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        # Clear all input fields after saving
        website_input_field.delete(0, END)
        email_input_field.delete(0, END)
        password_input_field.delete(0, END)
        # Put cursor back in website field for next entry
        website_input_field.focus()
        # Update the password counter display
        count_passwords_label.config(text=f"Passwords saved: {count_passwords()}")
        # Show success message
        messagebox.showinfo(title="Success", message="Credentials saved!")

# ---------------------------- UI SETUP ------------------------------- #
# Create the main window
window = Tk()
window.title("Lazy Password Manager")
window.geometry(DEFAULT_GEOMETRY)
window.minsize(width=410, height=470)
window.maxsize(width=410, height=470)
window.config(padx=10, pady=10)

# Create canvas for background image
bg_image = PhotoImage(file="logo.png")
canvas = Canvas(window, highlightthickness=0, bg=BLUE)
image_id = canvas.create_image(0, 0, image=bg_image)

def center_image(event):
    """Center the background image when window is resized"""
    canvas.coords(image_id, event.width / 2, event.height / 2)

# Bind the centering function to window resize events
canvas.bind("<Configure>", center_image)
canvas.grid(column=0, row=0, columnspan=3, pady=30)

# Create and position the website input section
website_label = Label(text="Website  ", font=(FONT_NAME, 12, "bold"))
website_label.grid(column=0, row=1, sticky="e", padx=(2, 0))
website_input_field = Entry(width=35)
website_input_field.grid(column=1, row=1, sticky="w")
website_input_field.focus()  # Start with cursor in this field

# Create and position the email input section
email_label = Label(text="Username ", 
               font=(FONT_NAME, 12, "bold"))
email_label.grid(column=0, row=2, sticky="e", padx=(2, 0))
email_input_field = Entry(width=35)
email_input_field.grid(column=1, row=2, sticky="w")

# Create and position the password input section
password_label = Label(text="Password ", font=(FONT_NAME, 12, "bold"))
password_label.grid(column=0, row=3, sticky="e", padx=(2, 0))
password_input_field = Entry(width=35)
password_input_field.grid(column=1, row=3, sticky="w")

# Display how many passwords are currently saved
count_passwords_label = Label(text=f"Passwords saved ({count_passwords()})", 
                              font=(FONT_NAME, 12, "bold"))
count_passwords_label.grid(column=0, row=0, columnspan=3, sticky="n")

# Create buttons for generating passwords and saving data
search_button = Button(text="Search")
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate\npassword", command=generate_password)
generate_password_button.config(height=2)
generate_password_button.grid(column=2, row=3, padx=10)

add_button = Button(text="Save credential", command=save_credentials)
add_button.grid(column=1, row=4, sticky="w")

# Start the GUI event loop - keeps the window open and responsive
window.mainloop()
