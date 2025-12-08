# UML-Analyzer
CSCE-411 Class Project

__Zoe Kerchal, Noah Bearden, Owen Addison__

## Objective
Using Python, verify that UML class diagrams (written in PlantUML) accurately depict sample objects and classes, including constraints. 
Convert user-provided SQL schema to a plantUML class diagram and compare it with the user-provided plantUML code.
Then, output a report citing inaccuracies, syntax errors, and a similarity score to the PlantUML code.

The goal is to verify real implementations match documentation, and suggest fixes.

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
6. If you want to test an arbitrary file against an answer key: In your terminal, run the command ```python gpt_answer_key.py``` (runs another CLI program). Make sure you added the target file to  ```pythonProject/chatGPT_generated_answers```

## Testing the project
For manual testing (grading purposes), follow these steps
1. The example user-provided files ```uml-1.txt``` (and -2 and -3) has three key differences from the dump in ```plantuml_export.txt```
   - "Collection -- Parent" is missing in the relationships
   - "class Addreess" is misspelled, should be "class Address" 
   - "+String description" is missing from the Equipment class
2. If you want to tweak the ```uml-1.txt``` file, simply alter whatever lines, attributes, etc.
3. Re-run the project to see how the changes affect the output.

## Acknowledgements
We used real sample SQL schema from real websites (1), sample-files (2), and Oracle (3) for authenticity. This was gathered from public sources