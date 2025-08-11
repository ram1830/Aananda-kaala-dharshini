import pyodbc
import tkinter as tk
from tkinter import messagebox

# SQL Server connection
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=SRIRAM\SQLEXPRESS;"
    "Database=UserAuthDB;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Register function
def register():
    user = entry_username.get()
    pwd = entry_password.get()

    if not user or not pwd:
        messagebox.showwarning("Input Error", "All fields required")
        return

    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", user, pwd)
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except pyodbc.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

# Login function
def login():
    user = entry_username.get()
    pwd = entry_password.get()

    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", user, pwd)
    row = cursor.fetchone()

    if row:
        messagebox.showinfo("Success", f"Welcome, {user}!")
    else:
        messagebox.showerror("Error", "Invalid username or password")

# GUI setup
root = tk.Tk()
root.title("Login & Register")
root.geometry("300x200")

tk.Label(root, text="Username").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=register).pack()

root.mainloop()
