# ----------------------------------------------------------------------------------- #
# Title: Assignment06
# Desc: This assignment demonstrates using functions with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Stefan Sandberg,5/28/2025, restructuring script by adding functions,
#                               classes, staticmethods, along with docstrings
#                               all with separations of concerns design
# ----------------------------------------------------------------------------------- #

import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program --------
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
-----------------------------------------  
'''
FILE_NAME: str = 'Enrollments.json'

# Define the Data Variables
menu_choice: str = ''   # Hold the choice made by the user.
students: list = []     # A table of student data.

# -----------------------------------------------------------------------------------
# Start of class named IO
# -----------------------------------------------------------------------------------
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    Change Log: (Who, When, What)
    RRoot,1/1/2030,Created Script
    Stefan Sandberg, 5/28/2025, Added class handling input output functions
                                Added functions within class with the decorator static
                                method
    """
    
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays the custom error messages to the user

        :param message: string with error message
        :param error: Exception object with technical details
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays the menu of choices to the user

        :param menu: string with menu options
        :return: None
        """
        print()
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        This function gets a menu choice from the user

        :return: string with the users choice
        """
        menu_choice = ""
        try:
            menu_choice = input("Enter your menu choice number: ")
            if menu_choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return menu_choice

    @staticmethod
    def output_student_courses(student_data: list):
        """
        This function displays the student's name and course separated by comma. Each
        entry is separated by a new line.

        :param student_data: list of student dictionaries
        :return: None
        """
        print("*" * 50)
        for student in student_data:
            message = " {},{},{}."
            print(message.format(student["FirstName"], student["LastName"],
                student["CourseName"]))
        print("*" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        This function gets the first name, last name, and course name from the user

        :param student_data: list of student dictionaries
        :return: list of student dictionaries
        """
        try:
            # Input the data
            student_first_name = input("Enter the student's first name? ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name? ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Enter the student's course name? ")

            student = {
                "FirstName": student_first_name,
                "LastName": student_last_name,
                "CourseName": course_name
            }
            student_data.append(student)
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

# -----------------------------------------------------------------------------------
# Start of class named FileProcessor
# -----------------------------------------------------------------------------------
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files
    Change Log: (Who, When, What)
    RRoot,1/1/2030,Created Script
    Stefan Sandberg, 5/28/2025, Added class handling flie processing read and writing
                                data to and from JSON files
                                Added functions within class with the decorator static
                                method
    """
    
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function extracts the data from JSON file and read the file data into table

        :param file_name: string with name of file
        :param student_data: list of student dictionaries
        :return: list of student dictionaries
        """
        file = None
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function saves the data to the JSON file

        :param file_name: string with name of file
        :param student_data: list of student dictionaries
        :return: None
        """
        file = None
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()

            print("*" * 50)
            print("The following data has been saved to the file:")
            for student in student_data:
                message = " {},{},{}."
                print(message.format(student["FirstName"], student["LastName"],
                    student["CourseName"]))
            print("*" * 50)

        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if file is not None and not file.closed:
                file.close()

# -----------------------------------------------------------------------------------
# Beginning of the main body of this script
# -----------------------------------------------------------------------------------
"""
    A collection of processing layer functions that work with JSON files
    Change Log: (Who, When, What)
    RRoot,1/1/2030,Created Script
    Stefan Sandberg, 5/28/2025, Added a main loop or driver code to control the main flow
                                of the code and to call the classes
    """
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:  # Repeat the following tasks
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break  # out of the while loop

print("Program Ended") 
