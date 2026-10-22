"""Quick smoke-test for the terminal version — feeds automated inputs."""
import subprocess, sys

# Sequence: Add a student (1), View (2), Search (3), Update (4), View (2), Delete (5), View (2), Exit (6)
inputs = "\n".join([
    "1",                          # Add Student
    "101", "Rahul Sharma", "Computer Science", "4", "9876543210", "85.5",
    "1",                          # Add another
    "102", "Priya Patel", "IT", "3", "9123456789", "92.0",
    "2",                          # View All
    "3",                          # Search
    "101",
    "4",                          # Update
    "101", "Rahul S. Sharma", "CSE", "5", "9876543210", "88.0",
    "2",                          # View after update
    "5",                          # Delete
    "102",
    "2",                          # View after delete
    "5",                          # Delete non-existent
    "999",
    "3",                          # Search non-existent
    "999",
    "6",                          # Exit
]) + "\n"

result = subprocess.run(
    [sys.executable, "student_terminal.py"],
    input=inputs, capture_output=True, text=True, timeout=15
)

print("=== STDOUT ===")
print(result.stdout)
if result.stderr:
    print("=== STDERR ===")
    print(result.stderr)
print(f"\nReturn code: {result.returncode}")
