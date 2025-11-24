"""
Student Grade Analyzer

A module for managing student grades,
adding them, analyzing them, and generating reports.
"""

import sys
from typing import List, TypedDict, Optional


# Type alias for the student data structure
class Student(TypedDict):
    """Defines a fixed dictionary schema for storing student data."""

    name: str
    grades: List[int]


def calculate_average(grades: List[int]) -> Optional[float]:
    """
    Calculates the average of a list of integers.

    Args:
        grades (List[int]): A list of integer grades.

    Returns:
        Optional[float]: The average as a float, or None if the list is empty.
    """
    if not grades:
        return None
    try:
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return None


def add_new_student(students: List[Student]) -> None:
    """
    Prompts user for a name and adds a new student dictionary to the list.
    Checks for duplicates.

    Args:
        students (List[Student]): The main list of student records.
    """
    name_input = input("Enter student name: ").strip()

    if not name_input:
        print("Error: Name cannot be empty.")
        return

    # Check if student already exists
    for student in students:
        if str(student["name"]).lower() == name_input.lower():
            print(f"Student '{name_input}' already exists.")
            return

    new_student: Student = {"name": name_input, "grades": []}
    students.append(new_student)
    print(f"Student '{name_input}' added successfully.")


def add_grades_for_student(students: List[Student]) -> None:
    """
    Finds a student and allows the user to input multiple grades.
    Handles input validation for integers and range [0, 100].

    Args:
        students (List[Student]): The main list of student records.
    """
    name_input = input("Enter student name: ").strip()

    target_student: Optional[Student] = None
    for student in students:
        if str(student["name"]).lower() == name_input.lower():
            target_student = student
            break

    if not target_student:
        print(f"Student '{name_input}' not found.")
        return

    # Ensure type safety for the grades list
    grades_list = target_student["grades"]
    if not isinstance(grades_list, list):
        # Fallback if data structure is corrupted
        grades_list = []
        target_student["grades"] = grades_list

    while True:
        user_input = input("Enter a grade (or 'done' to finish): ").strip()

        if user_input.lower() == "done":
            break

        try:
            grade = int(user_input)
            if 0 <= grade <= 100:
                grades_list.append(grade)
            else:
                print("Error: Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def show_report(students: List[Student]) -> None:
    """
    Generates and prints a full report of all students, including
    individual averages and a class summary (Min, Max, Overall).

    Args:
        students (List[Student]): The main list of student records.
    """
    print("\n--- Student Report ---")

    valid_averages: List[float] = []

    if not students:
        print("No students found.")
        print("-" * 26)
        print("No data to summarize.")
        return

    for student in students:
        name = student["name"]
        grades = student["grades"]

        # Ensure grades is a list
        if isinstance(grades, list):
            avg = calculate_average(grades)
        else:
            avg = None

        if avg is not None:
            print(f"{name}'s average grade is {avg:.1f}.")
            valid_averages.append(avg)
        else:
            print(f"{name}'s average grade is N/A.")

    print("-" * 26)

    if valid_averages:
        max_avg = max(valid_averages)
        min_avg = min(valid_averages)
        overall_avg = sum(valid_averages) / len(valid_averages)

        print(f"Max Average: {max_avg:.1f}")
        print(f"Min Average: {min_avg:.1f}")
        print(f"Overall Average: {overall_avg:.1f}")
    else:
        print("No grades available to calculate summary stats.")


def find_top_performer(students: List[Student]) -> None:
    """
    Identifies and prints the student with the highest average grade.
    Uses max() with a lambda function.

    Args:
        students (List[Student]): The main list of student records.
    """
    # Filter out students who have no grades to avoid skewing results
    # or causing issues if we were to force a default value like -1
    students_with_grades = [
        s for s in students if isinstance(s["grades"], list)
        and len(s["grades"]) > 0
    ]

    if not students_with_grades:
        print("No top student (no students or no grades added).")
        return

    # Using max() with a lambda — safe since grades are non-empty lists
    top_student = max(
        students_with_grades, key=lambda s: sum(s["grades"]) / len(s["grades"])
    )

    # Calculate the average again just for the display message
    grades = top_student["grades"]
    if isinstance(grades, list):
        avg = sum(grades) / len(grades)
        print(
            f"The student with the highest average is {top_student['name']} "
            f"with a grade of {avg:.1f}."
        )


def main() -> None:
    """
    Main program entry point. Handles the menu loop and high-level
    exception handling for user input.
    """
    students: List[Student] = []

    while True:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top performer")
        print("5. Exit")

        try:
            choice_input = input("Enter your choice: ").strip()

            # Basic validation to prevent massive error stacks on weird input
            if not choice_input.isdigit():
                print("Invalid input. Please enter a number (1-5).")
                continue

            choice = int(choice_input)

            if choice == 1:
                add_new_student(students)
            elif choice == 2:
                add_grades_for_student(students)
            elif choice == 3:
                show_report(students)
            elif choice == 4:
                find_top_performer(students)
            elif choice == 5:
                print("Exiting program.")
                break
            else:
                print("Invalid option. Please choose between 1 and 5.")

        except ValueError:
            # Catch errors in int(choice_input) or unexpected string conversion
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    # Ensures the script runs only when executed directly
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nProgram interrupted by user. Exiting.")
        sys.exit(0)
