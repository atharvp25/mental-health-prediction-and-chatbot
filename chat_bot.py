# mental_health_chatbot.py
import re
import random
from datetime import datetime

class MentalHealthChatbot:
    def __init__(self):
        self.user_context = {}
        self.responses = self._initialize_responses()
        self.patterns = self._initialize_patterns()
    
    def _initialize_responses(self):
        """Initialize all chatbot responses and knowledge base"""
        return {
            # Greetings and Basic Interactions
            'greeting': [
                "Hello! I'm your mental health support assistant. How are you feeling today?",
                "Hi there! I'm here to listen and support you. What's on your mind?",
                "Welcome! I'm your mental health companion. How can I help you today?"
            ],
            
            'farewell': [
                "Take care of yourself! Remember, I'm here whenever you need to talk.",
                "Goodbye! Don't hesitate to reach out if you need support.",
                "Take care! Your mental health matters. Come back anytime."
            ],
            
            'thanks': [
                "You're welcome! I'm glad I could help.",
                "No problem at all! I'm here for you.",
                "You're welcome! Remember to be kind to yourself today."
            ],
            
            # Mental Health Conditions
            'depression': [
                """Depression is more than just feeling sad. It's a serious condition that affects your thoughts, feelings, and daily activities.

Common symptoms include:
• Persistent sad, anxious, or "empty" mood
• Loss of interest in activities you once enjoyed
• Changes in appetite or weight
• Sleep disturbances
• Fatigue or loss of energy
• Feelings of worthlessness or guilt
• Difficulty concentrating
• Thoughts of death or suicide

If you're experiencing these symptoms, consider speaking with a mental health professional.""",

                """Depression is a common but serious mood disorder that requires understanding and treatment.

What can help:
• Talk to a therapist or counselor
• Consider medication if recommended by a doctor
• Maintain a routine
• Stay connected with loved ones
• Practice self-care
• Get regular exercise

Remember, depression is treatable and you don't have to face it alone."""
            ],
            
            'anxiety': [
                """Anxiety involves persistent and excessive worry that interferes with daily activities.

Common types include:
• Generalized Anxiety Disorder (GAD)
• Panic Disorder
• Social Anxiety Disorder
• Specific Phobias

Symptoms may include:
• Restlessness or feeling on edge
• Difficulty concentrating
• Muscle tension
• Sleep problems
• Panic attacks

Effective treatments include therapy (especially CBT), medication, and lifestyle changes.""",

                """Anxiety can feel overwhelming, but there are many strategies to manage it:

Immediate techniques:
• Deep breathing exercises
• Grounding techniques (5-4-3-2-1 method)
• Progressive muscle relaxation
• Mindfulness meditation

Long-term strategies:
• Cognitive Behavioral Therapy (CBT)
• Regular exercise
• Limiting caffeine and alcohol
• Maintaining a consistent sleep schedule"""
            ],
            
            'stress': [
                """Stress is your body's response to challenges or demands. While some stress is normal, chronic stress can affect your health.

Common causes:
• Work or school pressures
• Financial concerns
• Relationship issues
• Major life changes
• Health problems

Symptoms include:
• Headaches
• Muscle tension
• Fatigue
• Sleep problems
• Irritability
• Difficulty concentrating""",

                """Managing stress effectively:

Quick relief:
• Take a short walk
• Practice deep breathing
• Listen to calming music
• Take a break from screens

Long-term management:
• Time management techniques
• Regular physical activity
• Healthy boundaries
• Mindfulness practice
• Adequate sleep"""
            ],
            
            'burnout': [
                """Burnout is a state of emotional, physical, and mental exhaustion caused by excessive and prolonged stress.

Signs of burnout:
• Feeling drained most of the time
• Reduced performance at work/school
• Cynicism or detachment
• Feeling ineffective
• Physical symptoms like headaches or stomach issues

Recovery involves:
• Setting boundaries
• Taking regular breaks
• Seeking support
• Reevaluating priorities
• Professional help if needed"""
            ],
            
            # Coping Strategies and Techniques
            'coping_strategies': [
                """Here are some effective coping strategies:

Emotional coping:
• Journaling your thoughts and feelings
• Talking to someone you trust
• Creative expression (art, music, writing)
• Practicing self-compassion

Physical coping:
• Regular exercise
• Deep breathing exercises
• Progressive muscle relaxation
• Getting enough sleep

Mental coping:
• Mindfulness meditation
• Cognitive restructuring
• Problem-solving techniques
• Setting realistic goals""",

                """Quick coping techniques you can try right now:

1. 5-4-3-2-1 Grounding:
   • Name 5 things you can see
   • 4 things you can touch
   • 3 things you can hear
   • 2 things you can smell
   • 1 thing you can taste

2. Box Breathing:
   • Breathe in for 4 counts
   • Hold for 4 counts
   • Breathe out for 4 counts
   • Hold for 4 counts
   • Repeat 4 times

3. Progressive Muscle Relaxation:
   • Tense and relax each muscle group from toes to head"""
            ],
            
            'mindfulness': [
                """Mindfulness means paying attention to the present moment without judgment.

Simple mindfulness practices:
• Mindful breathing: Focus on your breath for 5 minutes
• Body scan: Notice sensations in each part of your body
• Mindful eating: Pay attention to the taste and texture of food
• Walking meditation: Focus on the sensation of walking

Benefits include reduced stress, improved focus, and better emotional regulation.""",

                """Try this 3-minute mindfulness exercise:

1. Find a comfortable position
2. Close your eyes and take 3 deep breaths
3. Notice the physical sensations in your body
4. Pay attention to your breathing
5. When your mind wanders, gently bring it back to your breath
6. Slowly open your eyes when ready"""
            ],
            
            'self_care': [
                """Self-care is essential for mental health. Here are some ideas:

Physical self-care:
• Get 7-9 hours of sleep
• Eat nutritious meals
• Exercise regularly
• Take relaxing baths

Emotional self-care:
• Practice saying no
• Set healthy boundaries
• Allow yourself to feel emotions
• Engage in hobbies you enjoy

Social self-care:
• Connect with supportive friends
• Join a community group
• Schedule quality time with loved ones""",

                """Daily self-care checklist:
☐ Drink enough water
☐ Eat at least one nutritious meal
☐ Move your body for 15 minutes
☐ Take breaks from screens
☐ Connect with someone
☐ Do one thing you enjoy
☐ Practice gratitude"""
            ],
            
            # Sleep Issues
            'sleep_problems': [
                """Sleep problems can significantly impact mental health. Common issues include:

• Insomnia: Difficulty falling or staying asleep
• Oversleeping: Sleeping too much
• Nightmares or night terrors
• Restless sleep

Improving sleep hygiene:
• Maintain a consistent sleep schedule
• Create a relaxing bedtime routine
• Keep your bedroom cool, dark, and quiet
• Avoid screens 1 hour before bed
• Limit caffeine and alcohol""",

                """Try this sleep routine:

1. 1 hour before bed: Turn off screens, do something relaxing
2. 30 minutes before: Warm shower or bath
3. 15 minutes before: Read a book or listen to calm music
4. Bedtime: Practice deep breathing in bed

If sleep problems persist, consider consulting a healthcare provider."""
            ],
            
            # Relationships and Social
            'loneliness': [
                """Feeling lonely is common and can affect anyone. Here's what might help:

• Reach out to old friends or family
• Join clubs or groups with similar interests
• Consider volunteering
• Practice self-compassion
• Seek professional support if needed

Remember, many people feel lonely sometimes, and it's okay to ask for connection.""",

                """Ways to combat loneliness:

• Schedule regular video calls with loved ones
• Join online communities
• Take a class or workshop
• Get a pet if possible
• Practice being comfortable with yourself"""
            ],
            
            'relationship_issues': [
                """Relationship challenges are normal. Consider:

• Open and honest communication
• Active listening
• Setting healthy boundaries
• Seeking couples counseling if needed
• Taking time for self-reflection

Remember that healthy relationships involve mutual respect and understanding."""
            ],
            
            # Professional Help
            'therapy': [
                """Therapy can be incredibly helpful for mental health. Types include:

• Cognitive Behavioral Therapy (CBT)
• Dialectical Behavior Therapy (DBT)
• Psychodynamic therapy
• Humanistic therapy
• Group therapy

How to find a therapist:
• Ask your doctor for referrals
• Use online directories like Psychology Today
• Check with your insurance provider
• Consider online therapy platforms""",

                """What to expect in therapy:

• A safe, confidential space to talk
• Professional guidance and support
• Practical strategies and tools
• Progress at your own pace

Remember, it's okay to try different therapists until you find the right fit."""
            ],
            
            'medication': [
                """Medication can be an important part of mental health treatment:

Common types:
• Antidepressants
• Anti-anxiety medications
• Mood stabilizers
• Antipsychotics

Important considerations:
• Always take as prescribed
• Discuss side effects with your doctor
• Don't stop abruptly without medical guidance
• Medication often works best with therapy

Only a qualified healthcare provider can prescribe medication."""
            ],
            
            # Crisis Resources
            'emergency': [
                """🚨 IMMEDIATE CRISIS SUPPORT 🚨

If you're in crisis or having thoughts of harming yourself, please reach out NOW:

• 988 Suicide & Crisis Lifeline: Call or text 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: Call 911
• National Suicide Prevention Lifeline: 1-800-273-8255

You are not alone, and there are people who want to help. Your life matters.""",

                """🚨 URGENT SUPPORT NEEDED 🚨

Please contact these resources immediately:

• 988 Suicide & Crisis Lifeline (24/7)
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911
• Go to your nearest emergency room

You matter, and help is available right now."""
            ],
            
            # Resources and Help
            'resources': [
                """🌐 Mental Health Resources:

Hotlines:
• 988 Suicide & Crisis Lifeline
• Crisis Text Line: Text HOME to 741741
• National Alliance on Mental Illness (NAMI) Helpline: 1-800-950-NAMI

Websites:
• Mental Health America: mhanational.org
• National Institute of Mental Health: nimh.nih.gov
• Anxiety and Depression Association of America: adaa.org

Apps:
• Calm (meditation)
• Headspace (mindfulness)
• MoodKit (CBT tools)
• Sanvello (anxiety/depression)""",

                """📚 Additional Resources:

Online Support:
• 7 Cups (free online therapy)
• TalkSpace (online therapy)
• BetterHelp (online counseling)

Books:
• "The Feeling Good Handbook" by David Burns
• "The Anxiety and Phobia Workbook" by Edmund Bourne
• "The Dialectical Behavior Therapy Skills Workbook" by McKay

Remember, these are supplementary to professional help."""
            ],
            
            # General Mental Health
            'mental_health_basics': [
                """Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act.

Good mental health doesn't mean being happy all the time. It means:
• Coping with life's challenges
• Maintaining fulfilling relationships
• Working productively
• Making contributions to your community
• Realizing your full potential""",

                """Taking care of your mental health is as important as physical health. Some basics:

• Get regular exercise
• Eat a balanced diet
• Get enough sleep
• Stay connected with others
• Practice stress management
• Seek help when needed"""
            ],
            
            # Positive Psychology
            'gratitude': [
                """Practicing gratitude can improve mental health:

Simple ways to practice:
• Keep a gratitude journal
• Share appreciation with others
• Notice small positive moments
• Write thank-you notes

Benefits include increased happiness, better relationships, and reduced stress.""",

                """Try this gratitude exercise:
Each day, write down 3 things you're grateful for. They can be small things like:
• A warm cup of coffee
• A kind word from someone
• Beautiful weather
• A comfortable bed"""
            ],
            
            'positive_thinking': [
                """Positive thinking doesn't mean ignoring problems. It means approaching challenges more productively.

Techniques:
• Reframe negative thoughts
• Practice self-compassion
• Focus on solutions, not just problems
• Celebrate small victories
• Surround yourself with positive influences""",

                """Challenge negative thoughts by asking:
• Is this thought based on facts or feelings?
• What's another way to look at this situation?
• What would I tell a friend in this situation?
• Is this thought helping or hurting me?"""
            ],
            
            # Default and Unknown Responses
            'unknown': [
                "I'm here to listen and support you. Could you tell me more about what you're experiencing?",
                "Thank you for sharing. I'm focusing on mental health support. How else can I help you today?",
                "I want to make sure I understand correctly. Could you rephrase that or tell me more about your concern?",
                "I'm learning to better support mental health needs. Could you share more about what you're looking for help with?",
                "That's an important topic. I'm here primarily for mental health support. Is there something specific you'd like to discuss about your mental wellbeing?"
            ],
            
            'off_topic': [
                "I'm specially designed to help with mental health concerns. Is there something about your emotional wellbeing you'd like to discuss?",
                "I focus on mental health support. Would you like to talk about stress, anxiety, depression, self-care, or other mental health topics?",
                "As a mental health assistant, I'm here to help with emotional wellbeing. What's on your mind related to how you're feeling?"
            ]
        }
    
    def _initialize_patterns(self):
        """Initialize pattern matching for user inputs"""
        return {
            'greeting': r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b',
            'farewell': r'\b(bye|goodbye|see you|later|take care|farewell)\b',
            'thanks': r'\b(thanks|thank you|thankyou|appreciate it|thx)\b',
            
            # Mental Health Conditions
            'depression': r'\b(depress|depressed|depression|hopeless|worthless|suicidal|ending it all)\b',
            'anxiety': r'\b(anxious|anxiety|panic|nervous|worried|worrying|overwhelmed|stressed)\b',
            'stress': r'\b(stress|stressed|pressure|overwhelmed|burnout|burnt out)\b',
            'burnout': r'\b(burnout|burnt out|exhausted|tired all the time|work fatigue)\b',
            
            # Coping and Techniques
            'coping_strategies': r'\b(cope|coping|strategies|techniques|deal with|handle|manage|what should I do)\b',
            'mindfulness': r'\b(mindful|mindfulness|meditation|meditate|present moment|grounding)\b',
            'self_care': r'\b(self care|self-care|take care of myself|self love|self compassion)\b',
            
            # Specific Issues
            'sleep_problems': r'\b(sleep|insomnia|can\'t sleep|tired|exhausted|wake up|nightmares)\b',
            'loneliness': r'\b(lonely|alone|isolated|no friends|no one cares|isolated)\b',
            'relationship_issues': r'\b(relationship|partner|spouse|friend|family|argument|fight|breakup)\b',
            
            # Professional Help
            'therapy': r'\b(therapy|therapist|counselor|counselling|psychologist|psychiatrist|therapy)\b',
            'medication': r'\b(medication|meds|pills|prescription|antidepressant|anti-anxiety)\b',
            
            # Crisis
            'emergency': r'\b(suicide|kill myself|end it all|hurting myself|emergency|crisis|help me now)\b',
            
            # Resources
            'resources': r'\b(resources|help|support|hotline|helpline|where to get help|professional)\b',
            
            # General Mental Health
            'mental_health_basics': r'\b(mental health|mental illness|emotional health|psychological)\b',
            'gratitude': r'\b(gratitude|thankful|appreciate|grateful)\b',
            'positive_thinking': r'\b(positive|optimistic|negative thoughts|thinking pattern)\b',
            
            # Off-topic
            'off_topic': r'\b(weather|sports|politics|news|entertainment|movies|music|games|food|travel)\b'
        }
    
    def get_response(self, message, user_id=None):
        """Get appropriate response based on user message"""
        if not message or not message.strip():
            return "I'm here to listen. Please share what's on your mind."
        
        message_lower = message.lower().strip()
        
        # Store user context
        if user_id:
            if user_id not in self.user_context:
                self.user_context[user_id] = {'last_interaction': datetime.now()}
            self.user_context[user_id]['last_interaction'] = datetime.now()
        
        # Check for emergency first (highest priority)
        if re.search(self.patterns['emergency'], message_lower, re.IGNORECASE):
            return random.choice(self.responses['emergency'])
        
        # Check for farewell
        if re.search(self.patterns['farewell'], message_lower, re.IGNORECASE):
            return random.choice(self.responses['farewell'])
        
        # Check for thanks
        if re.search(self.patterns['thanks'], message_lower, re.IGNORECASE):
            return random.choice(self.responses['thanks'])
        
        # Check for greeting
        if re.search(self.patterns['greeting'], message_lower, re.IGNORECASE):
            return random.choice(self.responses['greeting'])
        
        # Check for off-topic
        if re.search(self.patterns['off_topic'], message_lower, re.IGNORECASE):
            return random.choice(self.responses['off_topic'])
        
        # Check other mental health patterns
        for intent, pattern in self.patterns.items():
            if intent not in ['greeting', 'farewell', 'thanks', 'emergency', 'off_topic']:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return random.choice(self.responses[intent])
        
        # Default response for unknown input
        return random.choice(self.responses['unknown'])
    
    def get_welcome_message(self):
        """Get welcome message for new users"""
        return random.choice(self.responses['greeting'])
    
    def clear_user_context(self, user_id):
        """Clear context for a specific user"""
        if user_id in self.user_context:
            del self.user_context[user_id]

# Create global instance
mental_health_bot = MentalHealthChatbot()