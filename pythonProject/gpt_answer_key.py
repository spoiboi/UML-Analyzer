from validate_design import compare_two_files
import os


chatgpt_path = "./chatGPT_generated_answers"
answer_key_path = "./answer_keys"

answer_names = os.listdir(answer_key_path)
chatgpt_names = os.listdir(chatgpt_path)

answer_files = [f for f in answer_names if os.path.isfile(os.path.join(answer_key_path, f))]
chatgpt_files = [f for f in chatgpt_names if os.path.isfile(os.path.join(chatgpt_path, f))]


index = 1
for answer in answer_files:
    print(str(index) + ". " + answer)
    index += 1

first_question = input(
    "Which answer key do you want to check against? Please enter the number of the answer file you want to use, enter 'quit' to stop: ")

def get_target_file(key_path):
    index = 1
    for chatgpt_file in chatgpt_files:
        print(str(index) + ". " + chatgpt_file)
        index += 1
    second_question = input(
       "Which ChatGPT file do you want to compare against an answer key? Please enter the number of the answer file you want to use, enter 'quit' to stop:"
    )
    while second_question!="quit":
        try:
            second_question = int(second_question)
            if len(chatgpt_files) >= second_question >= 1:
                gpt_path = chatgpt_path + "/" + chatgpt_files[second_question - 1]
                second_question = "quit"
                compare_two_files(key_path, gpt_path)
            else:
                second_question = input("Please enter a number within the range, enter 'quit' to stop: ")
        except ValueError:
            second_question = input("Please enter a valid number between 1 and " + str(len(chatgpt_files)) + ": ")



while first_question != "quit":
    try:
        first_question = int(first_question)
        if len(answer_files) >= first_question >= 1:
            key_path = answer_key_path + "/" + answer_files[first_question - 1]
            first_question = "quit"
            get_target_file(key_path)
        else:
            first_question = input("Please enter a number within the range, enter 'quit' to stop: ")
    except ValueError:
        first_question = input("Please enter a valid number between 1 and " + str(len(answer_files)) + ": ")