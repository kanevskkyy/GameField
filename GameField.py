import json
import os

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions

def show_stats(user_point, correct_answer, wrong_answers):
    print(f"Your points : {user_point}")
    print(f"Correct answers : {correct_answer}")
    print(f"Wrong answers : {wrong_answers}")


def show_field(questions):
    max_len = 0
    for category in questions.keys():
        if len(category) > max_len:
            max_len = len(category)

    for category, items in questions.items():
        print(f"{category}", end="")

        if len(category) == max_len:
            print(" ", end="")
        else:
            for spaces in range(max_len - len(category) + 1):
                print(" ", end="")

        for points, item in items.items():
            if not item["asked"]:
                print(f"{points}", end=" ")
            else:
                print(f"    ", end="")
        print()


def parse_input(questions, answer_of_user):
    try:
        category, point = answer_of_user.split(" ")
        questions_lower = {key.lower(): value for key, value in questions.items()}
        if category not in questions_lower or point not in questions_lower[category] or questions_lower[category][point]["asked"] == True:
            return None, None, False, questions_lower
        else:
            return category, point, True, questions_lower
    except ValueError:
        return None, None, False, False


def save_results_to_file(user_point, correct_answer, wrong_answers):
        data = {
        "user point": user_point,
        "correct": correct_answer,
        "incorrect": wrong_answers
         }
        with open("answers.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


print("Hello!\nWe invite you to play a game with a playing field!\nExpected input: Category Points\nPress Enter if you are ready")
input()
clear_console()

user_point = 0
correct_answer = 0
wrong_answers = 0

questions = load_questions()

while True:
    is_question = 0
    for category, items in questions.items():
        for points, item in items.items():
            if not item["asked"]:
                is_question += 1

    if is_question == 0:
        print("Well, that's all! We've run out of questions)")
        break

    show_field(questions)
    selected_category = input("Enter your choice: ")
    category, point, correct_input, questions_lower = parse_input(questions, selected_category)

    if not correct_input:
        print("Oops... you entered the wrong value")
    else:
        answer_of_user = input(f"Word {questions_lower[category][point]['question']} from English to Ukrainian means = ")
        questions_lower[category][point]["asked"] = True
       
        if answer_of_user == questions_lower[category][point]["answer"]:
            temp_point = int(point)
            user_point += temp_point
            correct_answer += 1
            print(f"Correct, +{point}. Your points = {user_point}")
        else:
            wrong_answers += 1
            temp_point = int(point)
            user_point -= temp_point
            print(f"Wrong! It actually means {questions_lower[category][point]['answer']}, -{point}. Your points = {user_point}")

    print("Press Enter to continue ...", end = "")
    input()
    clear_console()

show_stats(user_point, correct_answer, wrong_answers)
save_results_to_file(user_point, correct_answer, wrong_answers)