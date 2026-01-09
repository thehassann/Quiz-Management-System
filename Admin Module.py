import os

# ================= FILES =================
DATA = "data"
STUDENTS = f"{DATA}/students.txt"
TEACHERS = f"{DATA}/teachers.txt"
RESULTS = f"{DATA}/results.txt"
ATTEMPTS = f"{DATA}/attempts.txt"
ADMIN = f"{DATA}/admin.txt"

# ================= FILE HELPERS =================
def read(file):
    return open(file).read().splitlines()

def write(file, lines):
    open(file, "w").write("\n".join(lines) + ("\n" if lines else ""))

def append(file, line):
    open(file, "a").write(line + "\n")

# ================= ADMIN MODULE =================
def admin_mode():
    pwd = input("Enter admin password: ")
    # Verify password from admin.txt
    if not read(ADMIN) or pwd != read(ADMIN)[0]:
        print("Invalid entry")
        return

    while True:
        print("\n--- Admin Menu ---")
        print("1. Teacher performance")
        print("2. Student performance")
        print("3. Add teacher/student")
        print("4. Remove teacher/student")
        print("5. Allow retake")
        print("6. Back")
        choice = input("Choose: ")

        # 1️⃣ Teacher performance
        if choice == "1":
            print("\n--- Teacher Performance ---")
            for t in read(TEACHERS):
                code, name, pwd, subject = t.split("|")
                print(f"Teacher: {name}, Subject: {subject}")

        # 2️⃣ Student performance
        elif choice == "2":
            print("\n--- Student Performance ---")
            records = read(RESULTS)
            if not records:
                print("No student has attempted any quiz yet")
            for r in records:
                roll, subject, score = r.split("|")
                print(f"Student Roll: {roll}, Subject: {subject}, Score: {score}")

        # 3️⃣ Add teacher/student
        elif choice == "3":
            t_or_s = input("Add teacher or student? (t/s): ").lower()
            name = input("Name: ")
            code = input("Roll no / Teacher code: ")
            pwd = input("Password: ")
            if t_or_s == "s":
                append(STUDENTS, f"{code}|{name}|{pwd}")
                print(f"Student {name} added successfully")
            elif t_or_s == "t":
                subject = input("Subject: ")
                append(TEACHERS, f"{code}|{name}|{pwd}|{subject}")
                print(f"Teacher {name} added successfully")
            else:
                print("Invalid choice")

        # 4️⃣ Remove teacher/student
        elif choice == "4":
            t_or_s = input("Remove teacher or student? (t/s): ").lower()
            code = input("Roll no / Teacher code: ")
            if t_or_s == "s":
                # Remove student data from all files
                write(STUDENTS, [s for s in read(STUDENTS) if not s.startswith(code + "|")])
                write(RESULTS, [r for r in read(RESULTS) if not r.startswith(code + "|")])
                write(ATTEMPTS, [a for a in read(ATTEMPTS) if not a.startswith(code + "|")])
                print(f"Student {code} removed successfully")
            elif t_or_s == "t":
                write(TEACHERS, [t for t in read(TEACHERS) if not t.startswith(code + "|")])
                print(f"Teacher {code} removed successfully")
            else:
                print("Invalid choice")

        # 5️⃣ Allow retake
        elif choice == "5":
            roll = input("Enter student roll no to allow retake: ")
            # Remove all attempts for that student
            write(ATTEMPTS, [a for a in read(ATTEMPTS) if not a.startswith(roll + "|")])
            print(f"Retake allowed for student {roll}")

        # 6️⃣ Back
        elif choice == "6":
            break

        else:
            print("Invalid choice, try again")