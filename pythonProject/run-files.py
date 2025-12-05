from pythonProject.sql_to_py import print_uml_from_schema
from pythonProject.validate_design import validate_file

sql_files = ["schema.txt"]
index = 1
for sql_file in sql_files:
    print(str(index) + ". " + sql_file)
    index += 1
first_question = input(
    "Which SQL file do you want to convert to UML? Please enter the number of the SQL file you want to scan, enter 'quit' to stop: ")
while first_question != "quit":
    try:
        first_question = int(first_question)
        if len(sql_files) >= first_question >= 1:
            print_uml_from_schema(sql_files[first_question - 1])
            validate_file()
            first_question = "quit"
        else:
            first_question = input("Please enter a number within the range, enter 'quit' to stop: ")
    except ValueError:
        first_question = input("Please enter a valid number between 1 and " + str(len(sql_files)) + ": ")