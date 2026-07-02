import streamlit as st
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO
import os
import json
import time
import random
import requests
import subprocess
import sys
import pickle

# Page configuration
st.set_page_config(
    page_title="Taha's Portfolio",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'profile_pic' not in st.session_state:
    st.session_state.profile_pic = None
if 'profile_pic_saved' not in st.session_state:
    st.session_state.profile_pic_saved = False
if 'show_game' not in st.session_state:
    st.session_state.show_game = False
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_initialized' not in st.session_state:
    st.session_state.chat_initialized = False
if 'chat_response_count' not in st.session_state:
    st.session_state.chat_response_count = 0
if 'chat_max_responses' not in st.session_state:
    st.session_state.chat_max_responses = 5
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True

# File to store the profile picture
PROFILE_PIC_FILE = "profile_pic_data.pkl"

def save_profile_pic(image_data):
    """Save profile picture to file"""
    try:
        with open(PROFILE_PIC_FILE, 'wb') as f:
            pickle.dump(image_data, f)
        return True
    except:
        return False

def load_profile_pic():
    """Load profile picture from file"""
    try:
        if os.path.exists(PROFILE_PIC_FILE):
            with open(PROFILE_PIC_FILE, 'rb') as f:
                return pickle.load(f)
        return None
    except:
        return None

def get_permanent_profile():
    """Get the permanent profile picture"""
    # Check if we have a saved profile picture in session
    if st.session_state.profile_pic is not None and st.session_state.profile_pic_saved:
        return st.session_state.profile_pic
    
    # Try to load from file
    saved_data = load_profile_pic()
    if saved_data is not None:
        st.session_state.profile_pic = saved_data
        st.session_state.profile_pic_saved = True
        return saved_data
    
    # Default profile (Zoro image placeholder)
    try:
        # Create a default profile image
        img = Image.new('RGB', (200, 200), color='#00ff88')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        # Draw a simple face
        draw.ellipse([50, 50, 150, 150], fill='#1a1a1a', outline='#00ff88', width=3)
        draw.ellipse([70, 90, 90, 110], fill='#00ff88')
        draw.ellipse([110, 90, 130, 110], fill='#00ff88')
        # Draw a smile
        draw.arc([70, 110, 130, 140], 0, 180, fill='#00ff88', width=2)
        # Add text
        draw.text((60, 170), "⚔️", fill='#00ff88')
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        st.session_state.profile_pic = f"data:image/png;base64,{img_base64}"
        st.session_state.profile_pic_saved = True
        save_profile_pic(st.session_state.profile_pic)
        return st.session_state.profile_pic
    except:
        # Ultimate fallback
        default = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        st.session_state.profile_pic = f"data:image/png;base64,{default}"
        st.session_state.profile_pic_saved = True
        return st.session_state.profile_pic

# Load permanent profile picture
PERMANENT_PROFILE = get_permanent_profile()

# Your Personal Information
PERSONAL_INFO = {
    "name": "Taha",
    "age": "13",
    "class": "C1",
    "title": "Python Developer & AI Enthusiast",
    "tagline": "Building innovative solutions with Python and AI",
    "bio": "Passionate Python developer with expertise in AI, web development, and creating interactive applications. Currently learning and growing at Aptech.",
    "email": "haidertaha2026@gmail.com",
    "phone": "03001234589",
    "location": "Rahim Yar Khan, Pakistan",
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourusername",
    "twitter": "https://twitter.com/yourusername",
    "website": "https://yourwebsite.com",
    "about": """⚔️ **Hello! I'm Taha**

I'm a 13-year-old passionate Python developer and AI enthusiast from Rahim Yar Khan, Pakistan. I started my programming journey at the age of 11 and have been building amazing projects ever since!

**🎯 My Mission:**
To create innovative solutions using Python and AI that make a difference. I believe in continuous learning and pushing the boundaries of what's possible.

**💡 What Drives Me:**
- Solving complex problems with code
- Exploring the latest in AI and technology
- Building projects that people can actually use
- Learning something new every day

**🚀 My Journey:**
- Started coding at 11 years old
- Joined Aptech in 2023 to formalize my learning
- Built 3+ major projects including this portfolio
- Earned multiple certifications in Python and AI
- Currently exploring advanced AI and web development

**🌟 Fun Facts:**
- I'm the youngest developer in my class
- I love playing video games (especially the ones I build!)
- I'm always curious about how things work
- I believe age is just a number when it comes to coding

**📚 Currently Learning:**
- Advanced Python concepts
- Machine Learning and Deep Learning
- Web Development with Streamlit
- Game Development with Pygame

**🎯 Future Goals:**
- Build more AI-powered applications
- Contribute to open-source projects
- Start my own tech startup
- Inspire other young developers to code

I'm always open to new opportunities, collaborations, and learning experiences. Let's build something amazing together! 💪"""
}

# Skills - Updated without JavaScript, HTML/CSS, Flask, Django, NLP
SKILLS = {
    "Programming Languages": [
        {"name": "Python", "level": 95}
    ],
    "AI & Machine Learning": [
        {"name": "Machine Learning", "level": 70},
        {"name": "Computer Vision", "level": 60}
    ],
    "Frameworks & Tools": [
        {"name": "Streamlit", "level": 90},
        {"name": "Git", "level": 80}
    ],
    "Other Skills": [
        {"name": "Problem Solving", "level": 85},
        {"name": "Team Work", "level": 80},
        {"name": "Communication", "level": 75}
    ]
}

# Projects - Updated without NLP
PROJECTS = [
    {
        "title": "AI Chatbot",
        "description": "An intelligent chatbot built using Python. Capable of understanding and responding to user queries.",
        "technologies": ["Python", "TensorFlow", "Streamlit"],
        "github": "https://github.com/yourusername/ai-chatbot",
        "demo": "chatbot"
    },
    {
        "title": "Aircraft Shooter Game",
        "description": "An exciting aircraft shooting game with keyboard controls, enemy AI, power-ups, and multiple levels!",
        "technologies": ["Python", "Pygame", "Streamlit"],
        "github": "https://github.com/yourusername/aircraft-shooter",
        "demo": "game"
    },
    {
        "title": "Portfolio Website",
        "description": "A professional portfolio website built with Streamlit to showcase projects, skills, and achievements.",
        "technologies": ["Python", "Streamlit"],
        "github": "https://github.com/yourusername/portfolio",
        "demo": "https://yourdemo.com"
    }
]

# Experience
EXPERIENCE = [
    {
        "company": "Aptech",
        "position": "Student",
        "period": "2023 - Present",
        "location": "Rahim Yar Khan, Pakistan",
        "description": [
            "Learning full-stack Python development and AI technologies",
            "Working on real-world projects and assignments",
            "Collaborating with peers on group projects",
            "Developing practical programming skills"
        ]
    }
]

# Education
EDUCATION = [
    {
        "degree": "none",
        "school": "H.H Sheikh Khalifa Public School",
        "year": "2026",
        "gpa": "A+"
    },
    {
        "degree": "Intermediate (ICS)",
        "school": "In Progress",
        "year": "2024 - Present",
        "gpa": "In Progress"
    },
    {
        "degree": "Software Engineering",
        "school": "Aptech - Rahim Yar Khan",
        "year": "2023 - Present",
        "gpa": "In Progress"
    }
]

# Certifications - Updated without Web Development Basics
CERTIFICATIONS = [
    "Python Programming",
    "Introduction to AI",
    "Streamlit Framework"
]

# Testimonials
TESTIMONIALS = [
    {"text": "Taha is a dedicated and talented developer with great potential.", "author": "Aptech Instructor"},
    {"text": "Excellent problem-solving skills and a quick learner.", "author": "Classmate"}
]

# Sidebar Navigation
def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("""
            <style>
            .sidebar-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #00ff88;
                text-align: center;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
            }
            .sidebar-subtitle {
                text-align: center;
                color: #00cc77;
                font-size: 0.9rem;
                margin-bottom: 1.5rem;
            }
            .nav-btn {
                width: 100%;
                padding: 0.6rem 1rem;
                margin: 0.2rem 0;
                border: none;
                border-radius: 10px;
                background: transparent;
                color: #cccccc;
                font-weight: 500;
                text-align: left;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .nav-btn:hover {
                background: rgba(0, 255, 136, 0.15);
                transform: translateX(5px);
                color: #00ff88;
            }
            .nav-btn-active {
                background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
                color: #1a1a1a !important;
                font-weight: 600;
            }
            .nav-btn-active:hover {
                background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
                transform: translateX(5px);
                color: #1a1a1a !important;
            }
            .nav-icon {
                margin-right: 10px;
            }
            .sidebar-divider {
                border: none;
                border-top: 1px solid rgba(0, 255, 136, 0.3);
                margin: 0.8rem 0;
            }
            .close-sidebar-btn {
                background: rgba(0, 255, 136, 0.15);
                color: #cccccc;
                border: 1px solid #00ff88;
                border-radius: 10px;
                padding: 0.5rem;
                width: 100%;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 1rem;
            }
            .close-sidebar-btn:hover {
                background: #00ff88;
                color: #1a1a1a;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">⚔️ Taha\'s Portfolio</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subtitle">Python Developer & AI Enthusiast</div>', unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Navigation buttons
        nav_items = [
            ("⚔️", "Home", "Home"),
            ("👤", "About", "About"),
            ("🤖", "AI Chatbot", "Chatbot"),
            ("✈️", "Aircraft Game", "Game"),
            ("📊", "Analytics", "Analytics"),
            ("📫", "Contact", "Contact")
        ]
        
        for icon, label, page in nav_items:
            is_active = st.session_state.page == page
            btn_class = "nav-btn nav-btn-active" if is_active else "nav-btn"
            
            # Use columns for better alignment
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown(f"<span style='font-size: 1.2rem;'>{icon}</span>", unsafe_allow_html=True)
            with col2:
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page
                    st.session_state.show_chatbot = False
                    st.session_state.show_game = False
                    st.rerun()
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Quick Stats in sidebar
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Projects", "3+")
        with col2:
            st.metric("Skills", "8+")
        
        # Social links
        st.markdown("### 🔗 Connect")
        st.markdown(f"""
            <div style="display: flex; gap: 0.5rem; justify-content: center; margin: 0.5rem 0;">
                <a href="{PERSONAL_INFO['github']}" target="_blank" style="font-size: 1.8rem; text-decoration: none;">🐙</a>
                <a href="{PERSONAL_INFO['linkedin']}" target="_blank" style="font-size: 1.8rem; text-decoration: none;">💼</a>
                <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="font-size: 1.8rem; text-decoration: none;">🐦</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Current time
        current_time = datetime.now().strftime("%I:%M %p")
        st.markdown(f"<div style='text-align: center; color: #999999; font-size: 0.9rem;'>🕐 {current_time}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; color: #666666; font-size: 0.8rem;'>{datetime.now().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
        
        # Close Sidebar Button
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        if st.button("❌ Close Sidebar", key="close_sidebar", use_container_width=True):
            st.session_state.sidebar_open = False
            st.rerun()

# Chatbot Functions (Simplified without NLP)
def get_chatbot_response(user_input, chat_history):
    """Get response from AI chatbot"""
    
    # Check if response limit reached
    if st.session_state.chat_response_count >= st.session_state.chat_max_responses:
        return None
    
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return """⚔️ Hello there! Welcome to Taha's AI Chatbot Demo!

I'm here to showcase my AI capabilities. You can ask me about:
- My skills and experience
- My projects
- Python programming
- AI and machine learning
- Or anything else you're curious about!

What would you like to know? 💡"""
    
    elif any(word in user_lower for word in ['python', 'code', 'programming']):
        return """🐍 Ah, Python! My favorite programming language!

Taha is highly skilled in Python with 95% proficiency. Here's what he can do:

**Python Expertise:**
- Web Development with Streamlit
- AI & Machine Learning
- Data Analysis & Visualization
- Game Development with Pygame
- API Development

**Fun Fact:** Taha started learning Python at age 11 and has been building amazing projects ever since!

Would you like to know about specific Python projects? 🚀"""
    
    elif any(word in user_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
        return """🤖 AI and Machine Learning are revolutionizing the world!

Taha has been diving deep into AI technologies:

**AI Skills:**
- Machine Learning (70%)
- Computer Vision (60%)
- Building AI Chatbots
- Working with LLMs

**Projects:**
1. This AI Chatbot - built with Python
2. Machine Learning models for predictions
3. Computer vision applications

Want to learn more about AI? Ask me anything! 🎯"""
    
    elif any(word in user_lower for word in ['project', 'portfolio', 'work']):
        return """🚀 Taha has built some amazing projects!

**Featured Projects:**
1. 🤖 **AI Chatbot** - You're using it right now!
   - Intelligent responses
   - 5 free questions demo

2. ✈️ **Aircraft Shooter Game**
   - Pygame development
   - Enemy AI system
   - Power-ups and scoring
   - Multiple enemy types

3. 🌐 **Portfolio Website**
   - Streamlit framework
   - Professional design
   - Interactive sections
   - Mobile responsive

Each project showcases different skills and technologies! 💪"""
    
    elif any(word in user_lower for word in ['age', 'how old']):
        return """🎂 Taha is 13 years old!

Despite his young age, he's already accomplished so much:
- Started programming at 11
- Learning at Aptech since 2023
- Built 3+ major projects
- Multiple certifications in Python and AI

Age is just a number when you have passion and dedication! 🌟"""
    
    elif any(word in user_lower for word in ['skills', 'expertise', 'know']):
        return """💪 Taha's skills are impressive for any developer!

**Core Skills:**
- 🐍 Python: 95% (Expert)
- 🤖 AI/ML: 70% (Advanced)
- 🎯 Problem Solving: 85% (Expert)
- 💪 Teamwork: 80% (Advanced)

**Certifications:**
1. Python Programming
2. Introduction to AI
3. Streamlit Framework

He's constantly learning and improving! 📚"""
    
    elif any(word in user_lower for word in ['game', 'aircraft', 'shooter']):
        return """✈️ The Aircraft Shooter Game is super fun!

**Game Features:**
- 🎯 Destroy 20 enemies to win
- 💪 5 lives to survive
- ⚡ Power-ups: Rapid Fire, Shield, Health
- 🔥 Combo system for bonus points
- 🎮 Keyboard controls (WASD/Arrows + Space)

**Enemy Types:**
- Normal: Standard enemy
- Fast: Quick and agile
- Tank: Takes 3 hits to destroy

Want to play? Click the "Play Game" button! 🎮"""
    
    elif any(word in user_lower for word in ['bot', 'chatbot', 'this']):
        return """🤖 This is an AI Chatbot Demo!

I'm a demonstration of Taha's AI capabilities. Here's what makes me special:

**Features:**
- 💬 Natural language understanding
- 🎯 5 free questions per session
- ⚔️ Intelligent responses
- 📚 Knowledge about multiple topics
- ✨ Interactive and engaging

**What I can do:**
- Answer questions about Taha
- Discuss technology
- Explain programming concepts
- Talk about projects

This is just a taste of what's possible with AI! 🌟"""
    
    elif any(word in user_lower for word in ['bye', 'goodbye', 'see you', 'later']):
        return """👋 Goodbye! Thanks for chatting with me!

**Remember:**
- You can ask 5 questions per session
- Click "Clear Chat" to start over
- Try different topics for interesting responses

Come back anytime! Have a great day! 🌟"""
    
    else:
        responses = [
            f"""⚔️ That's an interesting question! Let me think about '{user_input}'...

I can help you with:
- Learning about Taha's skills and projects
- Understanding Python and AI concepts
- Getting information about the portfolio
- Playing the aircraft shooter game

What specific aspect are you curious about? 🤔""",
            
            f"""💡 '{user_input}' - that's a topic worth exploring!

Here's what I know:
- Taha has experience with various technologies
- He's built 3 major projects
- He's passionate about AI and programming
- He's always learning new things

Would you like more details about any of these? 🎯""",
            
            f"""🌟 Interesting! You asked about '{user_input}'.

I'm designed to answer questions about:
1. Taha's background and skills
2. His projects (AI Chatbot, Aircraft Game, Portfolio)
3. Python and AI concepts
4. Technology and programming in general

Feel free to ask more specific questions! 💪""",
            
            f"""🚀 '{user_input}' - that's a great topic!

From what I know, Taha has expertise in:
- Python development (95%)
- Web applications with Streamlit
- AI and machine learning
- Game development
- Problem solving

Want to dive deeper into any of these areas? 📚"""
        ]
        return random.choice(responses)

def initialize_chat():
    """Initialize chat with a welcome message"""
    if not st.session_state.chat_initialized:
        welcome = """⚔️ **Welcome to the AI Chatbot Demo!**

I'm Taha's AI assistant, built to showcase his programming skills. Here's how this works:

⚔️ **You get exactly 5 free questions per session!**

**Ask me about:**
- 🐍 Python programming skills
- 🤖 AI and machine learning
- 🚀 Projects (Chatbot, Game, Portfolio)
- 💪 Skills and expertise
- 📚 Learning journey
- 🎯 Anything else you're curious about!

💡 **Pro Tip**: Ask specific questions for better responses!

**Your Questions Remaining: 5/5**

What would you like to know? 😊"""
        
        st.session_state.chat_history = [
            {"role": "assistant", "content": welcome}
        ]
        st.session_state.chat_initialized = True
        st.session_state.chat_response_count = 0

def render_chatbot_interface():
    """Render the chatbot interface"""
    st.markdown("""
        <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 1rem;
            background: rgba(40, 40, 40, 0.95);
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #00ff88;
        }
        .chat-message {
            margin: 0.5rem 0;
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            animation: fadeInUp 0.3s ease-out;
        }
        .user-message {
            background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
            color: #1a1a1a;
            margin-left: 20%;
            border-bottom-right-radius: 0;
        }
        .ai-message {
            background: rgba(0, 255, 136, 0.1);
            color: #cccccc;
            margin-right: 20%;
            border-bottom-left-radius: 0;
            border-left: 4px solid #00ff88;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .response-counter {
            background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
            color: #1a1a1a;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .suggested-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.5rem 0;
            justify-content: center;
        }
        .suggested-question {
            background: rgba(0, 255, 136, 0.15);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            border: 1px solid #00ff88;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            color: #cccccc;
            cursor: pointer;
        }
        .suggested-question:hover {
            background: #00ff88;
            color: #1a1a1a;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    
    initialize_chat()
    
    remaining = st.session_state.chat_max_responses - st.session_state.chat_response_count
    st.markdown(f"""
        <div class="response-counter">
            💬 Questions Used: {st.session_state.chat_response_count}/{st.session_state.chat_max_responses} 
            | Remaining: {remaining}
            {'🔴' if remaining == 0 else '🟢' if remaining > 2 else '🟡'}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message ai-message">
                    <strong>⚔️ AI Assistant:</strong> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    is_limit_reached = st.session_state.chat_response_count >= st.session_state.chat_max_responses
    
    if is_limit_reached:
        st.warning("⚠️ **You've used all 5 questions!** Click 'Clear Chat' to start a new session.")
    
    if not is_limit_reached and remaining > 0:
        st.markdown("""
            <div style="text-align: center; margin: 0.5rem 0;">
                <p style="color: #999999; font-size: 0.9rem;">💡 Try asking these questions:</p>
                <div class="suggested-questions">
                    <span class="suggested-question">💪 Skills</span>
                    <span class="suggested-question">🚀 Projects</span>
                    <span class="suggested-question">🤖 AI</span>
                    <span class="suggested-question">🎂 Age</span>
                    <span class="suggested-question">🐍 Python</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            user_input = st.text_input(
                "Type your question...",
                placeholder="Ask me anything! ⚔️ (5 questions max)",
                key="chat_input",
                label_visibility="collapsed",
                disabled=is_limit_reached
            )
        with col2:
            submit = st.form_submit_button(
                "Send 💬", 
                use_container_width=True,
                disabled=is_limit_reached
            )
        with col3:
            clear = st.form_submit_button("Clear 🗑️", use_container_width=True)
        
        if submit and user_input and not is_limit_reached:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("AI is thinking... 🤔"):
                response = get_chatbot_response(user_input, st.session_state.chat_history)
                
                if response is None:
                    st.warning("⚠️ You've reached the 5-question limit! Clear the chat to start over.")
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.session_state.chat_response_count += 1
            
            st.rerun()
        
        if clear:
            st.session_state.chat_history = []
            st.session_state.chat_initialized = False
            st.session_state.chat_response_count = 0
            st.rerun()

def launch_game():
    """Launch the aircraft shooter game"""
    try:
        game_script = """
import pygame
import random
import math
import sys

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
DARK_RED = (180, 20, 20)
GREEN = (50, 255, 50)
DARK_GREEN = (20, 180, 20)
BLUE = (50, 100, 255)
DARK_BLUE = (20, 50, 180)
YELLOW = (255, 255, 50)
ORANGE = (255, 150, 50)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)
CYAN = (50, 255, 255)
PURPLE = (150, 50, 255)

SPACE_DEEP = (30, 30, 30)
SPACE_MID = (50, 50, 50)

class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime, size=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen):
        alpha = self.lifetime / self.max_lifetime
        size = max(1, int(self.size * alpha))
        color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.choice([1, 2, 3])
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.02, 0.08)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        
    def update(self):
        self.brightness = 100 + int(155 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset)))
        
    def draw(self, screen):
        pygame.draw.circle(screen, (self.brightness, self.brightness, self.brightness), (int(self.x), int(self.y)), self.size)

class FighterJet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.create_jet_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_timer = 0
        self.health = 5
        self.max_health = 5
        self.invincible_timer = 0
        self.score = 0
        self.particles = []
        
    def create_jet_image(self):
        self.image = pygame.Surface((70, 70), pygame.SRCALPHA)
        jet_color = (0, 255, 136)
        accent_color = (0, 200, 100)
        
        fuselage_points = [(35, 8), (50, 18), (58, 28), (60, 38), (55, 52), (35, 58), (15, 52), (10, 38), (12, 28), (20, 18)]
        pygame.draw.polygon(self.image, jet_color, fuselage_points)
        pygame.draw.polygon(self.image, accent_color, fuselage_points, 2)
        
        wing_right = [(52, 32), (68, 28), (70, 42), (56, 44)]
        wing_left = [(18, 32), (2, 28), (0, 42), (14, 44)]
        pygame.draw.polygon(self.image, jet_color, wing_right)
        pygame.draw.polygon(self.image, jet_color, wing_left)
        
        canopy_points = [(28, 14), (42, 14), (45, 24), (35, 26), (25, 24)]
        pygame.draw.polygon(self.image, (100, 255, 200), canopy_points)
        
        pygame.draw.ellipse(self.image, (50, 60, 50), (28, 52, 14, 8))
        pygame.draw.ellipse(self.image, (0, 200, 100), (30, 55, 10, 6))
        pygame.draw.circle(self.image, GREEN, (35, 30), 3)
        
        self.original_image = self.image.copy()
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.particles = [p for p in self.particles if p.update()]
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
    
    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = 6
            bullet = Bullet(self.rect.centerx, self.rect.top - 5)
            return bullet
        return None
    
    def take_damage(self):
        if self.invincible_timer <= 0:
            self.health -= 1
            self.invincible_timer = 60
            for _ in range(10):
                particle = Particle(
                    self.rect.centerx + random.randint(-20, 20),
                    self.rect.centery + random.randint(-20, 20),
                    random.uniform(-4, 4),
                    random.uniform(-4, 4),
                    RED,
                    random.randint(10, 20),
                    random.randint(2, 4)
                )
                self.particles.append(particle)
            return True
        return False
    
    def add_score(self, points):
        self.score += points
    
    def draw(self, screen):
        if self.invincible_timer <= 0 or (pygame.time.get_ticks() // 50) % 2 == 0:
            screen.blit(self.image, self.rect)
        
        for particle in self.particles:
            particle.draw(screen)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill((0, 255, 136))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 12
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyJet(pygame.sprite.Sprite):
    def __init__(self, enemy_type='normal'):
        super().__init__()
        self.enemy_type = enemy_type
        self.create_enemy_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.rect.y = random.randint(-150, -50)
        
        if enemy_type == 'fast':
            self.speed_y = random.uniform(4, 6)
            self.speed_x = random.uniform(-3, 3)
            self.max_health = 2
            self.score_value = 20
        elif enemy_type == 'tank':
            self.speed_y = random.uniform(2, 3)
            self.speed_x = random.uniform(-0.5, 0.5)
            self.max_health = 5
            self.score_value = 40
        else:
            self.speed_y = random.uniform(3, 5)
            self.speed_x = random.uniform(-1, 1)
            self.max_health = 3
            self.score_value = 15
        
        self.health = self.max_health
        self.rotation = 0
        self.original_image = self.image.copy()
        self.hit_effect = 0
        
    def create_enemy_image(self):
        self.image = pygame.Surface((65, 65), pygame.SRCALPHA)
        color = (139, 0, 0)
        
        fuselage_points = [(32, 8), (48, 18), (55, 28), (57, 38), (52, 52), (32, 58), (12, 52), (7, 38), (9, 28), (16, 18)]
        pygame.draw.polygon(self.image, color, fuselage_points)
        
        wing_right = [(50, 32), (65, 28), (68, 40), (52, 42)]
        wing_left = [(14, 32), (-1, 28), (-4, 40), (12, 42)]
        pygame.draw.polygon(self.image, color, wing_right)
        pygame.draw.polygon(self.image, color, wing_left)
        
        if self.enemy_type == 'tank':
            for i in range(3):
                pygame.draw.rect(self.image, RED, (25 + i*5, 5, 3, 3))
        
        self.original_image = self.image.copy()
        
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        target_rot = self.speed_x * 5
        self.rotation += (target_rot - self.rotation) * 0.1
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=center)
        
        if self.rect.top > SCREEN_HEIGHT + 100:
            self.kill()
        
        return None
    
    def take_damage(self, damage=1):
        self.health -= damage
        self.hit_effect = 8
        if self.health <= 0:
            return True
        return False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        health_bar_width = 35
        health_bar_height = 4
        health_percentage = self.health / self.max_health
        
        bar_x = self.rect.centerx - health_bar_width // 2
        bar_y = self.rect.top - 8
        
        pygame.draw.rect(screen, DARK_RED, (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_bar_width * health_percentage, health_bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, health_bar_width, health_bar_height), 1)
        
        if self.hit_effect > 0:
            self.hit_effect -= 1
            flash_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 150))
            screen.blit(flash_surf, self.rect)

class Explosion:
    def __init__(self, x, y, intensity=1):
        self.particles = []
        for _ in range(30 * intensity):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice([(0, 255, 136), (0, 200, 100), (0, 255, 200)])
            particle = Particle(x, y, vx, vy, color, random.randint(20, 40), random.randint(2, 5))
            self.particles.append(particle)
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

def draw_space_background(screen):
    for i in range(SCREEN_HEIGHT):
        t = i / SCREEN_HEIGHT
        color = (
            int(SPACE_DEEP[0] * (1 - t) + SPACE_MID[0] * t),
            int(SPACE_DEEP[1] * (1 - t) + SPACE_MID[1] * t),
            int(SPACE_DEEP[2] * (1 - t) + SPACE_MID[2] * t)
        )
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))
    
    if not hasattr(draw_space_background, "stars"):
        draw_space_background.stars = [Star() for _ in range(100)]
    for star in draw_space_background.stars:
        star.update()
        star.draw(screen)

def show_text(screen, text, size, x, y, color=WHITE, center=True):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fighter Jet Combat")
    clock = pygame.time.Clock()
    
    total_enemies = 20
    enemies_defeated = 0
    level_complete = False
    level_complete_timer = 0
    
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = []
    
    player = FighterJet()
    all_sprites.add(player)
    
    enemy_spawn_counter = 0
    max_enemies_on_screen = 8
    
    running = True
    game_over = False
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not level_complete:
                    bullet = player.shoot()
                    if bullet:
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                if event.key == pygame.K_r and game_over:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        
        if not game_over and not level_complete:
            keys = pygame.key.get_pressed()
            player.speed_x = 0
            player.speed_y = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.speed_x = -7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.speed_x = 7
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.speed_y = -7
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.speed_y = 7
            
            if len(enemies) < max_enemies_on_screen and enemies_defeated < total_enemies:
                enemy_spawn_counter += 1
                if enemy_spawn_counter >= 50:
                    enemy_spawn_counter = 0
                    rand = random.random()
                    if rand < 0.3:
                        enemy_type = 'fast'
                    elif rand < 0.5:
                        enemy_type = 'tank'
                    else:
                        enemy_type = 'normal'
                    
                    enemy = EnemyJet(enemy_type)
                    enemies.add(enemy)
                    all_sprites.add(enemy)
            
            all_sprites.update()
            
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                if enemy.take_damage(1):
                    enemies_defeated += 1
                    player.add_score(enemy.score_value)
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery, 2 if enemy.enemy_type == 'tank' else 1))
                    enemy.kill()
            
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                if player.take_damage():
                    explosions.append(Explosion(player.rect.centerx, player.rect.centery, 3))
                    if player.health <= 0:
                        game_over = True
            
            explosions = [exp for exp in explosions if exp.update()]
            
            if enemies_defeated >= total_enemies and len(enemies) == 0:
                level_complete = True
                level_complete_timer = 180
        
        screen.fill(BLACK)
        draw_space_background(screen)
        
        for sprite in all_sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)
        
        for explosion in explosions:
            explosion.draw(screen)
        
        for i in range(player.health):
            color = GREEN if player.health > player.max_health * 0.6 else YELLOW if player.health > player.max_health * 0.3 else RED
            pygame.draw.rect(screen, color, (20 + i * 35, 20, 30, 25))
            pygame.draw.rect(screen, WHITE, (20 + i * 35, 20, 30, 25), 2)
        
        show_text(screen, f"SCORE: {player.score}", 32, 20, 60, GOLD, False)
        
        progress = enemies_defeated / total_enemies if total_enemies > 0 else 0
        show_text(screen, f"LEVEL 1", 28, SCREEN_WIDTH // 2, 20, CYAN, True)
        progress_width = 300 * progress
        bar_x = SCREEN_WIDTH // 2 - 150
        bar_y = 50
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, 300, 8))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, 8))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, 300, 8), 1)
        show_text(screen, f"{enemies_defeated}/{total_enemies}", 16, SCREEN_WIDTH // 2, 70, GRAY, True)
        
        show_text(screen, "SPACE: Shoot | WASD/Arrows: Move | ESC: Exit", 16, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20, GRAY, True)
        
        if level_complete:
            level_complete_timer -= 1
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            show_text(screen, "🎉 LEVEL COMPLETE! 🎉", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, GREEN, True)
            show_text(screen, f"SCORE: {player.score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GOLD, True)
            show_text(screen, "Press ESC to exit", 28, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, WHITE, True)
            
            if level_complete_timer <= 0:
                return True
        
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            show_text(screen, "💀 GAME OVER 💀", 80, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, RED, True)
            show_text(screen, f"SCORE: {player.score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10, GOLD, True)
            show_text(screen, "Press R to restart", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, YELLOW, True)
            show_text(screen, "Press ESC for menu", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110, WHITE, True)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return True
            if keys[pygame.K_ESCAPE]:
                return False
        
        pygame.display.flip()
    
    return False

def main():
    pygame.init()
    while True:
        restart = game_loop()
        if not restart:
            break
    pygame.quit()

if __name__ == "__main__":
    main()
"""
        
        subprocess.Popen([sys.executable, "-c", game_script])
        return True
    except Exception as e:
        st.error(f"Failed to launch game: {str(e)}")
        return False

# Custom CSS - Grey Background with Vibrant Green Text
st.markdown("""
    <style>
    /* Grey Background */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 50%, #1a1a1a 100%);
    }
    
    @keyframes greenGlow {
        0% { text-shadow: 0 0 10px rgba(0, 255, 136, 0.5), 0 0 20px rgba(0, 255, 136, 0.3); }
        50% { text-shadow: 0 0 20px rgba(0, 255, 136, 0.8), 0 0 40px rgba(0, 255, 136, 0.5); }
        100% { text-shadow: 0 0 10px rgba(0, 255, 136, 0.5), 0 0 20px rgba(0, 255, 136, 0.3); }
    }
    
    @keyframes flicker {
        0% { opacity: 0.9; }
        50% { opacity: 1; }
        100% { opacity: 0.9; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #00ff88;
        animation: greenGlow 2s ease-in-out infinite;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-title {
        font-size: 1.5rem;
        color: #00ff88;
        animation: flicker 1.5s ease-in-out infinite;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .tagline {
        font-size: 1.2rem;
        color: #cccccc;
        border-left: 4px solid #00ff88;
        padding-left: 1rem;
        margin: 1rem 0;
        text-align: left;
    }
    
    .profile-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeInUp 1s ease-out;
    }
    
    .profile-image {
        border-radius: 50%;
        border: 5px solid #00ff88;
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        transition: transform 0.3s ease;
        width: 200px;
        height: 200px;
        object-fit: cover;
    }
    
    .profile-image:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.6);
    }
    
    .default-avatar {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        padding: 2.5rem;
        border-radius: 50%;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        font-size: 5rem;
        color: #1a1a1a;
        border: 5px solid #00ff88;
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
        animation: float 3s ease-in-out infinite;
    }
    
    .default-avatar:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.6);
    }
    
    .upload-section {
        background: rgba(0, 255, 136, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 2px dashed #00ff88;
        margin-top: 1rem;
        text-align: center;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00ff88;
        margin: 2rem 0 1.5rem 0;
        border-bottom: 3px solid #00ff88;
        padding-bottom: 0.5rem;
        animation: slideInLeft 0.8s ease-out;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }
    
    .about-section {
        background: rgba(40, 40, 40, 0.8);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin: 1.5rem 0;
        border-left: 5px solid #00ff88;
    }
    
    .about-section h3 {
        color: #00ff88;
        font-size: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .about-section p {
        color: #cccccc;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    .about-card {
        background: rgba(40, 40, 40, 0.8);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border-top: 4px solid #00ff88;
    }
    
    .about-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.15);
        background: rgba(50, 50, 50, 0.8);
    }
    
    .about-card h4 {
        color: #00ff88;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .about-card p {
        color: #999999;
        font-size: 1rem;
        margin: 0;
    }
    
    .about-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #00ff88;
        margin: 0.5rem 0;
    }
    
    .skill-card {
        background: rgba(40, 40, 40, 0.8);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        animation: fadeInUp 0.8s ease-out;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 255, 136, 0.15);
        border-color: #00ff88;
    }
    
    .skill-card h4 {
        color: #cccccc;
    }
    
    .skill-card p {
        color: #00ff88;
    }
    
    .project-card {
        background: rgba(40, 40, 40, 0.8);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        height: 100%;
        animation: fadeInUp 0.8s ease-out;
        border-top: 4px solid #00ff88;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 255, 136, 0.15);
    }
    
    .project-card h3 {
        color: #00ff88;
    }
    
    .project-card p {
        color: #cccccc;
    }
    
    .experience-item {
        background: rgba(40, 40, 40, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00ff88;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        animation: slideInLeft 0.8s ease-out;
    }
    
    .experience-item:hover {
        box-shadow: 0 4px 8px rgba(0, 255, 136, 0.15);
    }
    
    .experience-item h3 {
        color: #00ff88;
    }
    
    .experience-item h4 {
        color: #00cc77;
    }
    
    .experience-item p {
        color: #cccccc;
    }
    
    .contact-card {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        padding: 2rem;
        border-radius: 15px;
        color: #1a1a1a;
        text-align: center;
        animation: fadeInUp 1s ease-out;
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
    }
    
    .contact-card h2 {
        color: #1a1a1a;
    }
    
    .social-icon {
        font-size: 2.5rem;
        margin: 0 0.5rem;
        transition: all 0.3s ease;
        color: #1a1a1a;
        text-decoration: none;
    }
    
    .social-icon:hover {
        transform: scale(1.2);
        color: #ffffff;
    }
    
    .cert-badge {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        color: #1a1a1a;
        display: inline-block;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .stat-box {
        background: rgba(40, 40, 40, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    .stat-box:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 255, 136, 0.15);
        border-color: #00ff88;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00ff88;
    }
    
    .stat-box p {
        color: #999999;
    }
    
    .info-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        color: #1a1a1a;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666666;
        border-top: 1px solid rgba(0, 255, 136, 0.3);
        margin-top: 2rem;
    }
    
    .demo-btn {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        color: #1a1a1a !important;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    .demo-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 25px rgba(0, 255, 136, 0.5);
        color: #1a1a1a !important;
        text-decoration: none;
    }
    
    .game-btn {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        color: #1a1a1a !important;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    .game-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 25px rgba(0, 255, 136, 0.5);
        color: #1a1a1a !important;
        text-decoration: none;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        color: #1a1a1a;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 25px rgba(0, 255, 136, 0.5);
    }
    
    .stMetric {
        background: rgba(40, 40, 40, 0.8);
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    .stMetric label {
        color: #999999 !important;
    }
    
    .stMetric div {
        color: #00ff88 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff88;
    }
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        .profile-image, .default-avatar {
            width: 150px;
            height: 150px;
            font-size: 3.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def render_header():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="profile-image-container">', unsafe_allow_html=True)
        
        # Show the permanent profile picture
        if st.session_state.profile_pic is not None:
            st.markdown(f"""
                <img src="{st.session_state.profile_pic}" 
                     class="profile-image" 
                     alt="Taha's Profile Picture">
            """, unsafe_allow_html=True)
        else:
            # Use the permanent profile from file
            img_data = load_profile_pic()
            if img_data is not None:
                st.markdown(f"""
                    <img src="{img_data}" 
                         class="profile-image" 
                         alt="Taha's Profile Picture">
                """, unsafe_allow_html=True)
            else:
                # Fallback to default avatar
                st.markdown("""
                    <div class="default-avatar">
                        ⚔️
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show upload button only if no profile picture is saved
        if not st.session_state.profile_pic_saved:
            with st.expander("📸 Upload Profile Picture", expanded=True):
                st.markdown('<div class="upload-section">', unsafe_allow_html=True)
                st.info("💡 **Upload once - it stays forever!** The picture will be saved permanently.")
                
                uploaded_file = st.file_uploader(
                    "Choose a photo...",
                    type=["jpg", "jpeg", "png", "gif"],
                    key="profile_uploader_permanent"
                )
                
                if uploaded_file is not None:
                    # Convert to base64
                    img = Image.open(uploaded_file)
                    # Resize to 200x200
                    img = img.resize((200, 200))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    img_data = f"data:image/png;base64,{img_base64}"
                    
                    # Save permanently
                    if save_profile_pic(img_data):
                        st.session_state.profile_pic = img_data
                        st.session_state.profile_pic_saved = True
                        st.success("")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to save profile picture. Please try again.")
                
                st.markdown("""
                    <p style="color: #999999; font-size: 0.8rem; margin-top: 0.5rem;">
                        💡 Once uploaded, the button will disappear and picture stays forever!
                    </p>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Show a message that profile is already set
            st.markdown("""
                <div style="background: rgba(0, 255, 136, 0.1); 
                            padding: 1rem; 
                            border-radius: 10px; 
                            border: 1px solid #00ff88;
                            text-align: center;
                            margin-top: 0.5rem;">
                    <p style="color: #00ff88; margin: 0;">
                        ✅ <strong>Profile picture is set!</strong>
                    </p>
                    <p style="color: #999999; font-size: 0.8rem; margin: 0.3rem 0 0 0;">
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="main-title">{PERSONAL_INFO["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-title">{PERSONAL_INFO["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tagline">{PERSONAL_INFO["tagline"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 1.1rem; color: #cccccc; margin: 1rem 0;">{PERSONAL_INFO["bio"]}</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.5rem 0;">
                <span class="info-badge">🎂 Age: {PERSONAL_INFO["age"]}</span>
                <span class="info-badge">📚 Class: {PERSONAL_INFO["class"]}</span>
                <span class="info-badge">📍 {PERSONAL_INFO["location"]}</span>
            </div>
        """, unsafe_allow_html=True)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown(f"📧 **Email**: {PERSONAL_INFO['email']}")
            st.markdown(f"📱 **Phone**: {PERSONAL_INFO['phone']}")
        with col4:
            st.markdown(f"📍 **Location**: {PERSONAL_INFO['location']}")
            st.markdown(f"🌐 **Website**: [{PERSONAL_INFO['website']}]({PERSONAL_INFO['website']})")
        with col5:
            st.markdown(f"""
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" style="font-size: 2rem; text-decoration: none;">🐙</a>
                    <a href="{PERSONAL_INFO['linkedin']}" target="_blank" style="font-size: 2rem; text-decoration: none;">💼</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="font-size: 2rem; text-decoration: none;">🐦</a>
                </div>
            """, unsafe_allow_html=True)

def render_about():
    """Render the About section with profile"""
    st.markdown('<div class="section-title">👤 About Me</div>', unsafe_allow_html=True)
    
    # Profile header with image and name
    col1, col2 = st.columns([1, 3])
    with col1:
        # Show the permanent profile picture
        if st.session_state.profile_pic is not None:
            st.markdown(f"""
                <div style="text-align: center;">
                    <img src="{st.session_state.profile_pic}" 
                         style="border-radius: 50%; width: 150px; height: 150px; border: 5px solid #00ff88; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);">
                    <div style="margin-top: 0.5rem;">
                        <span style="background: #00ff88; color: #1a1a1a; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">⭐ Verified</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            img_data = load_profile_pic()
            if img_data is not None:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <img src="{img_data}" 
                             style="border-radius: 50%; width: 150px; height: 150px; border: 5px solid #00ff88; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);">
                        <div style="margin-top: 0.5rem;">
                            <span style="background: #00ff88; color: #1a1a1a; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">⭐ Verified</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center;">
                        <div style="background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%); 
                                    border-radius: 50%; width: 150px; height: 150px; 
                                    display: flex; align-items: center; justify-content: center; 
                                    margin: auto; font-size: 4rem; color: #1a1a1a; 
                                    border: 5px solid #00ff88; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);">
                            ⚔️
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <span style="background: #00ff88; color: #1a1a1a; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">⭐ Verified</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
                <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                    <h1 style="font-size: 2.8rem; color: #00ff88; margin: 0; text-shadow: 0 0 30px rgba(0, 255, 136, 0.3);">
                        {PERSONAL_INFO['name']}
                    </h1>
                    <span style="background: #00ff88; color: #1a1a1a; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                        🚀 Active
                    </span>
                </div>
                <h3 style="color: #00cc77; margin: 0.2rem 0; font-size: 1.4rem;">{PERSONAL_INFO['title']}</h3>
                <div style="display: flex; gap: 1.5rem; margin: 0.5rem 0; flex-wrap: wrap;">
                    <span style="color: #cccccc;">📍 {PERSONAL_INFO['location']}</span>
                    <span style="color: #cccccc;">📧 {PERSONAL_INFO['email']}</span>
                    <span style="color: #cccccc;">📱 {PERSONAL_INFO['phone']}</span>
                </div>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap;">
                    <span class="info-badge">🎂 {PERSONAL_INFO['age']} Years</span>
                    <span class="info-badge">📚 {PERSONAL_INFO['class']}</span>
                    <span class="info-badge">🏆 3+ Projects</span>
                    <span class="info-badge">💻 8+ Skills</span>
                </div>
                <div style="display: flex; gap: 1rem; margin-top: 0.8rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" style="color: #00ff88; text-decoration: none; font-weight: 500;">🐙 GitHub</a>
                    <a href="{PERSONAL_INFO['linkedin']}" target="_blank" style="color: #00ff88; text-decoration: none; font-weight: 500;">💼 LinkedIn</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="color: #00ff88; text-decoration: none; font-weight: 500;">🐦 Twitter</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About content with better formatting
    st.markdown(f"""
        <div class="about-section">
            <div style="font-size: 1.1rem; line-height: 1.8; color: #cccccc;">
                {PERSONAL_INFO['about']}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats with icons
    st.markdown('<h3 style="font-size: 1.8rem; color: #00ff88; margin: 2rem 0 1rem 0; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">📊 Quick Stats</h3>', unsafe_allow_html=True)
    
    stats_data = [
        {"icon": "🎂", "value": "13", "label": "Years Old"},
        {"icon": "📍", "value": "PK", "label": "Pakistan"},
        {"icon": "🎯", "value": "2+", "label": "Coding Experience"},
        {"icon": "🚀", "value": "3+", "label": "Projects"},
        {"icon": "🏆", "value": "3", "label": "Certifications"},
        {"icon": "💻", "value": "8+", "label": "Skills"}
    ]
    
    cols = st.columns(6)
    for idx, stat in enumerate(stats_data):
        with cols[idx]:
            st.markdown(f"""
                <div class="about-card" style="border-top-color: #00ff88;">
                    <div style="font-size: 2rem;">{stat['icon']}</div>
                    <div class="value">{stat['value']}</div>
                    <p>{stat['label']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Journey Timeline
    st.markdown('<h3 style="font-size: 1.8rem; color: #00ff88; margin: 2rem 0 1rem 0; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">🗺️ My Journey</h3>', unsafe_allow_html=True)
    
    timeline_data = [
        {"year": "2023", "icon": "🌟", "title": "Started at Aptech", "description": "Began formal education in software engineering and Python development"},
        {"year": "2023", "icon": "🐍", "title": "First Python Project", "description": "Built first simple Python applications and learned programming fundamentals"},
        {"year": "2024", "icon": "🤖", "title": "AI Exploration", "description": "Started learning AI and machine learning concepts"},
        {"year": "2024", "icon": "💬", "title": "Chatbot Development", "description": "Built an AI chatbot using Python"},
        {"year": "2025", "icon": "🌐", "title": "Portfolio Website", "description": "Created this professional portfolio using Streamlit"},
        {"year": "2025", "icon": "🎮", "title": "Game Development", "description": "Developed Aircraft Shooter game with Pygame"}
    ]
    
    for item in timeline_data:
        st.markdown(f"""
            <div class="experience-item">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%); 
                                color: #1a1a1a; padding: 0.3rem 1rem; 
                                border-radius: 20px; font-weight: 600; 
                                min-width: 80px; text-align: center; 
                                box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">
                        {item['year']}
                    </span>
                    <span style="font-size: 1.8rem;">{item['icon']}</span>
                    <div>
                        <h4 style="margin: 0; color: #00ff88; font-size: 1.1rem;">{item['title']}</h4>
                        <p style="margin: 0.2rem 0 0 0; color: #999999; font-size: 0.95rem;">{item['description']}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Interests & Hobbies
    st.markdown('<h3 style="font-size: 1.8rem; color: #00ff88; margin: 2rem 0 1rem 0; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">🎯 Interests & Hobbies</h3>', unsafe_allow_html=True)
    
    interests = [
        {"icon": "🐍", "name": "Python Programming", "desc": "Building amazing projects with Python"},
        {"icon": "🤖", "name": "AI & Machine Learning", "desc": "Exploring the future of technology"},
        {"icon": "🎮", "name": "Game Development", "desc": "Creating fun and interactive games"},
        {"icon": "📚", "name": "Reading", "desc": "Learning new things every day"},
        {"icon": "🌐", "name": "Web Development", "desc": "Building beautiful websites with Streamlit"},
        {"icon": "🚀", "name": "Space & Science", "desc": "Fascinated by the universe"}
    ]
    
    cols = st.columns(3)
    for idx, interest in enumerate(interests):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="background: rgba(40, 40, 40, 0.8); 
                            padding: 1.2rem; 
                            border-radius: 12px; 
                            text-align: center;
                            border: 1px solid rgba(0, 255, 136, 0.15);
                            transition: all 0.3s ease;
                            margin-bottom: 0.5rem;">
                    <div style="font-size: 2.5rem;">{interest['icon']}</div>
                    <h4 style="color: #00ff88; margin: 0.3rem 0;">{interest['name']}</h4>
                    <p style="color: #888888; font-size: 0.85rem; margin: 0;">{interest['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Top Skills
    st.markdown('<h3 style="font-size: 1.8rem; color: #00ff88; margin: 2rem 0 1rem 0; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">⚡ Top Skills</h3>', unsafe_allow_html=True)
    
    top_skills = [
        {"name": "Python", "level": 95},
        {"name": "Streamlit", "level": 90},
        {"name": "Problem Solving", "level": 85},
        {"name": "Machine Learning", "level": 70},
        {"name": "Computer Vision", "level": 60}
    ]
    
    for skill in top_skills:
        st.markdown(f"""
            <div style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; color: #cccccc;">
                    <span>{skill['name']}</span>
                    <span style="color: #00ff88;">{skill['level']}%</span>
                </div>
                <div style="background: rgba(0, 255, 136, 0.1); border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #00cc77, #00ff88); 
                                width: {skill['level']}%; height: 8px; border-radius: 10px;
                                box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);">
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 204, 119, 0.15), rgba(0, 255, 136, 0.05)); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    text-align: center;
                    border: 1px solid rgba(0, 255, 136, 0.2);
                    margin-top: 2rem;">
            <h3 style="color: #00ff88; margin: 0;">💡 Let's Connect!</h3>
            <p style="color: #999999; margin: 0.5rem 0;">I'm always open to new opportunities, collaborations, and interesting conversations.</p>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
                <a href="mailto:haidertaha2026@gmail.com" style="background: #00ff88; color: #1a1a1a; padding: 0.5rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 600;">📧 Email Me</a>
                <a href="#" style="border: 2px solid #00ff88; color: #00ff88; padding: 0.5rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 600;">📄 View Resume</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_skills():
    st.markdown('<div class="section-title">🛠️ Skills & Expertise</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(list(SKILLS.keys()))
    
    for tab, (category, skills) in zip(tabs, SKILLS.items()):
        with tab:
            cols = st.columns(3)
            for idx, skill in enumerate(skills):
                with cols[idx % 3]:
                    st.markdown(f"""
                        <div class="skill-card">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📌</div>
                            <h4 style="color: #cccccc;">{skill['name']}</h4>
                            <div style="background: rgba(0, 255, 136, 0.15); border-radius: 10px; height: 12px; margin-top: 0.5rem; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #00cc77, #00ff88); 
                                            width: {skill['level']}%; height: 12px; border-radius: 10px;
                                            transition: width 1s ease-in-out;
                                            box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">
                                </div>
                            </div>
                            <p style="margin-top: 0.3rem; color: #00ff88; font-weight: 500;">{skill['level']}%</p>
                        </div>
                    """, unsafe_allow_html=True)

def render_experience():
    st.markdown('<div class="section-title">💼 Experience</div>', unsafe_allow_html=True)
    
    for exp in EXPERIENCE:
        st.markdown(f"""
            <div class="experience-item">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h3 style="margin: 0; color: #00ff88;">{exp['position']}</h3>
                        <h4 style="margin: 0.3rem 0; color: #00cc77;">{exp['company']}</h4>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%); color: #1a1a1a; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.9rem; box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);">
                            {exp['period']}
                        </span>
                        <p style="margin: 0.3rem 0 0 0; color: #cccccc; font-size: 0.9rem;">📍 {exp['location']}</p>
                    </div>
                </div>
                <ul style="margin-top: 0.8rem; padding-left: 1.2rem;">
                    {''.join([f'<li style="margin: 0.3rem 0; color: #cccccc;">{desc}</li>' for desc in exp['description']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)

def render_projects():
    st.markdown('<div class="section-title">🚀 Projects</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, project in enumerate(PROJECTS):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="project-card">
                    <div style="font-size: 3rem; text-align: center;">🚀</div>
                    <h3 style="text-align: center; color: #00ff88;">{project['title']}</h3>
                    <p style="color: #cccccc; text-align: center;">{project['description']}</p>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.3rem; justify-content: center; margin: 0.5rem 0;">
                        {''.join([f'<span style="background: linear-gradient(135deg, #00cc77 0%, #00ff88 100%); color: #1a1a1a; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500; box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);">{tech}</span>' for tech in project['technologies']])}
                    </div>
                    <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 0.5rem;">
                        <a href="{project['github']}" target="_blank" style="text-decoration: none; color: #00ff88; font-weight: 500;">📂 GitHub</a>
            """, unsafe_allow_html=True)
            
            if project['title'] == "AI Chatbot":
                if st.button("💬 Try Chatbot", key=f"chatbot_btn_{idx}", use_container_width=True):
                    st.session_state.page = "Chatbot"
                    st.session_state.show_chatbot = True
                    st.session_state.show_game = False
                    st.rerun()
            elif project['title'] == "Aircraft Shooter Game":
                if st.button("🎮 Play Game", key=f"game_btn_{idx}", use_container_width=True):
                    st.session_state.page = "Game"
                    st.session_state.show_game = True
                    st.session_state.show_chatbot = False
                    st.rerun()
            else:
                st.markdown(f"""
                        <a href="{project['demo']}" target="_blank" style="text-decoration: none; color: #00ff88; font-weight: 500;">🔗 Live Demo</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def render_education():
    st.markdown('<div class="section-title">🎓 Education</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, edu in enumerate(EDUCATION):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="experience-item" style="border-left-color: #00cc77;">
                    <h3 style="margin: 0; color: #00ff88;">{edu['degree']}</h3>
                    <h4 style="margin: 0.3rem 0; color: #00cc77;">{edu['school']}</h4>
                    <p style="color: #cccccc;">📅 {edu['year']} | GPA: {edu['gpa']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_certifications():
    st.markdown('<div class="section-title">📜 Certifications</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, cert in enumerate(CERTIFICATIONS):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <span class="cert-badge">🏅 {cert}</span>
                </div>
            """, unsafe_allow_html=True)

def render_stats():
    st.markdown('<div class="section-title">📊 Quick Stats</div>', unsafe_allow_html=True)
    
    stats = [
        {"label": "Projects Completed", "value": "3+"},
        {"label": "Programming Languages", "value": "1+"},
        {"label": "Certifications", "value": "3"},
        {"label": "Years Learning", "value": "2+"}
    ]
    
    cols = st.columns(4)
    for idx, stat in enumerate(stats):
        with cols[idx]:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{stat['value']}</div>
                    <p style="color: #999999; margin: 0.5rem 0 0 0; font-weight: 500;">{stat['label']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_testimonials():
    st.markdown('<div class="section-title">💬 Testimonials</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, testimonial in enumerate(TESTIMONIALS):
        with cols[idx % 2]:
            st.markdown(f"""
                <div style="background: rgba(40, 40, 40, 0.8); padding: 1.5rem; border-radius: 15px; 
                            border-left: 4px solid #00ff88; height: 100%;
                            animation: fadeInUp 0.8s ease-out;">
                    <p style="font-style: italic; color: #cccccc; font-size: 1.05rem;">"{testimonial['text']}"</p>
                    <p style="font-weight: 600; color: #00ff88; margin: 0.5rem 0 0 0;">- {testimonial['author']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_contact():
    st.markdown('<div class="section-title">📫 Get In Touch</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="contact-card">
            <h2 style="color: #1a1a1a; margin-bottom: 1rem;">Let's Connect!</h2>
            <p style="color: #1a1a1a; font-size: 1.1rem;">I'm always open to new opportunities and collaborations.</p>
            <div style="margin: 1.5rem 0;">
                <p style="color: #1a1a1a; font-size: 1.2rem;">✉️ {PERSONAL_INFO['email']}</p>
                <p style="color: #1a1a1a; font-size: 1.2rem;">📱 {PERSONAL_INFO['phone']}</p>
            </div>
            <div style="font-size: 2.5rem;">
                <a href="{PERSONAL_INFO['github']}" target="_blank" class="social-icon">🐙</a>
                <a href="{PERSONAL_INFO['linkedin']}" target="_blank" class="social-icon">💼</a>
                <a href="{PERSONAL_INFO['twitter']}" target="_blank" class="social-icon">🐦</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_analytics():
    """Render analytics dashboard"""
    st.markdown('<div class="section-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Profile Views", "1,234", "↑ 12%")
    with col2:
        st.metric("🚀 Projects", "3", "All Active")
    with col3:
        st.metric("💻 Skills", "8", "↑ 2 this month")
    with col4:
        st.metric("📚 Certifications", "3", "↑ 1 this month")
    
    st.markdown("---")
    
    st.markdown("### 🚀 Project Performance")
    project_data = {
        "AI Chatbot": 85,
        "Aircraft Game": 75,
        "Portfolio Website": 90
    }
    st.bar_chart(project_data)
    
    st.markdown("### 🎯 Skill Distribution")
    skill_data = {
        "Python": 95,
        "Streamlit": 90,
        "ML": 70,
        "Game Dev": 65,
        "Problem Solving": 85
    }
    st.bar_chart(skill_data)
    
    st.markdown("### 📈 Recent Activity")
    activities = [
        "✅ Updated Portfolio with new features",
        "🎮 Fixed game bugs in Aircraft Shooter",
        "🤖 Improved AI Chatbot responses",
        "📚 Completed Python Certification",
        "🚀 Launched new project"
    ]
    for activity in activities:
        st.write(f"• {activity}")

def render_chatbot_interface_full():
    """Render the full chatbot interface"""
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #00ff88; font-size: 3rem; text-shadow: 0 0 30px rgba(0, 255, 136, 0.3);">
                ⚔️ AI Chatbot Demo
            </h1>
            <p style="color: #cccccc;">Experience Taha's AI capabilities with 5 free questions! 💡</p>
            <p style="color: #00ff88; font-weight: 600;">⚡ 5 Questions Per Session ⚡</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_chatbot_interface()

def render_game_interface():
    """Render the full game interface"""
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #00ff88; font-size: 3rem; text-shadow: 0 0 30px rgba(0, 255, 136, 0.3);">
                ✈️ Aircraft Shooter Game
            </h1>
            <p style="color: #cccccc;">Defend the skies! Destroy all enemy aircraft! 🎯</p>
            <p style="color: #00ff88; font-weight: 600;">⚡ Single Level - Destroy 20 Enemies to Win ⚡</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("🎮 **The game will launch in a separate window.** Press ESC to exit the game.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            ### 🎯 Game Features
            - 20 enemies to destroy
            - 5 lives to survive
            - 3 enemy types
            - Score tracking
            - Keyboard controls
        """)
    with col2:
        st.markdown("""
            ### ⌨️ Controls
            - **WASD/Arrows**: Move
            - **SPACE**: Shoot
            - **ESC**: Exit game
            - **R**: Restart (when game over)
        """)
    
    if st.button("🚀 Launch Game", use_container_width=True):
        if launch_game():
            st.success("✅ Game launched in a new window!")
            st.balloons()
        else:
            st.error("❌ Failed to launch game. Make sure Pygame is installed.")

def main():
    """Main application function"""
    
    # Render sidebar if open
    if st.session_state.sidebar_open:
        render_sidebar()
    
    # Main content based on page
    if st.session_state.page == "About":
        render_about()
    elif st.session_state.page == "Chatbot" or st.session_state.show_chatbot:
        render_chatbot_interface_full()
    elif st.session_state.page == "Game" or st.session_state.show_game:
        render_game_interface()
    elif st.session_state.page == "Analytics":
        render_analytics()
    elif st.session_state.page == "Contact":
        render_contact()
    else:  # Home
        render_header()
        st.markdown("---")
        render_stats()
        render_skills()
        render_experience()
        render_projects()
        render_education()
        render_certifications()
        render_testimonials()
    
    # Footer
    st.markdown(f"""
        <div class="footer">
            <p style="font-size: 1.1rem;">© {datetime.now().year} {PERSONAL_INFO['name']}. All rights reserved.</p>
            <p style="font-size: 0.9rem; color: #555555;">Built with ❤️ using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
