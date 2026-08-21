# Smart-Interview-Coach
A Python-based interview practice application with a GUI, text-to-speech, and keyword-based answer evaluation.
🎤 Smart Interview Coach
📌 Overview
Smart Interview Coach is a Python-based GUI application that helps users practice interview questions and receive intelligent feedback on their answers. The system evaluates responses using basic NLP techniques and also supports voice interaction for a more interactive experience.

🚀 Features
Random interview questions

Automatic question display on startup

Answer input via:

⌨️ Text
🎤 Voice (Speech-to-Text)
🔊 Text-to-Speech (questions are spoken aloud)

Scoring system based on:

Answer length
Keyword matching
Positive tone detection
Feedback generation

Total score and attempt tracking

Response saving using file handling

🛠️ Technologies Used
Python
Tkinter (GUI)
SpeechRecognition (voice input)
pyttsx3 (text-to-speech)
File Handling
Functions, Lists, Dictionaries
👥 Team Members
Member 1 – GUI Development
Member 2 – Logic & Scoring
Member 3 – Data & Questions
Member 4 – Integration & Testing
📂 Project Structure
smart_interview_coach/ │ ├── main.py ├── logic.py ├── questions.py ├── data/ │ └── responses.txt

▶️ How to Run
Open project in VS Code

Install required libraries:

pip install pyttsx3 SpeechRecognition
Run:

python main.py
🎯 Future Scope
AI-based feedback using NLP models
Better speech accuracy and offline support
More interview categories (technical, HR, situational)
Performance analytics dashboard
Web-based version
