import sqlite3

conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

def ensure_status_column():
    cursor.execute("PRAGMA table_info(students)")
    cols = {row["name"] for row in cursor.fetchall()}
    if "status" not in cols:
        cursor.execute("ALTER TABLE students ADD COLUMN status TEXT NOT NULL DEFAULT 'Active'")
        conn.commit()
        cursor.execute("UPDATE students SET status='Active' WHERE status IS NULL")
        conn.commit()

ensure_status_column()

def add_student(name, age, course):
    cursor.execute(
        "INSERT INTO students (name, age, course, status) VALUES (?, ?, ?, 'Active')",
        (name, age, course),
    )
    conn.commit()
    print("✅ Student added successfully!")

def view_students(active_only=True):
    if active_only:
        cursor.execute("SELECT * FROM students WHERE status='Active' ORDER BY id")
        title = "\n--- Active Student Records ---"
    else:
        cursor.execute("SELECT * FROM students WHERE status='Inactive' ORDER BY id")
        title = "\n--- Inactive Student Records ---"

    rows = cursor.fetchall()
    print(title)
    if not rows:
        print("❌ No student records found.")
        return
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Course':<15} {'Status':<10}")
    print("-" * 60)
    for r in rows:
        print(f"{r['id']:<5} {r['name']:<20} {str(r['age']) if r['age'] is not None else '':<5} {str(r['course']) if r['course'] is not None else '':<15} {r['status']:<10}")

def search_student(student_id):
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    r = cursor.fetchone()
    if r:
        print("\n--- Student Found ---")
        print(f"ID: {r['id']}, Name: {r['name']}, Age: {r['age']}, Course: {r['course']}, Status: {r['status']}")
    else:
        print("❌ Student not found.")

def update_student(student_id, name, age, course):
    cursor.execute(
        "UPDATE students SET name=?, age=?, course=? WHERE id=?",
        (name, age, course, student_id),
    )
    conn.commit()
    if cursor.rowcount > 0:
        print("✅ Student updated successfully!")
    else:
        print("❌ Student ID not found.")

def deactivate_student(student_id):
    cursor.execute("UPDATE students SET status='Inactive' WHERE id=?", (student_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("✅ Student marked as Inactive (soft deleted).")
    else:
        print("❌ Student ID not found.")

def activate_student(student_id):
    cursor.execute("UPDATE students SET status='Active' WHERE id=?", (student_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("✅ Student re-activated.")
    else:
        print("❌ Student ID not found.")

def menu():
    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View Active Students")
        print("3. View Inactive Students")
        print("4. Search Student by ID")
        print("5. Update Student")
        print("6. Mark Student as Inactive")
        print("7. Reactivate Student")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter name: ")
            try:
                age = int(input("Enter age: "))
            except ValueError:
                print("❌ Age must be a number.")
                continue
            course = input("Enter course: ")
            add_student(name, age, course)

        elif choice == "2":
            view_students(active_only=True)

        elif choice == "3":
            view_students(active_only=False)

        elif choice == "4":
            try:
                student_id = int(input("Enter student ID: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            search_student(student_id)

        elif choice == "5":
            try:
                student_id = int(input("Enter student ID to update: "))
                age = int(input("Enter new age: "))
            except ValueError:
                print("❌ Invalid number input.")
                continue
            name = input("Enter new name: ")
            course = input("Enter new course: ")
            update_student(student_id, name, age, course)

        elif choice == "6":
            try:
                student_id = int(input("Enter student ID to mark inactive: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            deactivate_student(student_id)

        elif choice == "7":
            try:
                student_id = int(input("Enter student ID to reactivate: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            activate_student(student_id)

        elif choice == "8":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice, try again.")

menu()
conn.close()
