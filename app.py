from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
from datetime import datetime
import os

# Import the custom chatbot
from chat_bot import mental_health_bot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mental-health-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mental_health_score = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    physical_activity = db.Column(db.Float, nullable=False)
    work_hours = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    smoking_status = db.Column(db.Integer, nullable=False)
    alcohol_consumption = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ML Model Manager
class MLModelManager:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained ML model"""
        try:
            if os.path.exists('model\mental_health_model.pkl'):
                with open('model\mental_health_model.pkl', 'rb') as f:
                    model_data = pickle.load(f)
                
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.feature_names = model_data['feature_names']
                self.model_loaded = True
                print("✅ ML Model loaded successfully!")
                print(f"📊 Model features: {self.feature_names}")
            else:
                print("❌ Model file 'mental_health_model.pkl' not found!")
                self.model_loaded = False
                
        except Exception as e:
            print(f"❌ Model loading error: {e}")
            self.model_loaded = False
    
    def preprocess_features(self, features_dict):
        """Preprocess features for prediction"""
        try:
            # Convert form data to feature array in correct order
            features = np.array([[
                features_dict['age'],
                features_dict['gender'],
                features_dict['sleep_hours'],
                features_dict['physical_activity'],
                features_dict['work_hours'], 
                features_dict['screen_time'],
                features_dict['smoking_status'],
                features_dict['alcohol_consumption']
            ]])
            
            print(f"🔍 Raw features: {features[0]}")
            
            # Apply scaling
            if self.scaler:
                features = self.scaler.transform(features)
                print(f"📊 Scaled features: {features[0]}")
            
            return features
            
        except Exception as e:
            print(f"❌ Feature preprocessing error: {e}")
            return None
    
    def predict(self, features_dict):
        """Make prediction using the loaded model"""
        if not self.model_loaded:
            print("❌ Model not loaded, using fallback")
            return self._fallback_prediction(features_dict)
        
        try:
            features = self.preprocess_features(features_dict)
            if features is None:
                return self._fallback_prediction(features_dict)
                
            prediction = self.model.predict(features)[0]
            final_score = max(0, min(100, prediction))
            
            print(f"📈 ML Prediction: {final_score}")
            return round(final_score, 2)
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return self._fallback_prediction(features_dict)
    
    def _fallback_prediction(self, features_dict):
        """Fallback prediction when model fails"""
        try:
            age = features_dict['age']
            sleep_hours = features_dict['sleep_hours']
            physical_activity = features_dict['physical_activity']
            work_hours = features_dict['work_hours']
            screen_time = features_dict['screen_time']
            smoking = features_dict['smoking_status']
            alcohol = features_dict['alcohol_consumption']
            
            # Simple scoring logic
            base_score = 65
            sleep_score = max(-20, min(20, (sleep_hours - 6) * 5))
            activity_score = min(15, physical_activity / 10)
            work_score = -max(0, work_hours - 40) * 0.5
            screen_score = -screen_time * 1.2
            habit_score = -(smoking * 4 + alcohol * 2)
            
            final_score = base_score + sleep_score + activity_score + work_score + screen_score + habit_score
            fallback_score = max(0, min(100, round(final_score, 2)))
            
            print(f"🔄 Fallback prediction: {fallback_score}")
            return fallback_score
            
        except:
            return 65.0

# Initialize ML Model Manager
ml_manager = MLModelManager()

# Score Interpretation Function
def interpret_score(score):
    if score >= 80:
        return {
            'level': 'Excellent',
            'color': 'success',
            'icon': 'star',
            'message': 'Your mental health is in great shape! Keep up the good habits.',
            'gradient': 'linear-gradient(90deg, #28a745, #20c997)',
            'recommendations': [
                {'title': 'Maintain Routine', 'description': 'Continue your current healthy habits'},
                {'title': 'Help Others', 'description': 'Share your positive strategies with others'},
                {'title': 'Set New Goals', 'description': 'Challenge yourself with new mental wellness goals'}
            ]
        }
    elif score >= 65:
        return {
            'level': 'Good', 
            'color': 'info',
            'icon': 'thumbs-up',
            'message': 'You\'re doing well overall. Small improvements can make a big difference.',
            'gradient': 'linear-gradient(90deg, #17a2b8, #6f42c1)',
            'recommendations': [
                {'title': 'Sleep Quality', 'description': 'Focus on consistent sleep schedule'},
                {'title': 'Social Connections', 'description': 'Strengthen your support network'},
                {'title': 'Mindfulness', 'description': 'Practice daily meditation or breathing'}
            ]
        }
    elif score >= 50:
        return {
            'level': 'Fair',
            'color': 'warning', 
            'icon': 'exclamation-triangle',
            'message': 'There\'s room for improvement. Consider focusing on self-care.',
            'gradient': 'linear-gradient(90deg, #ffc107, #fd7e14)',
            'recommendations': [
                {'title': 'Professional Support', 'description': 'Consider talking to a mental health professional'},
                {'title': 'Exercise Routine', 'description': 'Increase physical activity gradually'},
                {'title': 'Digital Detox', 'description': 'Reduce screen time and social media use'}
            ]
        }
    else:
        return {
            'level': 'Needs Attention',
            'color': 'danger',
            'icon': 'heart',
            'message': 'Your mental health needs attention. Please consider seeking support.',
            'gradient': 'linear-gradient(90deg, #dc3545, #e83e8c)',
            'recommendations': [
                {'title': 'Immediate Support', 'description': 'Reach out to mental health professionals'},
                {'title': 'Crisis Resources', 'description': 'Use emergency resources if needed'},
                {'title': 'Daily Self-Care', 'description': 'Focus on basic self-care activities'}
            ]
        }

# Make interpret_score available in templates
@app.context_processor
def utility_processor():
    return dict(interpret_score=interpret_score)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            name = request.form['name']
            gender = request.form['gender']
            age = int(request.form['age'])
            
            print(f"🔍 Registration attempt - Username: {username}, Email: {email}")
            
            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect(url_for('register'))
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return redirect(url_for('register'))
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered!', 'error')
                return redirect(url_for('register'))
            
            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username, 
                email=email, 
                password=hashed_password,
                name=name, 
                gender=gender, 
                age=age
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            print(f"✅ User registered successfully: {username}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except KeyError as e:
            print(f"❌ Missing form field: {e}")
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('register'))
        except Exception as e:
            print(f"❌ Registration error: {e}")
            flash('Error during registration. Please try again.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            print(f"🔍 Login attempt - Username: {username}")
            
            user = User.query.filter_by(username=username).first()
            
            if user:
                print(f"✅ User found: {user.username}")
                if check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    session['username'] = user.username
                    session['name'] = user.name
                    print(f"✅ Login successful for: {user.name}")
                    flash(f'Welcome back, {user.name}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    print("❌ Password incorrect")
                    flash('Invalid password!', 'error')
            else:
                print("❌ User not found")
                flash('Username not found!', 'error')
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            flash('Error during login. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    recent_predictions = Prediction.query.filter_by(user_id=session['user_id']).order_by(Prediction.created_at.desc()).limit(3).all()
    return render_template('dashboard.html', user=user, predictions=recent_predictions)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender_str = request.form['gender']
            sleep_hours = float(request.form['sleep_hours'])
            physical_activity = float(request.form['physical_activity'])
            work_hours = float(request.form['work_hours'])
            screen_time = float(request.form['screen_time'])
            smoking_str = request.form['smoking_status']
            alcohol_str = request.form['alcohol_consumption']
            
            # Convert categorical values to numeric
            gender_map = {'Male': 0, 'Female': 1, 'Non-binary': 2}
            smoking_map = {'Never': 0, 'Former': 1, 'Current': 2}
            alcohol_map = {'Never': 0, 'Occasional': 1, 'Moderate': 2, 'Heavy': 3}
            
            gender = gender_map.get(gender_str, 0)
            smoking_status = smoking_map.get(smoking_str, 0)
            alcohol_consumption = alcohol_map.get(alcohol_str, 0)
            
            # Prepare features dictionary
            features_dict = {
                'age': age,
                'gender': gender,
                'sleep_hours': sleep_hours,
                'physical_activity': physical_activity,
                'work_hours': work_hours,
                'screen_time': screen_time,
                'smoking_status': smoking_status,
                'alcohol_consumption': alcohol_consumption
            }
            
            print(f"🎯 Making prediction with features: {features_dict}")
            
            # Get prediction from ML manager
            mental_health_score = ml_manager.predict(features_dict)
            
            print(f"✅ Final prediction score: {mental_health_score}")
            
            # Save prediction to database
            prediction = Prediction(
                user_id=session['user_id'],
                mental_health_score=mental_health_score,
                age=age, gender=gender, sleep_hours=sleep_hours,
                physical_activity=physical_activity, work_hours=work_hours,
                screen_time=screen_time, smoking_status=smoking_status,
                alcohol_consumption=alcohol_consumption
            )
            
            db.session.add(prediction)
            db.session.commit()
            
            return render_template('result.html', 
                                 score=mental_health_score,
                                 user_input=request.form)
            
        except Exception as e:
            print(f"❌ Prediction form error: {e}")
            flash('Error processing your prediction. Please try again.', 'error')
            return redirect(url_for('predict'))
    
    return render_template('predict.html')

@app.route('/old')
def old():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    predictions = Prediction.query.filter_by(user_id=session['user_id']).order_by(Prediction.created_at.desc()).all()
    
    gender_map = {0: 'Male', 1: 'Female', 2: 'Non-binary'}
    smoking_map = {0: 'Never', 1: 'Former', 2: 'Current'}
    alcohol_map = {0: 'Never', 1: 'Occasional', 2: 'Moderate', 3: 'Heavy'}
    
    for pred in predictions:
        pred.gender_label = gender_map[pred.gender]
        pred.smoking_label = smoking_map[pred.smoking_status]
        pred.alcohol_label = alcohol_map[pred.alcohol_consumption]
    
    return render_template('old.html', predictions=predictions)

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_message = request.json.get('message', '')
    user_id = session['user_id']
    
    if not user_message.strip():
        return jsonify({'response': "I'm here to listen. Please share what's on your mind."})
    
    try:
        # Get response from the comprehensive chatbot
        bot_response = mental_health_bot.get_response(user_message, user_id)
        return jsonify({'response': bot_response})
    
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return jsonify({'response': "I'm having trouble responding right now. Please try again."})

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'ml_model_loaded': ml_manager.model_loaded,
        'database_connected': True,
        'users_count': User.query.count(),
        'predictions_count': Prediction.query.count(),
        'chatbot_ready': True,
        'timestamp': datetime.utcnow().isoformat()
    })

# Debug route to test model
@app.route('/debug-model')
def debug_model():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Test with sample data
    test_data_good = {
        'age': 30,
        'gender': 1,  # Female
        'sleep_hours': 8.0,
        'physical_activity': 300.0,
        'work_hours': 40.0,
        'screen_time': 4.0,
        'smoking_status': 0,  # Never
        'alcohol_consumption': 1  # Occasional
    }
    
    test_data_poor = {
        'age': 30,
        'gender': 0,  # Male
        'sleep_hours': 4.0,
        'physical_activity': 30.0,
        'work_hours': 60.0,
        'screen_time': 12.0,
        'smoking_status': 2,  # Current
        'alcohol_consumption': 3  # Heavy
    }
    
    good_score = ml_manager.predict(test_data_good)
    poor_score = ml_manager.predict(test_data_poor)
    
    return f"""
    <h2>Model Debug Information</h2>
    <p><strong>Model Loaded:</strong> {ml_manager.model_loaded}</p>
    <p><strong>Model Type:</strong> {type(ml_manager.model) if ml_manager.model_loaded else 'N/A'}</p>
    
    <h3>Test Predictions:</h3>
    <p><strong>Good Lifestyle Score:</strong> {good_score}</p>
    <p><strong>Poor Lifestyle Score:</strong> {poor_score}</p>
    
    <p><em>Good lifestyle should score higher than poor lifestyle.</em></p>
    <a href="/dashboard">Back to Dashboard</a>
    """

# Debug routes for database
@app.route('/debug-users')
def debug_users():
    """Check all users in database"""
    users = User.query.all()
    result = "<h2>Users in Database:</h2><ul>"
    for user in users:
        result += f"<li>ID: {user.id}, Username: {user.username}, Email: {user.email}, Name: {user.name}</li>"
    result += "</ul>"
    result += f"<p>Total users: {len(users)}</p>"
    result += '<a href="/register">Go to Registration</a> | <a href="/">Home</a>'
    return result

@app.route('/create-test-user')
def create_test_user():
    """Create a test user for debugging"""
    try:
        # Check if test user already exists
        test_user = User.query.filter_by(username='test').first()
        if test_user:
            return """
            <h2>Test User Already Exists!</h2>
            <p>Try logging in with:</p>
            <p><strong>Username:</strong> test</p>
            <p><strong>Password:</strong> test123</p>
            <p><a href="/login">Go to Login</a></p>
            <p><a href="/debug-users">Check All Users</a></p>
            """
        
        # Create test user
        hashed_password = generate_password_hash('test123')
        new_user = User(
            username='test',
            email='test@example.com',
            password=hashed_password,
            name='Test User',
            gender='Male',
            age=25
        )
        
        db.session.add(new_user)
        db.session.commit()
        return """
        <h2>✅ Test User Created!</h2>
        <p><strong>Username:</strong> test</p>
        <p><strong>Password:</strong> test123</p>
        <p><a href="/login">Go to Login</a></p>
        <p><a href="/debug-users">Check All Users</a></p>
        """
        
    except Exception as e:
        return f"<h2>❌ Error creating test user: {e}</h2>"

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database initialized!")
    print(f"👥 Current users: {User.query.count()}")
    print(f"📊 Current predictions: {Prediction.query.count()}")

if __name__ == '__main__':
    print("🚀 Starting Mental Health Prediction App...")
    print("🤖 ML Model Status:", "✅ Loaded" if ml_manager.model_loaded else "❌ Not Loaded")
    print("💬 Custom Chatbot: ✅ Ready (chat_bot.py)")
    print("🗄️ Database: mental_health.db")
    print("🌐 Web Server: http://localhost:5000")
    print("\n📋 Important Routes:")
    print("   - /create-test-user  -> Create test user (if no users)")
    print("   - /debug-users       -> Check all users")
    print("   - /register          -> Register new user")
    print("   - /predict           -> Make predictions")
    print("   - /chatbot           -> Mental Health Chatbot")
    print("\n⚡ Starting Flask server...")
    
    app.run(debug=True, port=5000)