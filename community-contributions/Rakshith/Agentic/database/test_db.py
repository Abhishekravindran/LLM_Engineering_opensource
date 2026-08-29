import sqlite3

conn = sqlite3.connect("database/employee.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Employees LIMIT 5")
rows = cursor.fetchall()

print("First 5 employees:\n")
for row in rows:
    print(row)

conn.close()