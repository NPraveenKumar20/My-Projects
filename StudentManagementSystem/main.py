import sqlite3

class Student:
    def __init__(self, student_id=None, name=None, age=None, course=None, status="Active"):
        self.id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.status = status

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Age: {self.age}, Course: {self.course}, Status: {self.status}"

class StudentManager:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()
        self.ensure_status_column()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            status TEXT NOT NULL DEFAULT 'Active'
        )
        """)
        self.conn.commit()

    def ensure_status_column(self):
        self.cursor.execute("PRAGMA table_info(students)")
        cols = {row["name"] for row in self.cursor.fetchall()}
        if "status" not in cols:
            self.cursor.execute("ALTER TABLE students ADD COLUMN status TEXT NOT NULL DEFAULT 'Active'")
            self.conn.commit()

    def add_student(self, student: Student):
        self.cursor.execute(
            "INSERT INTO students (name, age, course, status) VALUES (?, ?, ?, ?)",
            (student.name, student.age, student.course, student.status)
        )
        self.conn.commit()
        print("✅ Student added successfully!")

    def view_students(self, active_only=True):
        status_filter = "Active" if active_only else "Inactive"
        self.cursor.execute("SELECT * FROM students WHERE status=? ORDER BY id", (status_filter,))
        rows = self.cursor.fetchall()

        title = f"\n--- {status_filter} Student Records ---"
        print(title)
        if not rows:
            print("❌ No student records found.")
            return
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Course':<15} {'Status':<10}")
        print("-" * 60)
        for r in rows:
            print(f"{r['id']:<5} {r['name']:<20} {str(r['age']) if r['age'] else '':<5} {r['course'] or '':<15} {r['status']:<10}")

    def search_student(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        r = self.cursor.fetchone()
        if r:
            student = Student(r["id"], r["name"], r["age"], r["course"], r["status"])
            print("\n--- Student Found ---")
            print(student)
        else:
            print("❌ Student not found.")

    def update_student(self, student: Student):
        self.cursor.execute(
            "UPDATE students SET name=?, age=?, course=? WHERE id=?",
            (student.name, student.age, student.course, student.id)
        )
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("✅ Student updated successfully!")
        else:
            print("❌ Student ID not found.")

    def deactivate_student(self, student_id):
        self.cursor.execute("UPDATE students SET status='Inactive' WHERE id=?", (student_id,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("✅ Student marked as Inactive (soft deleted).")
        else:
            print("❌ Student ID not found.")

    def activate_student(self, student_id):
        self.cursor.execute("UPDATE students SET status='Active' WHERE id=?", (student_id,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("✅ Student re-activated.")
        else:
            print("❌ Student ID not found.")

    def close(self):
        self.conn.close()

def menu():
    manager = StudentManager()

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
            student = Student(name=name, age=age, course=course)
            manager.add_student(student)

        elif choice == "2":
            manager.view_students(active_only=True)

        elif choice == "3":
            manager.view_students(active_only=False)

        elif choice == "4":
            try:
                student_id = int(input("Enter student ID: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            manager.search_student(student_id)

        elif choice == "5":
            try:
                student_id = int(input("Enter student ID to update: "))
                age = int(input("Enter new age: "))
            except ValueError:
                print("❌ Invalid number input.")
                continue
            name = input("Enter new name: ")
            course = input("Enter new course: ")
            student = Student(student_id=student_id, name=name, age=age, course=course)
            manager.update_student(student)

        elif choice == "6":
            try:
                student_id = int(input("Enter student ID to mark inactive: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            manager.deactivate_student(student_id)

        elif choice == "7":
            try:
                student_id = int(input("Enter student ID to reactivate: "))
            except ValueError:
                print("❌ ID must be a number.")
                continue
            manager.activate_student(student_id)

        elif choice == "8":
            print("👋 Exiting...")
            manager.close()
            break

        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    menu()
