import winreg
import random
import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quizz_data import quiz_data

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
    current_question += 1
    if current_question < len(current_category["questions"]):
        # If there are more questions, show the next question
        show_question()
    else:
        # If all questions have been answered, display the final score and end the quiz
        if score/len(current_category["questions"]) >= 0.6:
            messagebox.showinfo("Quiz Complete! ", "You have passed the quiz with a score of {}/{}".format(score, len(current_category["questions"])))
        else:
            messagebox.showinfo("Quiz Complete! ", "You have failed the quiz with a score of {}/{}. \nA score of 60% or more is required to pass.".format(score, len(current_category["questions"])))
            retry = messagebox.askquestion("Retry?", "Would you like to retake the quiz?", icon="question")
            if retry == "yes":
                restart_quiz()
            else:
                root.destroy()

# Function to start the quiz with the selected category
def start_quiz(category_index):
    global current_category
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

# Create frames for category selection and quiz
category_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)

# Create label for category selection
tk.Label(category_frame, text="Please select a category:", font=("Helvetica", 16)).pack(pady=10)

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

# Create buttons for selecting category
categories = [category["category"] for category in quiz_data]
for i, category_name in enumerate(categories):
    button = ttk.Button(category_frame, text=category_name, command=lambda i=i: start_quiz(i))
    button.pack(pady=5)

# Pack the category selection frame
category_frame.pack()

# Start the GUI event loop
root.mainloop()
