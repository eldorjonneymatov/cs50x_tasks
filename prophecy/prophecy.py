from cs50 import SQL
import csv

db = SQL("sqlite:///roster.db")

db.execute("DELETE FROM students")
db.execute("DELETE FROM houses")

id_count = 1
with open('students.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = db.execute("SELECT id FROM houses WHERE name = ?", row['house'])
        if r:
            house_id = r[0]['id']
        else:
            db.execute("INSERT INTO houses VALUES(?, ?, ?)", id_count, row['house'], row['head'])
            house_id = id_count
            id_count += 1
        id = int(row['id'])
        db.execute("INSERT INTO students (id, student_name, house_id) VALUES(?, ?, ?)", id, row['student_name'], house_id)

rows = db.execute("SELECT * FROM students")
for row in rows:
    print(row)