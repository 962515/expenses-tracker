import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        description TEXT,
        category TEXT,
        price REAL
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a new expense
def add_expense(date, description, category, price):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)", (date, description, category, price))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense added successfully!")

# Function to view all expenses
def view_all_expenses():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    conn.close()
    return expenses

# Function to view monthly expenses by category
def view_monthly_expenses(month, year):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? GROUP BY category", (month, year))
    expenses = cur.fetchall()
    conn.close()
    return expenses

# Function to add a new expense from GUI
def submit_expense():
    date = date_entry.get()
    description = description_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    if date and description and category and price:
        add_expense(date, description, category, price)
        date_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Function to display all expenses in a new window
def display_all_expenses():
    expenses = view_all_expenses()
    view_window = tk.Toplevel(root)
    view_window.title("All Expenses")
    for idx, expense in enumerate(expenses):
        tk.Label(view_window, text=expense).grid(row=idx, column=0)

# Function to display monthly expenses in a new window
def display_monthly_expenses():
    month = month_entry.get()
    year = year_entry.get()
    expenses = view_monthly_expenses(month, year)
    view_window = tk.Toplevel(root)
    view_window.title("Monthly Expenses")
    for idx, expense in enumerate(expenses):
        tk.Label(view_window, text=f"Category: {expense[0]}, Total: {expense[1]}").grid(row=idx, column=0)

# Initialize the database
init_db()

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")

# Labels and Entries for adding new expense
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Description").grid(row=1, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1)

tk.Label(root, text="Category").grid(row=2, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1)

tk.Label(root, text="Price").grid(row=3, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1)

tk.Button(root, text="Add Expense", command=submit_expense).grid(row=4, column=1)

# Buttons to view expenses
tk.Button(root, text="View All Expenses", command=display_all_expenses).grid(row=5, column=0)
tk.Label(root, text="Month (MM)").grid(row=6, column=0)
month_entry = tk.Entry(root)
month_entry.grid(row=6, column=1)

tk.Label(root, text="Year (YYYY)").grid(row=7, column=0)
year_entry = tk.Entry(root)
year_entry.grid(row=7, column=1)

tk.Button(root, text="View Monthly Expenses", command=display_monthly_expenses).grid(row=8, column=1)

root.mainloop()
