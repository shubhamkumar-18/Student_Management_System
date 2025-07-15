import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------- DATABASE SETUP ----------
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shubh@123",
    )
    return connection


def setup_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
    connection.database = "student_management"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student_Record (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Roll_number VARCHAR(20) UNIQUE,
            Grade VARCHAR(10),
            Phone VARCHAR(20)
        )
    """)
    connection.commit()
    return connection


mydb = setup_database()
mycursor = mydb.cursor()


# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Student Records")
root.geometry("800x600")
root.configure(bg="#f7f7f7")


# ---------- STYLING ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#fefefe", foreground="#333", rowheight=30,
                fieldbackground="#fefefe", font=('Arial', 12))
style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
style.map("Treeview", background=[("selected", "#adcbe3")])

# ---------- TREEVIEW ----------
columns = ("ID", "Name", "Roll_number", "Grade", "Phone")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col, anchor=tk.CENTER)
    tree.column(col, width=140, anchor=tk.CENTER)

tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)


# ---------- FUNCTIONS ----------
def load_data():
    tree.delete(*tree.get_children())
    mycursor.execute("SELECT * FROM Student_Record ORDER BY Name ASC")
    students = mycursor.fetchall()
    for index, student in enumerate(students, start=1):
        student_with_serial = (index, *student[1:])
        tree.insert("", "end", values=student_with_serial)


def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    grade = grade_entry.get().strip()
    phone = phone_entry.get().strip()

    if not all([name, roll, grade, phone]):
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        sql = "INSERT INTO Student_Record (Name, Roll_number, Grade, Phone) VALUES (%s, %s, %s, %s)"
        val = (name, roll, grade, phone)
        mycursor.execute(sql, val)
        mydb.commit()
        load_data()
        clear_fields()
        messagebox.showinfo("Success", "Student added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error adding student: {err}")


def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected.")
        return

    roll_number = tree.item(selected_item[0])['values'][2]
    try:
        sql = "DELETE FROM Student_Record WHERE Roll_number = %s"
        val = (roll_number,)
        mycursor.execute(sql, val)
        mydb.commit()
        load_data()
        messagebox.showinfo("Success", "Student deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error deleting student: {err}")


def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


# ---------- INPUT FORM ----------
form_frame = tk.Frame(root, bg="#f7f7f7")
form_frame.pack(pady=20)

label_font = ("Arial", 12)
entry_font = ("Arial", 12)

tk.Label(form_frame, text="Name:", font=label_font, bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(form_frame, width=20, font=entry_font)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(form_frame, text="Roll Number:", font=label_font, bg="#f7f7f7").grid(row=0, column=2, padx=10, pady=10, sticky="e")
roll_entry = tk.Entry(form_frame, width=20, font=entry_font)
roll_entry.grid(row=0, column=3, padx=10, pady=10)

tk.Label(form_frame, text="Grade:", font=label_font, bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=10, sticky="e")
grade_entry = tk.Entry(form_frame, width=20, font=entry_font)
grade_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(form_frame, text="Phone:", font=label_font, bg="#f7f7f7").grid(row=1, column=2, padx=10, pady=10, sticky="e")
phone_entry = tk.Entry(form_frame, width=20, font=entry_font)
phone_entry.grid(row=1, column=3, padx=10, pady=10)


# ---------- BUTTONS ----------
button_frame = tk.Frame(root, bg="#f7f7f7")
button_frame.pack(pady=20)

btn_style = {"font": ("Arial", 12, "bold"), "padx": 20, "pady": 10, "bd": 0, "width": 12}

add_btn = tk.Button(button_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white", **btn_style)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = tk.Button(button_frame, text="Delete Student", command=delete_student, bg="#d9534f", fg="white", **btn_style)
delete_btn.grid(row=0, column=1, padx=10)

refresh_btn = tk.Button(button_frame, text="Refresh", command=load_data, bg="#5c8a8a", fg="white", **btn_style)
refresh_btn.grid(row=0, column=2, padx=10)


# ---------- INITIAL DATA LOAD ----------
load_data()


# ---------- MAIN LOOP ----------
root.mainloop()
