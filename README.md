# Student Management System — DBMS Mini Project

## Run Locally

```bash
# Terminal version
python student_terminal.py

# GUI version
python student_gui.py
```

## Run with Docker (Terminal version)

```bash
docker build -t student-sms .
docker run -it student-sms
```

No extra dependencies needed — Python's standard library includes both `sqlite3` and `tkinter`.
