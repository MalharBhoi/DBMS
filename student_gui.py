import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# ─── Database Setup ───
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        roll    INTEGER PRIMARY KEY,
        name    TEXT NOT NULL,
        course  TEXT NOT NULL,
        sem     INTEGER NOT NULL,
        mobile  TEXT NOT NULL,
        marks   REAL NOT NULL
    )
""")
conn.commit()

# ─── Window ───
root = Tk()
root.title("Student Management System ~ DBMS Mini Project")
root.geometry("920x560")
root.resizable(False, False)
root.configure(bg="#f0f4f8")

# ─── Fonts & Colors ───
TITLE_FONT  = ("Helvetica", 16, "bold")
LABEL_FONT  = ("Segoe UI", 10)
ENTRY_FONT  = ("Segoe UI", 10)
BTN_FONT    = ("Segoe UI", 9, "bold")
HEADER_BG   = "#2c3e50"
HEADER_FG   = "#ecf0f1"
FORM_BG     = "#ffffff"
BTN_ADD     = "#27ae60"
BTN_UPDATE  = "#2980b9"
BTN_DELETE  = "#c0392b"
BTN_SEARCH  = "#8e44ad"
BTN_CLEAR   = "#7f8c8d"
BTN_FG      = "#ffffff"
BG_COLOR    = "#f0f4f8"

# ─── Variables ───
v_roll   = StringVar()
v_name   = StringVar()
v_course = StringVar()
v_sem    = StringVar()
v_mobile = StringVar()
v_marks  = StringVar()

# ─── Functions ───
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM student")
    for r in cursor.fetchall():
        tree.insert("", END, values=r)
    update_status()

def update_status():
    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0]
    status_var.set(f"  Total Records: {count}")

def clear_fields():
    for v in (v_roll, v_name, v_course, v_sem, v_mobile, v_marks):
        v.set("")

def add_student():
    if not v_roll.get() or not v_name.get():
        messagebox.showwarning("Warning", "Roll No and Name are required!")
        return
    try:
        cursor.execute(
            "INSERT INTO student VALUES (?, ?, ?, ?, ?, ?)",
            (int(v_roll.get()), v_name.get().strip(), v_course.get().strip(),
             int(v_sem.get()), v_mobile.get().strip(), float(v_marks.get())),
        )
        conn.commit()
        messagebox.showinfo("Done", "Student record added successfully!")
        clear_fields()
        refresh_table()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This Roll Number already exists in database!")
    except ValueError:
        messagebox.showerror("Error", "Check your inputs!\nRoll, Semester = numbers\nMarks = decimal allowed")

def search_student():
    if not v_roll.get():
        messagebox.showwarning("Warning", "Enter Roll Number to search!")
        return
    try:
        cursor.execute("SELECT * FROM student WHERE roll = ?", (int(v_roll.get()),))
        row = cursor.fetchone()
        if row:
            v_name.set(row[1]); v_course.set(row[2]); v_sem.set(row[3])
            v_mobile.set(row[4]); v_marks.set(row[5])
        else:
            messagebox.showinfo("Not Found", "No student found with that Roll Number.")
    except ValueError:
        messagebox.showerror("Error", "Roll Number should be a number!")

def update_student():
    if not v_roll.get() or not v_name.get():
        messagebox.showwarning("Warning", "Fill all the fields first!")
        return
    try:
        cursor.execute(
            "UPDATE student SET name=?, course=?, sem=?, mobile=?, marks=? WHERE roll=?",
            (v_name.get().strip(), v_course.get().strip(), int(v_sem.get()),
             v_mobile.get().strip(), float(v_marks.get()), int(v_roll.get())),
        )
        conn.commit()
        if cursor.rowcount:
            messagebox.showinfo("Done", "Record updated successfully!")
            clear_fields()
            refresh_table()
        else:
            messagebox.showinfo("Not Found", "No record with that Roll Number!")
    except ValueError:
        messagebox.showerror("Error", "Please check your inputs and try again.")

def delete_student():
    if not v_roll.get():
        messagebox.showwarning("Warning", "Enter Roll Number to delete!")
        return
    confirm = messagebox.askyesno("Confirm", f"Delete student with Roll No {v_roll.get()}?")
    if not confirm:
        return
    try:
        cursor.execute("DELETE FROM student WHERE roll = ?", (int(v_roll.get()),))
        conn.commit()
        if cursor.rowcount:
            messagebox.showinfo("Done", "Record deleted.")
            clear_fields()
            refresh_table()
        else:
            messagebox.showinfo("Not Found", "No record with that Roll Number!")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid Roll Number!")

def on_tree_select(event):
    selected = tree.focus()
    if selected:
        vals = tree.item(selected, "values")
        v_roll.set(vals[0]); v_name.set(vals[1]); v_course.set(vals[2])
        v_sem.set(vals[3]); v_mobile.set(vals[4]); v_marks.set(vals[5])


# ═══════════════════════════════════════
#   HEADER
# ═══════════════════════════════════════
header = Frame(root, bg=HEADER_BG, height=50)
header.pack(fill=X, side=TOP)
Label(header, text="📚 Student Management System", font=TITLE_FONT,
      bg=HEADER_BG, fg=HEADER_FG).pack(pady=12)

# ═══════════════════════════════════════
#   MAIN CONTENT AREA
# ═══════════════════════════════════════
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

# ─── Left Side: Form ───
left = Frame(main_frame, bg=BG_COLOR)
left.pack(side=LEFT, fill=Y, padx=(5, 10), pady=5)

form = LabelFrame(left, text=" Enter Student Details ", font=("Segoe UI", 10, "bold"),
                  bg=FORM_BG, fg="#2c3e50", padx=15, pady=12, bd=2, relief=GROOVE)
form.pack(fill=X)

field_labels = ["Roll No", "Name", "Course / Branch", "Semester", "Mobile No", "Marks"]
field_vars   = [v_roll, v_name, v_course, v_sem, v_mobile, v_marks]
for i, (lbl, var) in enumerate(zip(field_labels, field_vars)):
    Label(form, text=lbl + " :", font=LABEL_FONT, bg=FORM_BG, anchor=W).grid(
        row=i, column=0, sticky=W, pady=6)
    e = Entry(form, textvariable=var, font=ENTRY_FONT, width=22, bd=1, relief=SOLID)
    e.grid(row=i, column=1, pady=6, padx=(12, 0))

# ─── Buttons ───
btn_box = LabelFrame(left, text=" Actions ", font=("Segoe UI", 10, "bold"),
                     bg=FORM_BG, fg="#2c3e50", padx=8, pady=10, bd=2, relief=GROOVE)
btn_box.pack(fill=X, pady=(10, 0))

btn_data = [
    ("Add",    BTN_ADD,    add_student),
    ("Search", BTN_SEARCH, search_student),
    ("Update", BTN_UPDATE, update_student),
    ("Delete", BTN_DELETE, delete_student),
    ("Clear",  BTN_CLEAR,  clear_fields),
]
for i, (txt, color, cmd) in enumerate(btn_data):
    row_n = i // 3
    col_n = i % 3
    Button(btn_box, text=txt, command=cmd, font=BTN_FONT,
           bg=color, fg=BTN_FG, activebackground=color,
           width=9, cursor="hand2", bd=0, pady=4).grid(
        row=row_n, column=col_n, padx=4, pady=4)

# ─── Right Side: Table ───
right = Frame(main_frame, bg=BG_COLOR)
right.pack(side=RIGHT, fill=BOTH, expand=True, pady=5, padx=(0, 5))

table_label = Label(right, text="Student Records", font=("Segoe UI", 11, "bold"),
                    bg=BG_COLOR, fg="#2c3e50", anchor=W)
table_label.pack(anchor=W, pady=(0, 4))

# Style the treeview
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#ffffff",
                foreground="#2c3e50",
                rowheight=26,
                fieldbackground="#ffffff",
                font=("Segoe UI", 9))
style.configure("Treeview.Heading",
                background="#34495e",
                foreground="#ffffff",
                font=("Segoe UI", 9, "bold"))
style.map("Treeview", background=[("selected", "#3498db")])

tree_frame = Frame(right, bg=BG_COLOR)
tree_frame.pack(fill=BOTH, expand=True)

cols = ("Roll", "Name", "Course", "Sem", "Mobile", "Marks")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=16)
widths = [55, 120, 100, 45, 100, 55]
for c, w in zip(cols, widths):
    tree.heading(c, text=c)
    tree.column(c, width=w, anchor=CENTER)

scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# ═══════════════════════════════════════
#   STATUS BAR
# ═══════════════════════════════════════
status_var = StringVar()
status_bar = Label(root, textvariable=status_var, font=("Segoe UI", 9),
                   bg="#2c3e50", fg="#ecf0f1", anchor=W, padx=8)
status_bar.pack(fill=X, side=BOTTOM)

refresh_table()
root.mainloop()
conn.close()
