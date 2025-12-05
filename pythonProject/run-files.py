from sql_to_py import print_uml_from_schema
from validate_design import validate_file
import os

folder_path = "./sql_files"
folder_path_user = "./user_files"
file_and_dir_names = os.listdir(folder_path)
file_and_dir_names_user = os.listdir(folder_path_user)

sql_files = [f for f in file_and_dir_names if os.path.isfile(os.path.join(folder_path, f))]
user_files = [f for f in file_and_dir_names_user if os.path.isfile(os.path.join(folder_path_user, f))]


index = 1
for sql_file in sql_files:
    print(str(index) + ". " + sql_file)
    index += 1


first_question = input(
    "Which SQL file do you want to convert to UML? Please enter the number of the SQL file you want to scan, enter 'quit' to stop: ")

def prompt_validation():
    answer = input("\nDo you want to validate the uml against your own file? (enter 'y' or 'n'): \n")
    while answer.lower() != "y" and answer.lower() != "n":
        answer = input("Please enter a valid input (enter 'y' or 'n'): ")
    if answer == 'y':
        index_user = 1
        for user_file in user_files:
            print(str(index_user) + ". " + user_file)
            index_user += 1
        file_choice = input("Which file do you want to validate? (enter 'quit' to stop): ")
        while file_choice.lower() != "quit":
            try:
                file_choice = int(file_choice)
                if len(user_files) >= file_choice >= 1:
                    validate_file(folder_path_user + "/" + user_files[file_choice - 1])
                    file_choice = "quit"
                else:
                    file_choice = input("Please enter a valid input (enter 'quit' to stop): ")
            except ValueError:
                file_choice = input("Please enter a valid input (enter 'quit' to stop): ")


while first_question != "quit":
    try:
        first_question = int(first_question)
        if len(sql_files) >= first_question >= 1:
            print_uml_from_schema(folder_path + "/" + sql_files[first_question - 1])
            first_question = "quit"
            prompt_validation()
        else:
            first_question = input("Please enter a number within the range, enter 'quit' to stop: ")
    except ValueError:
        first_question = input("Please enter a valid number between 1 and " + str(len(sql_files)) + ": ")