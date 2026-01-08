import os
import random

# ================= FILES =================
DATA = "data"
STUDENTS = f"{DATA}/students.txt"
QUIZZES = f"{DATA}/quizzes.txt"
RESULTS = f"{DATA}/results.txt"
ATTEMPTS = f"{DATA}/attempts.txt"

SUBJECTS = ["Mathematics", "English", "General Science", "Computer Science", "History"]

# ================= SETUP =================
# Create folder and files if they do not exist
if not os.path.exists(DATA):
    os.mkdir(DATA)

for f in [STUDENTS, QUIZZES, RESULTS, ATTEMPTS]:
    if not os.path.exists(f):
        open(f, "w").close()

# ================= FILE HELPERS =================
def read(file):
    return open(file).read().splitlines()

def write(file, lines):
    open(file, "w").write("\n".join(lines) + ("\n" if lines else ""))

def append(file, line):
    open(file, "a").write(line + "\n")

# ================= STUDENT MODULE =================
def student_login():
    roll = input("Roll no: ")
    pwd = input("Password: ")

    for s in read(STUDENTS):
        r, name, p = s.split("|")
        if r == roll and p == pwd:
            student_menu(roll, name)
            return
    print("Invalid entry")

def student_menu(roll, name):
    while True:
        print("\n1. Take quiz\n2. View record\n3. Exit")
        ch = input("Choose: ")

        if ch == "1":
            take_quiz(roll, name)
        elif ch == "2":
            view_record(roll)
        elif ch == "3":
            break

def take_quiz(roll, name):
    print("\nSubjects:")
    for s in SUBJECTS:
        print(s)
    subject = input("Choose subject: ")

    # Check attempts
    attempts = [a for a in read(ATTEMPTS) if a == f"{roll}|{subject}"]
    if len(attempts) >= 1:
        print("Retake not allowed")
        if len(attempts) >= 2:
            delete_student(roll)
            print(f"Student {name} deleted")
        append(ATTEMPTS, f"{roll}|{subject}")
        return

    # Load questions
    questions = [q for q in read(QUIZZES) if q.startswith(subject + "|")]
    if len(questions) < 5:
        print("Quiz not available")
        return

    # Randomly select 5 questions
    selected = random.sample(questions, 5)
    score = 0
    review = []

    for q in selected:
        parts = q.split("|")
        print("\nQ:", parts[1])
        options = parts[2:6]
        correct = parts[6]

        for opt in options:
            print(opt)

        ans = input("Choose answer (a/b/c/d): ")
        if ans == correct:
            score += 1

        review.append((parts[1], options, correct, ans))

    # Save results
    append(RESULTS, f"{roll}|{subject}|{score}")
    append(ATTEMPTS, f"{roll}|{subject}")

    # Show score
    print("\nCorrect:", score)
    print("Incorrect:", 5 - score)

    # Review quiz with ticks and crosses
    print("\n--- Review ---")
    for q, opts, cor, ans in review:
        print("\nQ:", q)
        for o in opts:
            if o[0] == cor:
                print(o, "✓")
            elif o[0] == ans:
                print(o, "✗")
            else:
                print(o)

def view_record(roll):
    records = [r for r in read(RESULTS) if r.startswith(roll + "|")]
    if not records:
        print("No quiz attempted")
        return
    for r in records:
        _, subject, score = r.split("|")
        print(f"{subject:<20}{score}")

def delete_student(roll):
    write(STUDENTS, [s for s in read(STUDENTS) if not s.startswith(roll + "|")])
    write(RESULTS, [r for r in read(RESULTS) if not r.startswith(roll + "|")])
    write(ATTEMPTS, [a for a in read(ATTEMPTS) if not a.startswith(roll + "|")])

# ================= MAIN PROGRAM =================
if __name__ == "__main__":
    while True:
        print("\nQuiz management system")
        print("\n1. Student\n2. Exit")
        choice = input("Choose: ")

        if choice == "1":
            student_login()
        elif choice == "2":
            break


