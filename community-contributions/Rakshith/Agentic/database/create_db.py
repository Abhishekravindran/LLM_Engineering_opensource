import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database/employee.db")
cursor = conn.cursor()

# -----------------------------
# Create Departments Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
)
""")

# -----------------------------
# Create Employees Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER,
    city TEXT,
    salary INTEGER,
    experience INTEGER,
    FOREIGN KEY (department_id)
        REFERENCES Departments(department_id)
)
""")

# -----------------------------
# Insert Departments
# -----------------------------
departments = [
    (1, "Engineering"),
    (2, "Marketing"),
    (3, "HR"),
    (4, "Finance"),
    (5, "Sales")
]

cursor.executemany(
    "INSERT OR REPLACE INTO Departments VALUES (?, ?)",
    departments
)

# -----------------------------
# Insert Employees (25 Records)
# -----------------------------
employees = [
    (1, "Aarav", 1, "Bengaluru", 120000, 5),
    (2, "Diya", 1, "Bengaluru", 95000, 3),
    (3, "Rohan", 2, "Mumbai", 85000, 4),
    (4, "Ananya", 3, "Hyderabad", 65000, 2),
    (5, "Kiran", 4, "Chennai", 90000, 6),
    (6, "Sneha", 5, "Bengaluru", 78000, 3),
    (7, "Rahul", 1, "Pune", 140000, 7),
    (8, "Meera", 2, "Bengaluru", 72000, 2),
    (9, "Vikram", 5, "Delhi", 88000, 5),
    (10, "Pooja", 4, "Mumbai", 102000, 6),
    (11, "Harsha", 1, "Bengaluru", 110000, 4),
    (12, "Nisha", 3, "Chennai", 68000, 3),
    (13, "Aditya", 2, "Hyderabad", 79000, 4),
    (14, "Keerthi", 1, "Bengaluru", 98000, 2),
    (15, "Manoj", 5, "Pune", 87000, 5),
    (16, "Shreya", 4, "Delhi", 105000, 7),
    (17, "Abhishek", 1, "Bengaluru", 150000, 8),
    (18, "Lavanya", 3, "Mumbai", 71000, 2),
    (19, "Arjun", 2, "Bengaluru", 93000, 5),
    (20, "Sanjana", 5, "Hyderabad", 82000, 4),
    (21, "Naveen", 4, "Bengaluru", 99000, 5),
    (22, "Ishita", 1, "Chennai", 108000, 6),
    (23, "Pranav", 2, "Pune", 76000, 3),
    (24, "Bhavana", 3, "Bengaluru", 69000, 2),
    (25, "Yash", 5, "Bengaluru", 89000, 5)
]

cursor.executemany(
    "INSERT OR REPLACE INTO Employees VALUES (?, ?, ?, ?, ?, ?)",
    employees
)

conn.commit()
conn.close()

print("Database created successfully with 25 employee records!")