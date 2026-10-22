import sqlite3

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


def add_student():
    roll   = int(input("Roll Number : "))
    name   = input("Name        : ")
    course = input("Course      : ")
    sem    = int(input("Semester    : "))
    mobile = input("Mobile      : ")
    marks  = float(input("Marks       : "))
    try:
        cursor.execute(
            "INSERT INTO student VALUES (?, ?, ?, ?, ?, ?)",
            (roll, name, course, sem, mobile, marks),
        )
        conn.commit()
        print("✅ Student added successfully.\n")
    except sqlite3.IntegrityError:
        print("❌ Roll number already exists.\n")


def view_students():
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    if not rows:
        print("No records found.\n")
        return
    print(f"{'Roll':<8}{'Name':<20}{'Course':<15}{'Sem':<6}{'Mobile':<15}{'Marks':<8}")
    print("-" * 72)
    for r in rows:
        print(f"{r[0]:<8}{r[1]:<20}{r[2]:<15}{r[3]:<6}{r[4]:<15}{r[5]:<8}")
    print()


def search_student():
    roll = int(input("Enter Roll Number to search: "))
    cursor.execute("SELECT * FROM student WHERE roll = ?", (roll,))
    row = cursor.fetchone()
    if row:
        print(f"Roll: {row[0]}, Name: {row[1]}, Course: {row[2]}, "
              f"Sem: {row[3]}, Mobile: {row[4]}, Marks: {row[5]}\n")
    else:
        print("❌ Student not found.\n")


def update_student():
    roll = int(input("Enter Roll Number to update: "))
    cursor.execute("SELECT * FROM student WHERE roll = ?", (roll,))
    if not cursor.fetchone():
        print("❌ Student not found.\n")
        return
    name   = input("New Name    : ")
    course = input("New Course  : ")
    sem    = int(input("New Semester: "))
    mobile = input("New Mobile  : ")
    marks  = float(input("New Marks   : "))
    cursor.execute(
        "UPDATE student SET name=?, course=?, sem=?, mobile=?, marks=? WHERE roll=?",
        (name, course, sem, mobile, marks, roll),
    )
    conn.commit()
    print("✅ Student updated successfully.\n")


def delete_student():
    roll = int(input("Enter Roll Number to delete: "))
    cursor.execute("DELETE FROM student WHERE roll = ?", (roll,))
    conn.commit()
    if cursor.rowcount:
        print("✅ Student deleted successfully.\n")
    else:
        print("❌ Student not found.\n")


# ─── Main Menu ───
while True:
    print("=" * 40)
    print("  STUDENT MANAGEMENT SYSTEM (Terminal)")
    print("=" * 40)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    choice = input("Enter choice (1-6): ")

    if   choice == "1": add_student()
    elif choice == "2": view_students()
    elif choice == "3": search_student()
    elif choice == "4": update_student()
    elif choice == "5": delete_student()
    elif choice == "6":
        conn.close()
        print("Goodbye! 👋")
        break
    else:
        print("Invalid choice. Try again.\n")
