FROM python:3.11-slim

WORKDIR /app
COPY student_terminal.py .

CMD ["python", "-u", "student_terminal.py"]
