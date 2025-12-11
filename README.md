🧠 Mental Health Prediction and Chatbot

A Flask-based web application that predicts mental health scores using Multiple Linear Regression and provides a fully-featured pattern-based mental health chatbot built from scratch in Python.

📌 Overview

This project combines a machine-learning mental health predictor with a smart support-oriented chatbot capable of understanding a wide range of mental-health-related patterns.
Users can predict their mental-health score and chat with an AI assistant to receive guidance, coping strategies, and emotional support.

🚀 Features
🔍 1. Mental Health Prediction (Machine Learning)

Algorithm: Multiple Linear Regression

Model Performance:

MSE: 29.91

R² Score: 0.91

Predicts a mental health score based on multiple input parameters

High accuracy for linear regression

💬 2. Smart Rule-Based Mental Health Chatbot

A highly structured chatbot using:

Regex-based intent detection

Large categorized response system

Context-aware messaging

Emergency keyword detection (highest priority)

Emotionally supportive long-form responses

It can understand and respond to:

✔ Depression
✔ Anxiety & panic
✔ Stress & burnout
✔ Loneliness
✔ Relationship issues
✔ Sleep issues
✔ Coping strategies
✔ Mindfulness
✔ Self-care
✔ Gratitude & positivity
✔ Therapy & medication
✔ Crisis support
✔ Greetings, farewells, thanks
✔ Off-topic input

🛠 3. Built With Flask (Backend)

Flask manages:

User input for ML prediction

Chatbot communication

Page routing

Template rendering

🔧 4. Actively Being Upgraded & Improved

This project is not static — it is actively being enhanced.
Planned upgrades include:

Adding more ML models

Improving UI/UX

Expanding chatbot knowledge

Integrating smarter natural language processing

Adding additional mental health categories

Making the chatbot more personalized


🧠 Chatbot Logic (mental_health_chatbot.py)

The chatbot uses:

class MentalHealthChatbot:
    def __init__(self):
        self.user_context = {}
        self.responses = self._initialize_responses()
        self.patterns = self._initialize_patterns()


It uses:

regex for intent detection

A large library of categorized mental-health responses

Context tracking

Emergency priority checks

Helpful fallback responses

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/atharvp25/mental-health-prediction-and-chatbot.git
cd mental-health-prediction-and-chatbot

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the Flask application
python app.py


Visit:

http://127.0.0.1:5000/

📈 Machine Learning Model Details
Metric	Value
MSE	29.91
R² Score	0.91

The model explains 91% of the variance, showing strong predictive performance.

💡 What the Chatbot Can Assist With
Mental Health Topics

Depression

Anxiety

Stress

Burnout

Loneliness

Relationship issues

Sleep challenges

Wellbeing & Daily Coping

Mindfulness

Self-care routines

Positive thinking

Gratitude exercises

Deep-breathing & grounding techniques

Guidance & Support

Therapy options

Medication information

Helplines & crisis support

🤝 Contributing

Contributions, suggestions, and improvements are welcome.

📜 License

This project is open-source. Feel free to modify and use it.
