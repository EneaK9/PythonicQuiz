import winreg
import os
import random
import csv
import time
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quizz_data import quiz_data

# Function to create quiz results file if it hasn't been created yet or is missing from directory
def create_quiz_results_file(quiz_results):
    if not os.path.exists(quiz_results):
        with open(quiz_results, 'w', newline='') as results:
            results_writer = csv.writer(results)
            results_writer.writerow(['Username', 'Category', 'Score', 'Duration', 'Pass/Fail'])

# Call function to create quiz results file
create_quiz_results_file('quiz_results.csv')

# Function to add results of the quiz to the results file
def add_results(quiz_results, username, category, score, duration, pass_fail):
    with open (quiz_results, 'a', newline='') as results:
        results_writer = csv.writer(results)
        results_writer.writerow([username, category, score, duration, pass_fail])

# Function to display the current question and choices
def show_question():
    # Get the current question from the selected category
    question = current_category["questions"][current_question]
    qs_label.config(text=question["question"])  # Update question label text

    # Display the choices on the buttons
    choices = question["options"]
    random.shuffle(choices)
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal")  # Update choice buttons text

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled")

# Function to check the selected answer and provide feedback
def check_answer(choice):
    # Get the current question from the selected category
    question = current_category["questions"][current_question]
    selected_choice = choice_btns[choice].cget("text")  # Get the text of the selected choice button

    # Check if the selected choice matches the correct answer
    if selected_choice == question["answer"]:
        # Update the score and display it
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(current_category["questions"])))
        feedback_label.config(text="Correct!", foreground="green")
    else: 
        feedback_label.config(text="Incorrect!", foreground="red")

    # Disable all choice buttons and enable the next button
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")
        
# Function to move to the next question
def next_question():
    global current_question
    global score
    global start_time
    global end_time
    global quiz_duration
    global username
    global current_category_name
    current_question += 1
    if current_question < len(current_category["questions"]):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score and time and end the quiz
        end_time = time.time()
        quiz_duration = int(end_time - start_time)
        if score/len(current_category["questions"]) >= 0.6:
            add_results('quiz_results.csv', username, current_category_name, score, quiz_duration, pass_fail='Pass')
            messagebox.showinfo("Quiz Complete! ", "You finished the quiz in {} seconds. You have passed the quiz with a score of {}/{}.".format(quiz_duration, score, len(current_category["questions"])))
            root.destroy()
        else:
            add_results('quiz_results.csv', username, current_category_name, score, quiz_duration, pass_fail='Fail')
            messagebox.showinfo("Quiz Complete! ", "You finished the quiz in {} seconds. You have failed the quiz with a score of {}/{}. \nA score of 60% or more is required to pass.".format(quiz_duration, score, len(current_category["questions"])))
            retry = messagebox.askquestion("Retry?", "Would you like to retake the quiz?", icon="question")
            if retry == "yes":
                restart_quiz()
            else:
                root.destroy()

# Function to start the quiz with the selected category
def start_quiz(category_index):
    global current_category
    global start_time
    global current_category_name
    start_time = time.time()
    current_category_name = categories[category_index]
    current_category = quiz_data[category_index]  # Get the selected category
    category_frame.pack_forget()  # Hide category selection frame
    quiz_frame.pack()  # Show quiz frame
    random.shuffle(current_category["questions"]) # Shuffle the question bank
    show_question()  # Show the first question

# Function to restart the quiz with the previously selected category
def restart_quiz():
    global score
    global current_question
    global current_category
    global start_time
    global end_time
    global quiz_duration
    start_time = time.time()
    end_time = 0
    quiz_duration = 0
    random.shuffle(current_category["questions"])
    score = 0
    current_question = 0
    score_label.config(text="Score: {}/{}".format(score, len(current_category["questions"])))
    show_question()

# Detect the system's theme preference
def detect_system_preference():
    registry_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
            value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
            return "light" if value == 1 else "dark"
    except FileNotFoundError:
        # Key not found, unable to determine preference
        return "unknown"
    
# Function for submitting username
def submit_username():
    global username
    username = username_field.get()
    # Username frame is hidden and the cateory selection frame shows up
    username_frame.pack_forget()
    category_frame.pack()

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("800x600")

# Set the style theme based on the user's system preference
theme_preference = detect_system_preference()
if theme_preference == "light":
    style = Style(theme="flatly")
else:
    style = Style(theme="darkly")

# Configure font size for labels and buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Create frames for username creation, category selection and quiz
category_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)
username_frame = tk.Frame(root)

# Create label for username creation
username_label = ttk.Label(username_frame, text="Please enter a username").pack(pady=10)

# Create a text field widget for the username creation
username_field = ttk.Entry(username_frame, font = ("Helvetica", 16), width = 30)
username_field.pack(pady=10)

#Create a button to submit the username
username_submit_bttn = ttk.Button(username_frame, text="Submit", command=submit_username).pack(pady=10)

# Pack the username creation frame
username_frame.pack(pady=180)

# Initialize username as a blank string
username = ''

# Create label for category selection
tk.Label(category_frame, text="Please select a category", font=("Helvetica", 16)).pack(pady=10)

# Create label for question display
qs_label = ttk.Label(quiz_frame, anchor="center", wraplength=500, padding=10)
qs_label.pack(pady=10)

# Create choice buttons for answers
choice_btns = []
for i in range(4):
    button = ttk.Button(quiz_frame, command=lambda i=i: check_answer(i))
    button.pack(pady=5)
    choice_btns.append(button)

# Create label for feedback
feedback_label = ttk.Label(quiz_frame, anchor="center", padding=10)
feedback_label.pack(pady=10)

# Initialize score
score = 0
score_label = ttk.Label(quiz_frame, text="Score: 0/0", anchor="center", padding=10)
score_label.pack(pady=10)

# Create next button for navigating to the next question
next_btn = ttk.Button(quiz_frame, text="Next", command=next_question, state="disabled")
next_btn.pack(pady=10)

# Initialize current question index
current_question = 0
current_category = None
current_category_name = ''

# Create buttons for selecting category
categories = [category["category"] for category in quiz_data]
for i, category_name in enumerate(categories):
    button = ttk.Button(category_frame, text=category_name, command=lambda i=i: start_quiz(i))
    button.pack(pady=5)

# Initialize start and end times for the quiz, and the duration
start_time = 0
end_time = 0
quiz_duration = 0

# Start the GUI event loop
root.mainloop()
