import tkinter as tk
import random
from tkinter import messagebox

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BSI - Kryminalne Zagadki Polibudy")
        self.root.geometry("900x800")

        self.questions = self.load_questions("pyta.dat")
        self.current_question = None
        self.checkboxes = []
        self.vars = []
        # self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.question_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=400, justify='center')
        self.checkVar = tk.IntVar(value=1)

        self.question_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        self.answers_frame = tk.Frame(root)
        self.answers_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky='wesn')

        self.checkboxes_frame = tk.Frame(self.answers_frame)
        self.checkboxes_frame.pack(fill='x')

        # self.answers_frame.grid_rowconfigure(0, weight=1)
        self.answers_frame.grid_columnconfigure(0, weight=1)

        self.info_label = tk.Label(root, text="Naciśnij:\n Strzałka w górę - losuj pytanie.\nStrzałka w dół - sprawdź odpowiedź.\nStrzałka w lewo - poprzednie pytanie.\nStrzałka w prawo - następne pytanie.\nBackspace - wroc do poczatku.", font=("Arial", 10), wraplength=400, justify='center')
        self.info_label.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        self.first_question()
        self.bind_keys()


    def load_questions(self, filename):
        questions = []
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split("*")
                question = parts[0]
                all_answers = parts[1:]
                correct_answers = [answer.replace('[X]', '') for answer in all_answers if '[X]' in answer]
                questions.append((question, all_answers, correct_answers))
        return questions

    def first_question(self):
        self.current_question = self.questions[0]
        self.update_question()

    def random_question(self):
        self.current_question = random.choice(self.questions)
        self.update_question()
    
    def update_question(self):
        question_text = self.current_question[0]
        self.question_label.config(text=question_text)

        for cb in self.checkboxes:
            cb.destroy()
        self.checkboxes.clear()
        self.vars.clear()

        answers_with_vars = []
        for answer in self.current_question[1]:
            clean_answer = answer.replace('[X]', '') 
            var = tk.BooleanVar()
            answers_with_vars.append((clean_answer, var))

        random.shuffle(answers_with_vars)

        for clean_answer, var in answers_with_vars:
            cb = tk.Checkbutton(self.checkboxes_frame, text=clean_answer, variable=var, wraplength=400, justify='left', font=("Helvetica", 12))
            cb.pack(anchor='w')
            self.checkboxes.append(cb)
            self.vars.append(var)


    def check_answer(self):
        for cb, var in zip(self.checkboxes, self.vars):
            answer_text = cb.cget("text") 
            is_correct = answer_text in self.current_question[2]
            if is_correct:
                cb.config(fg="green", font=("Helvetica", 12, "bold"), variable=self.checkVar)
            else:
                cb.config(fg="black", state="disabled")


    def next_question(self):
        current_index = self.questions.index(self.current_question)
        next_index = (current_index + 1) % len(self.questions)
        self.current_question = self.questions[next_index]
        self.update_question()

    def prev_question(self):
        current_index = self.questions.index(self.current_question)
        prev_index = (current_index - 1) % len(self.questions)
        self.current_question = self.questions[prev_index]
        self.update_question()
        
    def bind_keys(self):
        self.root.bind("<Right>", lambda event: self.next_question())
        self.root.bind("<Left>", lambda event: self.prev_question())
        self.root.bind("<Down>", lambda event: self.check_answer())
        self.root.bind("<Up>", lambda event: self.random_question())
        self.root.bind("<BackSpace>", lambda event: self.first_question())

root = tk.Tk()
app = QuizApp(root)
root.mainloop()
