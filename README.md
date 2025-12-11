# 🧠 Mental Health Prediction & Chatbot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-1.1.2-orange?logo=flask&logoColor=white">
</p>

A web application built with <strong>Flask</strong> combining <strong>Machine Learning</strong> and a <strong>custom mental health chatbot</strong>.  
Users can predict their mental health score and chat with a supportive AI assistant.

---

## 💡 Features

<ul>
  <li><strong>Mental Health Prediction</strong>
    <ul>
      <li>Algorithm: Multiple Linear Regression</li>
      <li>MSE: 29.91</li>
      <li>R² Score: 0.91</li>
      <li>Predicts mental health scores based on user inputs</li>
    </ul>
  </li>
  <li><strong>Rule-Based Mental Health Chatbot</strong>
    <ul>
      <li>Custom-built in Python using <code>regex</code> for intent detection</li>
      <li>Responds to mental health topics:
        <ul>
          <li>Depression, Anxiety, Stress, Burnout, Loneliness, Sleep, Relationships</li>
        </ul>
      </li>
      <li>Provides coping strategies, mindfulness exercises, and self-care tips</li>
      <li>Prioritizes emergencies and tracks user context</li>
      <li>Handles off-topic and unknown messages</li>
    </ul>
  </li>
  <li><strong>Flask Backend</strong>
    <ul>
      <li>Handles ML predictions and chatbot interactions</li>
      <li>Serves HTML pages for predictions and chat</li>
      <li>Smooth backend integration</li>
    </ul>
  </li>
  <li><strong>Ongoing Upgrades</strong>
    <ul>
      <li>UI/UX improvements</li>
      <li>Advanced NLP chatbot integration</li>
      <li>Additional ML models</li>
      <li>Expanded knowledge base and topics</li>
    </ul>
  </li>
</ul>

---

## 🧠 Chatbot Logic

<details>
  <summary>Click to expand code</summary>

```python
class MentalHealthChatbot:
    def __init__(self):
        self.user_context = {}
        self.responses = self._initialize_responses()
        self.patterns = self._initialize_patterns()
    
    def get_response(self, message, user_id=None):
        # Implementation of chatbot response logic
        pass
```
</details>
⚙️ Installation & Usage
<ol> <li>Clone the repository: <pre><code>git clone https://github.com/atharvp25/mental-health-prediction-and-chatbot.git cd mental-health-prediction-and-chatbot</code></pre> </li> <li>Install dependencies: <pre><code>pip install -r requirements.txt</code></pre> </li> <li>Run the Flask app: <pre><code>python app.py</code></pre> Visit <code>http://127.0.0.1:5000/</code> in your browser </li> </ol>
📊 Machine Learning Model
<table> <tr> <th>Metric</th> <th>Value</th> </tr> <tr> <td>MSE</td> <td>29.91</td> </tr> <tr> <td>R² Score</td> <td>0.91</td> </tr> </table>
🧩 Supported Chatbot Topics
<ul> <li><strong>Mental Health:</strong> Depression, Anxiety, Stress, Burnout, Loneliness</li> <li><strong>Wellbeing:</strong> Mindfulness, Self-care, Gratitude, Positive Thinking</li> <li><strong>Support:</strong> Therapy guidance, Medication info, Crisis resources</li> <li><strong>Other:</strong> Greetings, Farewell, Thanks, Off-topic handling</li> </ul>
🤝 Contributing

Fork the repository, open issues, and submit pull requests. Contributions are welcome!


