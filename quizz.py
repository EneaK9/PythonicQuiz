#The file to start the project for ANDRRA Academy 

import json
import random

class QuizCategory:
    def __init__(self, category_name):
        self.category_name = category_name
        self.questions = self.load_questions()

    def load_questions(self):
        with open('quiz_data_multichoice.json', 'r') as file: # quiz_data_multichoice it's a sample file I used to see how to quiz works
            data = json.load(file)
        return data.get(self.category_name, [])

    def run(self):
        score = 0
        random.shuffle(self.questions)  

        for question in self.questions:
            print(f"\n{question['question']}")
            for i, option in enumerate(question['options'], start=1):
                print(f"{i}. {option}")

            while True:  # Keep asking until a valid input is given
                try:
                    user_choice = int(input("Your answer (1-4): ")) - 1
                    if user_choice < 0 or user_choice >= len(question['options']):
                        print(f"Please enter a number between 1 and {len(question['options'])}.")
                        continue  # Ask for input again if it's out of range
                    break  # Exit the loop if input is valid
                except ValueError:
                    print("Please enter a valid number.")

            if question['options'][user_choice] == question['answer']:
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
            print(f"Explanation: {question['explanation']}\n")

        print(f"Your score in {self.category_name}: {score}/{len(self.questions)}")

def load_categories():
    with open('quiz_data_multichoice.json', 'r') as file:
        data = json.load(file)
    return list(data.keys())

def main():
    categories = load_categories()
    print("Available categories:")
    for category in categories:
        print(category)

    chosen_category = input("\nChoose a category: ").strip()
    if chosen_category in categories:
        quiz = QuizCategory(chosen_category)
        quiz.run()
    else:
        print("Invalid category.")

if __name__ == "__main__":
    main()
