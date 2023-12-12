import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Operations
def create_connection():
    return sqlite3.connect('motorcycle_renting.db')

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_motorcycle_renting (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            motorcycle_name TEXT,
            price STRING NOT NULL
        )
    ''')
    conn.commit()

def create_renting(conn, student_name, motorcycle_name, price):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_motorcycle_renting (student_name, motorcycle_name, price)
        VALUES (?, ?, ?)
    ''', (student_name, motorcycle_name, price))
    conn.commit()

def read_renting(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM student_motorcycle_renting')
    return cursor.fetchall()

def update_renting(conn, student_id, new_price):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE student_motorcycle_renting
        SET price = ?
        WHERE student_id = ?
    ''', (new_price, student_id))
    conn.commit()

def delete_renting(conn, student_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM student_motorcycle_renting WHERE student_id = ?', (student_id,))
    conn.commit()

# GUI Functions
def create_renting_entry():
    student_name = student_name_entry.get()
    motorcycle_name = motorcycle_name_entry.get()
    price = price_entry.get()

    if student_name and motorcycle_name and price:
        create_renting(conn, student_name, motorcycle_name, price)
        messagebox.showinfo("Success", "Renting entry created successfully.")
        clear_entries()
        update_renting_listbox()
    else:
        messagebox.showerror("Error", "Please fill in all details.")

def read_renting_entries():
    entries = read_renting(conn)
    messagebox.showinfo("Renting Entries", entries)

def update_renting_entry():
    selected_index = renting_listbox.curselection()

    if selected_index:
        student_id = renting_listbox.get(selected_index)[0]
        new_price = new_price_entry.get()

        if new_price:
            update_renting(conn, student_id, new_price)
            messagebox.showinfo("Success", "Renting entry updated successfully.")
            update_renting_listbox()
        else:
            messagebox.showerror("Error", "Please enter a new price.")
    else:
        messagebox.showerror("Error", "Please select a renting entry.")

def delete_renting_entry():
    selected_index = renting_listbox.curselection()

    if selected_index:
        student_id = renting_listbox.get(selected_index)[0]
        delete_renting(conn, student_id)
        messagebox.showinfo("Success", "Renting entry deleted successfully.")
        update_renting_listbox()
    else:
        messagebox.showerror("Error", "Please select a renting entry.")

def clear_entries():
    student_name_entry.delete(0, tk.END)
    motorcycle_name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    new_price_entry.delete(0, tk.END)

def update_renting_listbox():
    renting_listbox.delete(0, tk.END)
    entries = read_renting(conn)
    for entry in entries:
        renting_listbox.insert(tk.END, entry)

# GUI
root = tk.Tk()
root.title("Motorcycle Rental System")

# Database Setup
conn = create_connection()
create_table(conn)

# Renting Entry
renting_label = tk.Label(root, text="Renting Entry:")
renting_label.grid(row=0, column=0, columnspan=2, pady=10)

student_name_label = tk.Label(root, text="Student Name:")
student_name_label.grid(row=1, column=0, pady=5)
student_name_entry = tk.Entry(root)
student_name_entry.grid(row=1, column=1, pady=5)

motorcycle_name_label = tk.Label(root, text="Motorcycle Name:")
motorcycle_name_label.grid(row=2, column=0, pady=5)
motorcycle_name_entry = tk.Entry(root)
motorcycle_name_entry.grid(row=2, column=1, pady=5)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=3, column=0, pady=5)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, pady=5)

create_button = tk.Button(root, text="Create Renting Entry", command=create_renting_entry)
create_button.grid(row=2, column=5, columnspan=2, pady=10)

# Renting Listbox
renting_listbox = tk.Listbox(root, height=5, width=50)
renting_listbox.grid(row=5, column=0, columnspan=2, pady=10)

# Buttons for Read, Update, and Delete
read_button = tk.Button(root, text="Read Renting Entries", command=read_renting_entries)
read_button.grid(row=3, column=5, columnspan=2, pady=5)

update_label = tk.Label(root, text="Update Renting Entry:")
update_label.grid(row=7, column=0, columnspan=2, pady=5)

new_price_label = tk.Label(root, text="New Price:")
new_price_label.grid(row=8, column=0, pady=5)
new_price_entry = tk.Entry(root)
new_price_entry.grid(row=8, column=1, pady=5)

update_button = tk.Button(root, text="Update Renting Entry", command=update_renting_entry)
update_button.grid(row=9, column=0, columnspan=2, pady=5)

delete_button = tk.Button(root, text="Delete Renting Entry", command=delete_renting_entry)
delete_button.grid(row=10, column=0, columnspan=2, pady=10)

# Clear Entries Button
clear_button = tk.Button(root, text="Clear Entries", command=clear_entries)
clear_button.grid(row=11, column=0, columnspan=2, pady=10)

# Initialize Renting Listbox
update_renting_listbox()

root.mainloop()