def collect_and_save_student_details():
    name = input("Enter student's name: ")
    age = input("Enter student's age: ")
    email = input("Enter student's email: ")
    with open("student_details.txt", "a") as file:
        file.write(f"Name: {name}, Age: {age}, Email: {email}\n")

# Example usage:from lab5.task1_1 import collect_and_save_student_details

# Save in a specific directory or with a custom filename
collect_and_save_student_details(output_directory="lab5", filename="student_record.txt")
# collect_and_save_student_details()