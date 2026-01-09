import os
import random

# ================= FILES =================
DATA = "data"
TEACHERS = f"{DATA}/teachers.txt"
QUIZZES = f"{DATA}/quizzes.txt"
RESULTS = f"{DATA}/results.txt"
ATTEMPTS = f"{DATA}/attempts.txt"

# ================= FILE HELPERS =================
def read(file):
    try:
        with open(file, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

def write(file, lines):
    with open(file, 'w') as f:
        if lines:
            f.write("\n".join(lines))

def append(file, line):
    with open(file, 'a') as f:
        f.write(line + "\n")

# ================= TEACHER MODULE =================
def teacher_mode():
    code = input("Teacher code: ")
    pwd = input("Password: ")

    # Verify teacher
    teacher = None
    for t in read(TEACHERS):
        parts = t.split("|")
        if len(parts) >= 4:
            t_code, name, t_pwd, subject = parts[:4]
            if t_code == code and t_pwd == pwd:
                teacher = {"code": t_code, "name": name, "subject": subject}
                break
    
    if not teacher:
        print("Invalid login")
        return

    while True:
        print(f"\n--- Teacher Menu ({teacher['name']}) ---")
        print("1. View marksheet")
        print("2. Double check")
        print("3. Create / Edit quiz")
        print("4. Exit")
        choice = input("Choose: ").strip()

        # 1️⃣ View marksheet
        if choice == "1":
            print(f"\n--- Marks for {teacher['subject']} ---")
            found = False
            for r in read(RESULTS):
                parts = r.split("|")
                if len(parts) >= 3:
                    roll, sub, score = parts[:3]
                    if sub == teacher["subject"]:
                        print(f"{roll:<10} {score}")
                        found = True
            if not found:
                print("No students attempted this quiz yet.")

        # 2️⃣ Double check
        elif choice == "2":
            roll = input("Enter student roll no to double check: ").strip()
            quiz_lines = [q for q in read(QUIZZES) if q.startswith(teacher["subject"] + "|")]
            
            if not quiz_lines:
                print("No quiz available for this subject")
                continue
            
            results_lines = read(RESULTS)
            student_score = None
            
            for r in results_lines:
                parts = r.split("|")
                if len(parts) >= 3:
                    r_roll, sub, score = parts[:3]
                    if r_roll == roll and sub == teacher["subject"]:
                        student_score = int(score)
                        break
            
            if student_score is None:
                print("Student has not attempted this quiz")
                continue

            print(f"\n--- Double checking quiz for {roll} ---")
            for q in quiz_lines:
                parts = q.split("|")
                if len(parts) >= 7:
                    question = parts[1]
                    options = parts[2:6]
                    correct = parts[6]
                    print("\nQ:", question)
                    for o in options:
                        if o[0] == correct:
                            print(o, "✓")
                        else:
                            print(o)
                    mark = input("Mark as correct? (y/n): ").lower()
                    if mark == "y":
                        student_score += 1
            
            # Update student score
            new_results = []
            for r in results_lines:
                parts = r.split("|")
                if len(parts) >= 3:
                    r_roll, sub, score = parts[:3]
                    if r_roll == roll and sub == teacher["subject"]:
                        new_results.append(f"{r_roll}|{sub}|{student_score}")
                    else:
                        new_results.append(r)
            
            write(RESULTS, new_results)
            print(f"Updated score for {roll}: {student_score}")

        # 3️⃣ Create / Edit quiz
        elif choice == "3":
            print("\n1. Edit existing quiz")
            print("2. Create new quiz")
            print("3. Back")
            sub_choice = input("Choose: ").strip()

            if sub_choice == "1":
                quiz_lines = [q for q in read(QUIZZES) if q.startswith(teacher["subject"] + "|")]
                if not quiz_lines:
                    print("No quiz to edit")
                    continue
                
                print("\n--- Existing Questions ---")
                for idx, q in enumerate(quiz_lines):
                    parts = q.split("|")
                    if len(parts) >= 2:
                        print(f"{idx+1}. {parts[1]}")
                
                try:
                    q_idx = int(input("Select question number to edit: ")) - 1
                except ValueError:
                    print("Invalid input")
                    continue
                
                if 0 <= q_idx < len(quiz_lines):
                    q_parts = quiz_lines[q_idx].split("|")
                    new_question = input("Enter new question text (or press enter to skip): ").strip()
                    if new_question:
                        q_parts[1] = new_question
                    
                    for i in range(2, 6):
                        new_opt = input(f"Option {i-1} (or press enter to skip): ").strip()
                        if new_opt:
                            q_parts[i] = new_opt
                    
                    new_correct = input("Enter correct option (a/b/c/d) or press enter to skip: ").strip().lower()
                    if new_correct in ['a', 'b', 'c', 'd']:
                        q_parts[6] = new_correct
                    
                    quiz_lines[q_idx] = "|".join(q_parts)
                    all_quizzes = [q for q in read(QUIZZES) if not q.startswith(teacher["subject"] + "|")]
                    all_quizzes.extend(quiz_lines)
                    write(QUIZZES, all_quizzes)
                    print("Question updated successfully")
                else:
                    print("Invalid selection")

            elif sub_choice == "2":
                print("\n--- Creating New Quiz ---")
                for i in range(1, 11):
                    print(f"\nQuestion {i}:")
                    question = input("Enter question: ").strip()
                    a = input("Option a: ").strip()
                    b = input("Option b: ").strip()
                    c = input("Option c: ").strip()
                    d = input("Option d: ").strip()
                    correct = input("Correct option (a/b/c/d): ").strip().lower()
                    
                    if correct not in ['a', 'b', 'c', 'd']:
                        print("Invalid option, defaulting to 'a'")
                        correct = 'a'
                    
                    append(QUIZZES, f"{teacher['subject']}|{question}|{a}|{b}|{c}|{d}|{correct}")
                print("New quiz created successfully")

            elif sub_choice == "3":
                continue
            else:
                print("Invalid choice")

        # 4️⃣ Exit
        elif choice == "4":
            break

        else:
            print("Invalid choice, try again")

# ================= MAIN PROGRAM =================
def main():
    print("Welcome to Quiz Management System")
    while True:
        print("\n--- Main Menu ---")
        print("1. Teacher Login")
        print("2. Exit")
        choice = input("Choose: ").strip()
        
        if choice == "1":
            teacher_mode()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    # Ensure data directory exists
    if not os.path.exists(DATA):
        os.makedirs(DATA)
    
    # Ensure necessary files exist
    for file in [TEACHERS, QUIZZES, RESULTS, ATTEMPTS]:
        if not os.path.exists(file):
            with open(file, 'w'):
                pass
    
    main()