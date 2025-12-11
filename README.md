🧠 Mental Health Prediction & Chatbot

A Flask-based web application that predicts mental health scores using Multiple Linear Regression and includes a smart rule-based mental health chatbot built entirely in Python.

📌 Overview

This project blends Machine Learning with a pattern-matching mental health chatbot to help users understand their mental wellbeing and receive supportive guidance.

Users can:

Predict their mental health score

Chat with a supportive assistant

Learn coping strategies & mindfulness practices

Receive helpful emotional wellbeing insights

🚀 Features
🔍 1. Mental Health Prediction (Machine Learning)

Model: Multiple Linear Regression

Performance Metrics:

MSE: 29.91

R² Score: 0.91

Predicts a mental-health index based on user inputs

High accuracy for a linear model

💬 2. Smart Rule-Based Mental Health Chatbot

This chatbot is built using regex-based intent detection, not simple if-else.
It contains a large library of categorized responses and offers supportive, long-form mental health guidance.

The chatbot can understand and respond to:

🧠 Mental Health Topics

Depression

Anxiety

Stress

Burnout

Loneliness

Sleep issues

Relationship issues

🌿 Wellbeing & Coping

Mindfulness

Self-care

Gratitude

Grounding techniques

Positive thinking

📘 Support & Guidance

Therapy information

Medication basics

Crisis helplines

General emotional support

⚠️ Special Handling

Emergency keyword detection (highest priority)

User context tracking

Off-topic detection

Clean fallback responses

🌐 3. Flask Backend

Flask handles:

User input for ML prediction

Chatbot message routing

Page rendering

Smooth connection between chatbot and UI

🔧 4. Ongoing Improvements

This project is actively being improved. Planned upgrades include:

Better UI/UX

Additional ML models

A more advanced NLP-based chatbot

More mental-health categories

Personalized suggestions

🧠 Chatbot Logic (Brief Overview)
class MentalHealthChatbot:
    def __init__(self):
        self.user_context = {}
        self.responses = self._initialize_responses()
        self.patterns = self._initialize_patterns()


✔ Uses regex for detecting intent
✔ Has detailed mental health explanations
✔ Supports contextual replies
✔ Prioritizes emergency messages

⚙️ Installation & Usage
1️⃣ Clone the Repository
git clone https://github.com/atharvp25/mental-health-prediction-and-chatbot.git
cd mental-health-prediction-and-chatbot

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Run the Flask App
python app.py


Visit the app at:
👉 http://127.0.0.1:5000/

📈 Machine Learning Model Details
Metric	Value
MSE	29.91
R² Score	0.91

A strong score indicating that the model explains 91% of dataset variance.

🤝 Contribution

Feel free to fork the project, open issues, or submit pull requests.

📜 License

This project is open-source. You’re free to use and modify it.
