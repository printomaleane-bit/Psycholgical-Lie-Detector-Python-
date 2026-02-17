import tkinter as tk
from tkinter import messagebox
from collections import deque

# Normalize answers
def normalize(ans):
    ans = ans.lower()

    positive = [
        "very honest", "mostly honest", "yes",
        "protect feelings", "blame myself"
    ]

    negative = [
        "no", "sometimes dishonest",
        "tell the truth", "blame circumstances"
    ]

    if ans in positive:
        return "YES"
    if ans in negative:
        return "NO"
    return ans


# Question Queue
questions = deque([
    ("honesty", "How would people close to you describe your honesty?",
     ["Very honest", "Mostly honest", "Sometimes dishonest"]),

    ("honesty", "Do you like being honest to people you trust?",
     ["Yes", "No"]),

    ("comfort", "Do you feel comfortable hiding the truth if it avoids conflict?",
     ["Yes", "No"]),

    ("comfort", "Is it better to protect feelings or tell the truth, even if it hurts?",
     ["Protect feelings", "Tell the truth"]),

    ("responsibility", "When something goes wrong, what do you usually do?",
     ["Blame myself", "Blame circumstances"]),

    ("responsibility", "Have you ever avoided admitting responsibility?",
     ["Yes", "No"])
])

answers = {}
contradictions = 0
selected_option = None


def next_question():
    global selected_option

    if not questions:
        show_result()
        return

    trait, text, options = questions.popleft()
    question_label.config(text=text)

    selected_option = tk.StringVar(value="")

    for widget in options_frame.winfo_children():
        widget.destroy()

    for opt in options:
        tk.Radiobutton(
            options_frame,
            text=opt,
            variable=selected_option,
            value=opt,
            font=("Arial", 11)
        ).pack(anchor="w")

    submit_btn.config(command=lambda: submit_answer(trait))


def submit_answer(trait):
    global contradictions

    raw_ans = selected_option.get()
    if raw_ans == "":
        messagebox.showwarning("Select an option", "Please choose an answer")
        return

    norm_ans = normalize(raw_ans)

    if trait in answers and answers[trait] != norm_ans:
        contradictions += 1
    else:
        answers[trait] = norm_ans

    next_question()


def show_result():
    if contradictions == 0:
        verdict = "No psychological contradictions detected"
    elif contradictions == 1:
        verdict = "Minor inconsistency detected"
    else:
        verdict = "Psychological contradiction detected"

    messagebox.showinfo(
        "Analysis Result",
        f"Contradictions Found: {contradictions}\n\nVerdict: {verdict}"
    )

    root.destroy()


# GUI Setup
root = tk.Tk()
root.title("Psychological Lie Detector (Simulation)")
root.geometry("560x420")

tk.Label(
    root,
    text="Psychological Lie Detector",
    font=("Arial", 18, "bold")
).pack(pady=10)

question_label = tk.Label(
    root,
    text="Click Start to Begin",
    font=("Arial", 12),
    wraplength=520
)
question_label.pack(pady=15)

options_frame = tk.Frame(root)
options_frame.pack(pady=10)

submit_btn = tk.Button(
    root,
    text="Start",
    width=15,
    command=next_question
)
submit_btn.pack(pady=15)

root.mainloop()
