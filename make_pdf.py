"""
Generate the project guide PDF.
Run:  source venv/bin/activate && python make_pdf.py
Output: Student_Management_System_Guide.pdf
"""

from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Student Management System - DBMS Mini Project", align="R")
        self.ln(4)
        self.set_draw_color(41, 128, 185)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, title)
        self.ln(8)
        self.set_draw_color(41, 128, 185)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(6)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(52, 73, 94)
        self.cell(0, 8, title)
        self.ln(7)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(50, 50, 50)
        self.cell(8)
        self.cell(5, 6, "-")
        self.multi_cell(0, 6, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 10)
        self.set_fill_color(236, 240, 241)
        self.set_text_color(44, 62, 80)
        x = self.get_x()
        self.set_x(x + 5)
        self.multi_cell(180, 5.5, text, fill=True)
        self.ln(4)

    def table_row(self, cells, header=False):
        self.set_font("Helvetica", "B" if header else "", 10)
        if header:
            self.set_fill_color(44, 62, 80)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(245, 245, 245)
            self.set_text_color(50, 50, 50)
        col_w = 190 / len(cells)
        for c in cells:
            self.cell(col_w, 8, str(c), border=1, fill=True, align="C")
        self.ln()


# ======================================
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)


# -- COVER PAGE --
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 32)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 15, "Student Management System", align="C")
pdf.ln(18)
pdf.set_font("Helvetica", "", 18)
pdf.set_text_color(41, 128, 185)
pdf.cell(0, 10, "DBMS Mini Project - Complete Guide", align="C")
pdf.ln(15)
pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Technologies: Python 3  |  SQLite  |  Tkinter", align="C")
pdf.ln(8)
pdf.cell(0, 8, "Subject: Database Management System (DBMS)", align="C")
pdf.ln(30)

pdf.set_draw_color(41, 128, 185)
pdf.set_line_width(1)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(15)
pdf.set_font("Helvetica", "I", 11)
pdf.set_text_color(130, 130, 130)
pdf.cell(0, 7, "This document explains the project working, application flow,", align="C")
pdf.ln(7)
pdf.cell(0, 7, "database design, code structure, and presentation tips.", align="C")


# -- 1. PROJECT OVERVIEW --
pdf.add_page()
pdf.section_title("1. Project Overview")
pdf.body_text(
    "The Student Management System is a DBMS mini project that lets users "
    "manage student records using a SQLite database. It supports all CRUD operations "
    "(Create, Read, Update, Delete) and is built in two versions:"
)
pdf.bullet("Terminal Version - runs in the command line with a text menu.")
pdf.bullet("GUI Version - a Tkinter-based graphical window with forms and buttons.")
pdf.ln(3)
pdf.body_text(
    "The project uses only Python's standard library (sqlite3 and tkinter), "
    "meaning zero external dependencies are required to run it."
)

pdf.ln(4)
pdf.sub_title("Project Files")
pdf.code_block(
    "StudentManagementSystem/\n"
    "+-- student_terminal.py      Terminal-based app (~114 lines)\n"
    "+-- student_gui.py           GUI-based app (~180 lines)\n"
    "+-- Dockerfile               Docker container for terminal version\n"
    "+-- README.md                Run instructions\n"
    "+-- students.db              SQLite database (auto-created)"
)


# -- 2. DATABASE DESIGN --
pdf.add_page()
pdf.section_title("2. Database Design")

pdf.sub_title("Database File")
pdf.body_text("Name: students.db (SQLite file-based database, auto-created on first run)")

pdf.sub_title("Table: student")
pdf.table_row(["Column", "Data Type", "Constraint"], header=True)
pdf.table_row(["roll", "INTEGER", "PRIMARY KEY"])
pdf.table_row(["name", "TEXT", "NOT NULL"])
pdf.table_row(["course", "TEXT", "NOT NULL"])
pdf.table_row(["sem", "INTEGER", "NOT NULL"])
pdf.table_row(["mobile", "TEXT", "NOT NULL"])
pdf.table_row(["marks", "REAL", "NOT NULL"])

pdf.ln(5)
pdf.sub_title("CREATE TABLE Query")
pdf.code_block(
    "CREATE TABLE IF NOT EXISTS student (\n"
    "    roll    INTEGER PRIMARY KEY,\n"
    "    name    TEXT NOT NULL,\n"
    "    course  TEXT NOT NULL,\n"
    "    sem     INTEGER NOT NULL,\n"
    "    mobile  TEXT NOT NULL,\n"
    "    marks   REAL NOT NULL\n"
    ");"
)

pdf.sub_title("Why SQLite?")
pdf.bullet("No server setup needed - it is a single file (students.db).")
pdf.bullet("Built into Python - import sqlite3 works out of the box.")
pdf.bullet("Data persists after closing the application.")
pdf.bullet("Perfect for small-scale projects and learning DBMS concepts.")


# -- 3. SQL QUERIES EXPLAINED --
pdf.add_page()
pdf.section_title("3. SQL Queries Used")

queries = [
    ("INSERT (Add Student)",
     "INSERT INTO student VALUES (?, ?, ?, ?, ?, ?)",
     "Inserts a new row with roll, name, course, semester, mobile, and marks. "
     "The '?' are placeholders filled by Python to prevent SQL injection."),

    ("SELECT ALL (View Students)",
     "SELECT * FROM student",
     "Fetches every row from the student table. The '*' means all columns."),

    ("SELECT WHERE (Search Student)",
     "SELECT * FROM student WHERE roll = ?",
     "Finds one specific student by their roll number (Primary Key lookup)."),

    ("UPDATE (Update Student)",
     "UPDATE student SET name=?, course=?, sem=?, mobile=?, marks=?\nWHERE roll=?",
     "Modifies an existing record. The WHERE clause ensures only the matching "
     "roll number is updated, not the entire table."),

    ("DELETE (Delete Student)",
     "DELETE FROM student WHERE roll = ?",
     "Removes one student record from the database permanently."),
]

for title, sql, explanation in queries:
    pdf.sub_title(title)
    pdf.code_block(sql)
    pdf.body_text(explanation)
    pdf.ln(1)


# -- 4. APPLICATION FLOW --
pdf.add_page()
pdf.section_title("4. Application Flow (Step-by-Step)")

steps = [
    "Application Starts\n"
    "Python connects to SQLite database file (students.db). If the file does not "
    "exist, SQLite creates it automatically.",

    "Table Creation\n"
    "The CREATE TABLE IF NOT EXISTS query runs. If the table already exists, "
    "this step is skipped - so your old data is preserved.",

    "User Interface Loads\n"
    "Terminal version: A numbered menu (1-6) is displayed.\n"
    "GUI version: The Tkinter window opens with form fields and buttons.",

    "User Performs an Action\n"
    "The user chooses Add/View/Search/Update/Delete. Each action maps to a "
    "specific SQL query that is executed on the database.",

    "Database is Updated\n"
    "After INSERT, UPDATE, or DELETE, conn.commit() saves changes permanently. "
    "For SELECT, the results are fetched and displayed.",

    "Results are Displayed\n"
    "Terminal: Printed as formatted text in the console.\n"
    "GUI: Shown in the Treeview table widget and via message boxes.",

    "Loop or Exit\n"
    "The menu repeats until the user chooses Exit (option 6). On exit, "
    "the database connection is closed with conn.close().",
]

for i, step in enumerate(steps, 1):
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(10, 7, f"{i}.")
    lines = step.split("\n", 1)
    pdf.cell(0, 7, lines[0])
    pdf.ln(7)
    if len(lines) > 1:
        pdf.body_text(lines[1])
    pdf.ln(2)


# -- 5. TERMINAL VERSION EXPLAINED --
pdf.add_page()
pdf.section_title("5. Terminal Version - How It Works")

pdf.body_text("File: student_terminal.py (114 lines)")
pdf.ln(2)

pdf.sub_title("Menu Structure")
pdf.code_block(
    "========================================\n"
    "  STUDENT MANAGEMENT SYSTEM (Terminal)\n"
    "========================================\n"
    "1. Add Student\n"
    "2. View All Students\n"
    "3. Search Student\n"
    "4. Update Student\n"
    "5. Delete Student\n"
    "6. Exit\n"
    "Enter choice (1-6): _"
)

pdf.body_text(
    "The program runs in a while True loop. It prints the menu, takes user input, "
    "and calls the matching function. Each function uses input() to get the student "
    "details and then runs the SQL query."
)

pdf.sub_title("Key Functions")
pdf.bullet("add_student() - Prompts for 6 fields, runs INSERT, handles duplicate roll no.")
pdf.bullet("view_students() - Runs SELECT *, prints a formatted table with headers.")
pdf.bullet("search_student() - Takes roll number, runs SELECT WHERE, shows result.")
pdf.bullet("update_student() - First checks if student exists, then takes new values, runs UPDATE.")
pdf.bullet("delete_student() - Runs DELETE, checks cursor.rowcount to confirm deletion.")

pdf.ln(3)
pdf.sub_title("How to Run")
pdf.code_block("python student_terminal.py")


# -- 6. GUI VERSION EXPLAINED --
pdf.add_page()
pdf.section_title("6. GUI Version - How It Works")

pdf.body_text("File: student_gui.py (~180 lines)")
pdf.ln(2)

pdf.sub_title("Window Layout")
pdf.bullet("Header Bar - Dark bar at the top with the project title.")
pdf.bullet("Left Panel - LabelFrame with 6 input fields (Roll No, Name, Course, Semester, Mobile, Marks).")
pdf.bullet("Buttons - Color-coded: Add (green), Search (purple), Update (blue), Delete (red), Clear (gray).")
pdf.bullet("Right Panel - Treeview table displaying all student records with a scrollbar.")
pdf.bullet("Status Bar - Bottom bar showing total record count.")

pdf.ln(3)
pdf.sub_title("GUI Interactions")
pdf.bullet("Fill the form and click Add to insert a new student.")
pdf.bullet("Enter Roll No and click Search to auto-fill the form with that student's data.")
pdf.bullet("Modify form fields and click Update to save changes.")
pdf.bullet("Click Delete - a confirmation dialog appears before removing the record.")
pdf.bullet("Click any row in the table - the form auto-fills with that row's data for editing.")
pdf.bullet("Click Clear to empty all form fields.")

pdf.ln(3)
pdf.sub_title("How to Run")
pdf.code_block("python student_gui.py")


# -- 7. DOCKER SUPPORT --
pdf.add_page()
pdf.section_title("7. Docker Support")

pdf.body_text(
    "A Dockerfile is included to run the terminal version inside a Docker container. "
    "This demonstrates deployment/portability of the project."
)

pdf.sub_title("Dockerfile Contents")
pdf.code_block(
    'FROM python:3.11-slim\n\n'
    'WORKDIR /app\n'
    'COPY student_terminal.py .\n\n'
    'CMD ["python", "-u", "student_terminal.py"]'
)

pdf.sub_title("Commands")
pdf.code_block("docker build -t student-sms .\ndocker run -it student-sms")

pdf.body_text(
    "No extra dependencies are downloaded - python:3.11-slim already includes sqlite3. "
    "The GUI version cannot run in Docker because containers do not have a display server."
)


# -- 8. PRESENTATION TIPS --
pdf.add_page()
pdf.section_title("8. How to Present This Project")

pdf.sub_title("Before the Presentation")
pdf.bullet("Run student_gui.py once and add 2-3 sample student records so the table is not empty.")
pdf.bullet("Open the PPT file (Student_Management_System_PPT.pptx) and add your name/college on slide 1.")
pdf.bullet("Keep both the PPT and the code files ready to switch between during the demo.")

pdf.ln(3)
pdf.sub_title("Slide-by-Slide Script")

script = [
    ("Slide 1 - Title",
     "Introduce yourself. Say: 'My project is a Student Management System, "
     "built using Python, SQLite, and Tkinter as a DBMS mini project.'"),

    ("Slide 2 - Introduction",
     "Briefly explain: 'It allows adding, viewing, searching, updating, and "
     "deleting student records. Data is saved in an SQLite database.'"),

    ("Slide 3 - Technologies",
     "Point to each card: 'Python is the backend language, SQLite is the "
     "database, Tkinter is for the GUI, and we use standard SQL queries.'"),

    ("Slide 4 - Features",
     "Quickly read through the 6 features. Emphasize these are CRUD operations."),

    ("Slide 5 - Database Design",
     "Show the table schema. Mention 'Roll number is the Primary Key and "
     "all fields are NOT NULL.' This is a key DBMS concept."),

    ("Slide 6 - SQL Queries",
     "Point to each query. Say: 'We use parameterized queries with ? "
     "placeholders to prevent SQL injection.'"),

    ("Slides 7-8 - Two Versions",
     "Briefly mention both versions exist. Then SWITCH TO LIVE DEMO."),

    ("LIVE DEMO (most important!)",
     "Open the terminal, run python student_gui.py. Add a student, search by "
     "roll number, update the name, delete a record. Show the table updates "
     "in real-time. This is what impresses teachers the most."),

    ("Slides 9-11 - Flow, Docker, Structure",
     "Quickly cover these. Mention Docker as a bonus feature."),

    ("Slide 12-13 - Conclusion and Thank You",
     "Summarize: 'The project demonstrates complete CRUD operations with "
     "SQL, Python-database connectivity, and GUI development.' Ask for questions."),
]

for title, tip in script:
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 7, title)
    pdf.ln(7)
    pdf.body_text(tip)
    pdf.ln(1)


# -- 9. COMMON QUESTIONS --
pdf.add_page()
pdf.section_title("9. Questions Your Teacher May Ask")

qna = [
    ("Q: Why did you use SQLite instead of MySQL?",
     "A: SQLite is file-based and needs no server setup. It is built into Python's "
     "standard library, making it ideal for a mini project. For larger systems, "
     "MySQL or PostgreSQL would be better."),

    ("Q: What is a Primary Key?",
     "A: A Primary Key uniquely identifies each record. In our table, 'roll' is "
     "the primary key - no two students can have the same roll number."),

    ("Q: What are parameterized queries?",
     "A: Instead of inserting values directly into SQL strings, we use ? placeholders. "
     "Python fills in the values safely, preventing SQL injection attacks."),

    ("Q: What does conn.commit() do?",
     "A: It saves (commits) the changes to the database permanently. Without it, "
     "INSERT/UPDATE/DELETE operations would be lost when the program closes."),

    ("Q: What does CREATE TABLE IF NOT EXISTS do?",
     "A: It creates the table only if it does not already exist. This prevents "
     "errors when running the program multiple times - your old data is safe."),

    ("Q: Can this project handle multiple users?",
     "A: No, SQLite is single-user. For multi-user access, we would need MySQL/PostgreSQL "
     "with a client-server architecture."),

    ("Q: What is Tkinter?",
     "A: Tkinter is Python's built-in GUI library. It provides widgets like "
     "buttons, labels, text fields, and tables to build desktop applications."),
]

for q, a in qna:
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 7, q)
    pdf.ln(7)
    pdf.body_text(a)
    pdf.ln(2)


# -- SAVE --
output = "Student_Management_System_Guide.pdf"
pdf.output(output)
print(f"PDF saved: {output}")
print(f"Total pages: {pdf.pages_count}")
