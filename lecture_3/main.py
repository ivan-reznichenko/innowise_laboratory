students = []

while True:
    try:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Generate a full report")
        print("4. Find the top student")
        print("5. Exit program")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student name: ")
            exists = False
            for student in students:
                if student['name'] == name:
                    exists = True
                    break
            if exists:
                print("Student already exists.")
            else:
                students.append({'name': name, 'grades': []})

        elif choice == '2':
            name = input("Enter student name: ")
            found_student = None
            for student in students:
                if student['name'] == name:
                    found_student = student
                    break
            
            if found_student is None:
                print("Student not found.")
            else:
                while True:
                    grade_input = input("Enter a grade (or 'done' to finish): ")
                    if grade_input.lower() == 'done':
                        break
                    try:
                        grade = int(grade_input)
                        if 0 <= grade <= 100:
                            found_student['grades'].append(grade)
                        else:
                            print("Invalid input. Please enter a number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

        elif choice == '3':
            print("--- Student Report ---")
            if not students:
                print("No students available.")
            else:
                valid_averages = []
                for student in students:
                    try:
                        avg = sum(student['grades']) / len(student['grades'])
                        print(f"{student['name']}'s average grade is {avg}.")
                        valid_averages.append(avg)
                    except ZeroDivisionError:
                        print(f"{student['name']}'s average grade is N/A.")
                
                print("--------------------------")
                if valid_averages:
                    max_avg = max(valid_averages)
                    min_avg = min(valid_averages)
                    overall_avg = sum(valid_averages) / len(valid_averages)
                    print(f"Max Average: {max_avg}")
                    print(f"Min Average: {min_avg}")
                    print(f"Overall Average: {overall_avg}")
                else:
                    print("No grades available for summary.")

        elif choice == '4':
            valid_students = [s for s in students if s['grades']]
            if not valid_students:
                print("No top student found.")
            else:
                top_student = max(valid_students, key=lambda s: sum(s['grades']) / len(s['grades']))
                top_avg = sum(top_student['grades']) / len(top_student['grades'])
                print(f"The student with the highest average is {top_student['name']} with a grade of {top_avg}.")

        elif choice == '5':
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please try again.")

    except Exception:
        print("An error occurred. Please try again.")