import tkinter as tk
import random
import pyttsx3
import speech_recognition as sr
import os

# ---------------- TEXT TO SPEECH SETUP ----------------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- QUESTIONS + KEYWORDS ----------------
questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "Why should we hire you?",
    "Describe a challenge you faced.",
    "Tell me about a team project."
]

keywords = {
    "Tell me about yourself.": ["student", "skills", "experience"],
    "What are your strengths?": ["hardworking", "team", "learning"],
    "Why should we hire you?": ["skills", "value", "contribute"],
    "Describe a challenge you faced.": ["problem", "solution", "learned"],
    "Tell me about a team project.": ["team", "role", "collaboration"]
}

model_answers = {
    "Tell me about yourself.": "I am a motivated student with strong skills and a passion for learning. I have worked on projects that improved my problem-solving abilities.",
    
    "What are your strengths?": "My strengths include teamwork, adaptability, and continuous learning. I stay focused and always try to improve my skills.",
    
    "Why should we hire you?": "You should hire me because I bring dedication, relevant skills, and a willingness to contribute positively to the organization.",
    
    "Describe a challenge you faced.": "I faced a challenge where I had to solve a difficult problem. I analyzed the situation, found a solution, and learned valuable lessons.",
    
    "Tell me about a team project.": "In a team project, I contributed actively, communicated effectively, and ensured collaboration to achieve our goal."
}

# ---------------- ANALYSIS FUNCTION ----------------
def analyze_answer(answer, question, keywords):
    score = 0
    feedback = []

    words = answer.split()

    # Length check
    if len(words) < 10:
        feedback.append("Answer is too short. Try to elaborate.")
    elif len(words) > 30:
        feedback.append("Good detailed answer.")
        score += 2
    else:
        feedback.append("Decent length.")
        score += 1

    # Keyword check
    matched = 0
    for word in keywords.get(question, []):
        if word in answer.lower():
            matched += 1

    if matched >= 2:
        feedback.append("Good use of relevant keywords.")
        score += 2
    elif matched == 1:
        feedback.append("Try adding more relevant points.")
        score += 1
    else:
        feedback.append("Answer lacks important keywords.")

    # Positive tone check
    positive_words = ["confident", "achieved", "success", "improved"]

    for word in positive_words:
        if word in answer.lower():
            feedback.append("Positive tone detected.")
            score += 1
            break

    return score, feedback

# ---------------- GLOBAL VARIABLES ----------------
current_question = ""
total_score = 0
attempts = 0

# ---------------- FUNCTIONS ----------------
def get_question():
    global current_question

    new_question = random.choice(questions)

    # prevent same question repeating
    while new_question == current_question:
        new_question = random.choice(questions)

    current_question = new_question

    question_label.config(text=current_question)
    answer_box.delete("1.0", tk.END)
    result_label.config(text="")

    speak(current_question)


def submit_answer():
    global total_score, attempts

    answer = answer_box.get("1.0", tk.END).strip()

    if answer == "":
        result_label.config(text="Please enter an answer.")
        return

    score, feedback = analyze_answer(answer, current_question, keywords)

    total_score += score
    attempts += 1

    result_text = f"Score: {score}/5\n\n"
    result_text += "\n".join(feedback)

    result_label.config(text=result_text)
    
    if score >= 4:
        result_label.config(fg=GREEN)
    elif score <= 2:
        result_label.config(fg=RED)
    else:
        result_label.config(fg=TEXT)

    overall_label.config(text=f"Total Score: {total_score} | Attempts: {attempts}")

    # Ensure folder exists
    os.makedirs("data", exist_ok=True)

    # Save to file
    with open("data/responses.txt", "a") as file:
        file.write(f"Q: {current_question}\n")
        file.write(f"A: {answer}\n")
        file.write(f"Score: {score}\n\n")


def record_answer():
    recognizer = sr.Recognizer()

    # 🔥 ADD IT HERE
    recognizer.pause_threshold = 1.2

    with sr.Microphone() as source:
        result_label.config(text="🎤 Get ready... Recording starts in 2 seconds")
        root.update()

        import time
        time.sleep(2)

        recognizer.adjust_for_ambient_noise(source, duration=1)

        result_label.config(text="🎤 Speak now...")
        root.update()

        try:
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=30
            )

            result_label.config(text="Processing...")
            root.update()

            text = recognizer.recognize_google(audio, language="en-IN")

            answer_box.delete("1.0", tk.END)
            answer_box.insert(tk.END, text)

            result_label.config(
                text="Captured! You can edit the answer if needed."
            )

        except sr.WaitTimeoutError:
            result_label.config(text="No speech detected.")
        except sr.UnknownValueError:
            result_label.config(text="Could not understand clearly.")
        except sr.RequestError:
            result_label.config(text="Network error.")

def show_model_answer():
    if current_question == "":
        result_label.config(text="No question selected.")
        return

    key = current_question.strip()
    answer = model_answers.get(key)

    if answer:
        result_label.config(text=f"📘 Model Answer:\n\n{answer}")
    else:
        result_label.config(text="Model answer not found. Check question text.")

# ---------------- GUI SETUP ----------------
# ---------------- GUI SETUP ----------------
BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#a78bfa"
BTN = "#334155"
BTN_HOVER = "#475569"
GREEN = "#4ade80"
RED = "#f87171"

root = tk.Tk()
root.title("Smart Interview Coach")
root.geometry("720x680")
root.configure(bg=BG)

# ---------------- HOVER EFFECT ----------------
def on_enter(e):
    e.widget['bg'] = BTN_HOVER

def on_leave(e):
    e.widget['bg'] = BTN

# ---------------- TITLE ----------------
title = tk.Label(root, text="🎤 Smart Interview Coach",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=ACCENT)
title.pack(pady=(10, 2))

tagline = tk.Label(root, text="Practice. Improve. Succeed.",
                   font=("Segoe UI", 10, "italic"),
                   bg=BG, fg=TEXT)
tagline.pack(pady=(0, 10))

tk.Frame(root, bg=ACCENT, height=2).pack(fill="x", padx=120, pady=5)

# ---------------- PROGRESS ----------------
progress_label = tk.Label(root, text="Question 1",
                          font=("Segoe UI", 10),
                          bg=BG, fg=TEXT)
progress_label.pack(pady=5)

# ---------------- QUESTION CARD ----------------
q_frame = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
q_frame.pack(padx=20, pady=10, fill="x")

question_label = tk.Label(q_frame,
    text="Click Next Question",
    font=("Segoe UI", 12),
    bg=CARD, fg=TEXT,
    wraplength=550,
    padx=10, pady=10)
question_label.pack()

# ---------------- ANSWER ----------------
answer_title = tk.Label(root, text="Your Answer:",
                        font=("Segoe UI", 11, "bold"),
                        bg=BG, fg=TEXT)
answer_title.pack(anchor="w", padx=20)

answer_box = tk.Text(root, height=5,
                     bg="#020617",
                     fg=TEXT,
                     insertbackground="white",
                     font=("Segoe UI", 10))
answer_box.pack(pady=5, padx=20, fill="x")

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

def make_btn(text, command):
    btn = tk.Button(btn_frame, text=text,
                    command=command,
                    bg=BTN, fg="white",
                    activebackground=BTN_HOVER,
                    bd=0, padx=12, pady=6,
                    font=("Segoe UI", 9, "bold"))
    btn.pack(side="left", padx=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

make_btn("➡ Next", get_question)
make_btn("🎤 Speak", record_answer)
make_btn("✨ Evaluate", submit_answer)
make_btn("📘 Model", show_model_answer)

# ---------------- FEEDBACK ----------------
result_label = tk.Label(root,
    text="Feedback will appear here...",
    wraplength=550,
    justify="left",
    font=("Segoe UI", 10),
    bg=CARD, fg=TEXT,
    padx=12, pady=12)
result_label.pack(pady=10, padx=20, fill="x")

# ---------------- SCORE ----------------
overall_label = tk.Label(root,
    text="⭐ Average Score: 0.0/5 | Attempts: 0",
    font=("Segoe UI", 11, "bold"),
    bg=BG, fg=ACCENT)
overall_label.pack(pady=10)

# ---------------- RUN ----------------
get_question()
root.mainloop()