import streamlit as st
import numpy as np
import pickle
import base64
import os

# Page configuration
st.set_page_config(page_title="Spirit Animal Finder", page_icon="🐾", layout="centered")

# Function to set background
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        div[class*="stRadio"] label, div[class*="stRadio"] div, .stMarkdown, .stTitle, .stHeading {{
            color: black !important;
        }}
        .stApp {{
            padding-left: 50px;  
            padding-right: 50px;
        }}
        .result-box {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            color: black;
        }}
        .result-row {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .result-img {{
            width: 250px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image
set_background("background.png")

# Load model and label encoder
with open("rf_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Title
st.markdown("""<h1 style='color:black;'>🐾 Spirit Animal Finder</h1>""", unsafe_allow_html=True)
st.markdown("<p style='color:black;'>Answer the questions to discover your spirit animal.</p>", unsafe_allow_html=True)

# Full profile information
animal_profiles = {
    "Bear": {
        "description": "You share qualities with the <strong>Bear</strong> — introspective, grounded, and protective. You thrive in calm, reflective environments and prefer solitude or deep one-on-one connections. You tend to think before acting and offer wisdom to others. You positively impact your world by providing emotional depth, quiet leadership, and a reliable presence.",
        "ocean": "High Introversion, High Conscientiousness",
        "mbti": "INFJ / INTJ",
        "enneagram": "4 or 5"
    },
    "Cat": {
        "description": "You align with the <strong>Cat</strong> — independent, curious, and highly perceptive. You thrive when given freedom and space, and you prefer doing things in your own unique way. You tend to quietly observe before engaging and positively impact others by modeling authenticity, insight, and quiet resilience.",
        "ocean": "High Openness, Moderate Introversion",
        "mbti": "ISFP / INTP",
        "enneagram": "5 or 9"
    },
    "Dolphin": {
        "description": "You resonate with the <strong>Dolphin</strong> — playful, empathetic, and social. You thrive in group settings and prefer uplifting, meaningful interactions. You tend to bring people together and lighten the mood. You positively impact others by spreading joy, empathy, and creative energy.",
        "ocean": "High Extraversion, High Agreeableness",
        "mbti": "ESFP / ENFP",
        "enneagram": "2 or 7"
    },
    "Elephant": {
        "description": "You reflect the <strong>Elephant</strong> — wise, nurturing, and loyal. You thrive in structured, value-based environments and prefer taking care of others and being part of a close-knit group. You tend to lead with quiet strength and positively impact the world by being dependable and emotionally intelligent.",
        "ocean": "High Agreeableness, High Conscientiousness",
        "mbti": "ISFJ / ESFJ",
        "enneagram": "2 or 6"
    },
    "Fox": {
        "description": "You embody the <strong>Fox</strong> — clever, quick-witted, and adaptable. You thrive in fast-paced environments and prefer to stay ahead of the curve. You tend to think on your feet and positively impact others by offering solutions, strategy, and creative insight.",
        "ocean": "High Openness, High Conscientiousness",
        "mbti": "ENTP / INTJ",
        "enneagram": "3 or 5"
    },
    "Lion": {
        "description": "You are the <strong>Lion</strong> — courageous, strong, and born to lead. You thrive in situations where bold decisions are needed and prefer to take initiative. You tend to inspire others through confidence and vision. You positively impact others by leading with integrity and bravery.",
        "ocean": "High Extraversion, Low Neuroticism",
        "mbti": "ENTJ / ESTJ",
        "enneagram": "3 or 8"
    },
    "Owl": {
        "description": "You connect with the <strong>Owl</strong> — wise, observant, and thoughtful. You thrive in intellectual and philosophical spaces and prefer deep conversations over small talk. You tend to seek truth and knowledge. You positively impact others by offering insight, perspective, and clarity.",
        "ocean": "High Openness, High Introversion",
        "mbti": "INTP / INTJ",
        "enneagram": "5"
    },
    "Parrot": {
        "description": "You align with the <strong>Parrot</strong> — expressive, social, and enthusiastic. You thrive in vibrant environments and prefer to be surrounded by people and ideas. You tend to uplift those around you and positively impact others with your energy, humor, and optimism.",
        "ocean": "High Extraversion, High Openness",
        "mbti": "ESFP / ENFP",
        "enneagram": "7 or 2"
    },
    "Snake": {
        "description": "You share traits with the <strong>Snake</strong> — intuitive, calm, and transformative. You thrive in introspective and emotionally rich environments and prefer deep reflection. You tend to sense what others miss and positively impact others by encouraging healing, transformation, and growth.",
        "ocean": "High Introversion, Moderate Openness",
        "mbti": "INFJ / INFP",
        "enneagram": "4"
    },
    "Tiger": {
        "description": "You resonate with the <strong>Tiger</strong> — fierce, passionate, and bold. You thrive in high-energy settings and prefer to chase goals fearlessly. You tend to act decisively and inspire with intensity. You positively impact others through your strength, determination, and fearlessness.",
        "ocean": "High Extraversion, Moderate Neuroticism",
        "mbti": "ESTP / ENFP",
        "enneagram": "7 or 8"
    },
    "Turtle": {
        "description": "You identify with the <strong>Turtle</strong> — patient, wise, and grounded. You thrive in peaceful, steady environments and prefer a slower, thoughtful pace. You tend to be a grounding presence. You positively impact others through stability, calm, and timeless wisdom.",
        "ocean": "High Agreeableness, Low Extraversion",
        "mbti": "ISFJ / ISTJ",
        "enneagram": "9"
    },
    "Wolf": {
        "description": "You reflect the <strong>Wolf</strong> — loyal, intuitive, and community-focused. You thrive in strong, supportive networks and prefer meaningful collaboration. You tend to sense emotional dynamics well. You positively impact others by fostering connection, loyalty, and collective strength.",
        "ocean": "Balanced Extraversion and Agreeableness",
        "mbti": "INFJ / ENFJ",
        "enneagram": "6 or 9"
    }
}

# Questions and options
questions = [
    "You begin your solo hike just after sunrise. What’s going through your head as you walk?",
    "You see a deer on the trail. What do you do?",
    "You sit beside a river. What color do you see in the reflection?",
    "You arrive at a clearing to set up camp. How do you go about it?",
    "By the fire, you open your journal. What do you write about?",
    "At the river crossing, what kind of boat is waiting for you?",
    "Another hiker smiles at you. How do you respond?",
    "You reach a high ridge. What are you feeling?",
    "Lying in your tent, what image comes to mind first?",
    "As the journey ends, what do you take home with you?"
]


options = [
    ["Reviewing goals and plans", "Tuned into nature's sounds", "Reflecting on something emotional", "Enjoying the moment, not thinking much"],
    ["Freeze and observe", "Take a photo", "Whisper something", "Step off the trail to give space"],
    ["Blue — calm", "Gold — energized", "Green — peaceful", "Grey — introspective"],
    ["Planned everything ahead", "Go with the flow", "Try but second-guess", "Hands-on improvisation"],
    ["Something emotional", "Gratitude for nature", "A new idea", "Someone I care about"],
    ["Canoe for one", "Sturdy rowboat", "Sailboat", "Large shared boat"],
    ["Smile and walk on", "Short chat", "Ask and share stories", "Invite to walk with me"],
    ["Clarity and purpose", "Deep calm", "Desire to share", "Creative inspiration"],
    ["A distant light", "An approaching animal", "Swaying tree", "Mountain behind clouds"],
    ["Inner strength", "Nature connection", "Inspiration", "Peace and gratitude"]
]

if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.answers = []

if st.session_state.current_q < len(questions):
    q_idx = st.session_state.current_q
    st.markdown(f"### Question {q_idx + 1} of {len(questions)}")
    answer = st.radio(questions[q_idx], options[q_idx], key=f"q{q_idx}")
    if st.button("Next"):
        st.session_state.answers.append(options[q_idx].index(answer) + 1)
        st.session_state.current_q += 1
        st.rerun()
else:
    st.markdown("### 🎉 You're almost there!")
    if st.button("Discover My Spirit Animal 🐾"):
        input_array = np.array([st.session_state.answers])
        prediction = model.predict(input_array)[0]
        predicted_animal = label_encoder.inverse_transform([prediction])[0]

        profile = animal_profiles.get(predicted_animal, None)
        image_path = f"images/{predicted_animal.lower()}.png"

        if profile:
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:black;'>🌟 Your Spirit Animal is: {predicted_animal}</h2>", unsafe_allow_html=True)
            if os.path.exists(image_path):
                st.image(image_path, width=250)
            st.markdown(profile["description"], unsafe_allow_html=True)
            st.markdown(f"<br><strong>OCEAN Traits:</strong> {profile['ocean']}<br>", unsafe_allow_html=True)
            st.markdown(f"<strong>MBTI Match:</strong> {profile['mbti']}<br>", unsafe_allow_html=True)
            st.markdown(f"<strong>Enneagram Type:</strong> {profile['enneagram']}</div>", unsafe_allow_html=True)

    if st.button("Restart Quiz 🔄"):
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.rerun()
