"""
Assignment06
This assignment demonstrates using functions with structured error handling
Change Log: (Who, When, What)
    RRoot,1/1/2030,Created Script
    Stefan Sandberg,5/28/2025, restructuring script by adding functions,
                               classes, staticmethods, along with docstrings
                               all with separations of concerns design
"""

import json


class Student:
    """A class representing a student's course registration."""
    
    def __init__(self, first_name, last_name, course_name):
        self.first_name = first_name
        self.last_name = last_name
        self.course_name = course_name

    @staticmethod
    def validate_name(name):
        """
        Validates if a name contains only alphabetic characters, hyphens, 
        and apostrophes.
        """
        for character in name:
            is_valid = (
                character.isalpha() or  
                character == '-' or     
                character == "'"        
            )
            if not is_valid:
                return False
        return True


class FileProcessor:
    """Handles all file operations for student registrations."""
    
    @staticmethod
    def read_data_from_file(file_name, student_data):
        """
        Reads student data from a JSON file.
        """
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a problem with reading the file.", 
                e
            )
            return []

    @staticmethod
    def write_data_to_file(file_name, student_data):
        """
        Writes student data to a JSON file.
        """
        try:
            with open(file_name, "w") as file:
                json.dump(student_data, file)
            return True
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a problem with writing to the file.", 
                e
            )
            return False


class IO:
    """Handles all input/output operations."""
    
    MENU = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''

    @staticmethod
    def output_error_messages(message, error=None):
        """
        Displays error messages to the user.
        """
        print(message)
        if error:
            print("-- Technical Error Message -- ")
            print(error.__doc__)
            print(error.__str__())

    @staticmethod
    def output_menu(menu):
        """
        Displays the menu to the user.
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """
        Gets the menu choice from the user.
        """
        return input("What would you like to do: ")

    @staticmethod
    def input_student_data(student_data):
        """
        Gets student registration data from the user.
        """
        while True:
            try:
                first_name = input("Enter the student's first name: ")
                if not Student.validate_name(first_name):
                    raise ValueError(
                        "The first name should only contain letters, "
                        "hyphens, or apostrophes."
                    )
                
                last_name = input("Enter the student's last name: ")
                if not Student.validate_name(last_name):
                    raise ValueError(
                        "The last name should only contain letters, "
                        "hyphens, or apostrophes."
                    )
                
                course_name = input("Please enter the name of the course: ")
                return Student(first_name, last_name, course_name)
            except ValueError as e:
                IO.output_error_messages(str(e), e)

    @staticmethod
    def output_student_courses(student_data):
        """
        Displays the current student registration data.
        """
        print("*" * 50)
        for student in student_data:
            print(
                f'Student {student["FirstName"]} '
                f'{student["LastName"]} is enrolled in '
                f'{student["CourseName"]}'
            )
        print("*" * 50)


class DataProcessor:
    """Handles data processing operations."""
    
    @staticmethod
    def add_student(students, student):
        """
        Adds a new student registration to the list.
        """
        student_data = {
            "FirstName": student.first_name,
            "LastName": student.last_name,
            "CourseName": student.course_name
        }
        students.append(student_data)
        return students


def main():
    """Main function to run the program."""
    # Constants
    FILE_NAME = "Enrollments.json"
    
    # Variables
    students = []
    
    # Read initial data
    students = FileProcessor.read_data_from_file(FILE_NAME, students)
    
    # Main program loop
    while True:
        IO.output_menu(IO.MENU)
        menu_choice = IO.input_menu_choice()
        
        if menu_choice == "1":
            student = IO.input_student_data(students)
            students = DataProcessor.add_student(students, student)
            print(
                f"You have registered {student.first_name} "
                f"{student.last_name} for {student.course_name}."
            )
            
        elif menu_choice == "2":
            IO.output_student_courses(students)
            
        elif menu_choice == "3":
            if FileProcessor.write_data_to_file(FILE_NAME, students):
                print("The following data was saved to file!")
                IO.output_student_courses(students)
                
        elif menu_choice == "4":
            break
            
        else:
            print("Please only choose option 1, 2, 3, or 4")
    
    print("Program Ended")


main()
