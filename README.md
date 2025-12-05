# UML-Analyzer
CSCE-411 Class Project

__Zoe Kerchal, Noah Bearden, Owen Addison__

## Objective
Using Python, verify that UML class diagrams (written in PlantUML) accurately depict sample objects and classes, including constraints. 
Convert user-provided SQL schema to a plantUML class diagram and compare it with the user-provided plantUML code.
Then, output a report citing inaccuracies, syntax errors, and a similarity score to the PlantUML code.

## Research & Report
Compare our script to the performance of AI prompted to do the same task.

## Running the project
1. In the terminal, change into the project directory ```cd UML-Analyzer```
2. Change into the project source folder ```cd pythonProject```
3. In your terminal, run the command ```python run-files.py``` (runs the CLI program)
4. There is an example SQL schema file and user-provided plantUML code file that you can use to test the program
5. If you want to run it on your own files, follow these steps
   - Place your SQL schema file as a .txt format in ```pythonProject/sql_files```
   - Place your plantUML code file as a .txt format in ```pythonProject/user_files```
   - This will allow your file to appear in the list of options during runtime

## Testing the project
For manual testing (grading purposes), follow these steps
1. The example user-provided file ```user_uml_import.txt``` has three key differences from the ```plantuml_export.txt```
   - "Collection -- Parent" is missing in the relationships
   - "class Addreess" is misspelled, should be "class Address" 
   - "+String description" is missing from the Equipment class
2. If you want to tweak the ```user_uml_input.txt``` file, simply alter whatever lines, attributes, etc.
3. Re-run the project to see how the changes affect the output.
