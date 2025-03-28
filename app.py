import streamlit as st
import numpy as np
import pickle
import base64

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
        div[class*="stRadio"] label, div[class*="stRadio"] div, .stMarkdown, .stTitle {{
            color: black !important;
        }}
        .stApp {{
            padding-left: 50px;  
            padding-right: 50px;
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
st.title("🐾 Spirit Animal Finder")
st.markdown("Answer the questions to discover your spirit animal.")

# Animal personality profiles
animal_profiles = {
    "Bear": """You share qualities with the **Bear** — characterized by high Introversion (OCEAN), introspection, and thoughtfulness. 
    Often aligning with INFJ or INTJ (MBTI), you have deep inner wisdom and emotional intuition, reflecting Enneagram types 4 or 5, known for their profound emotional depth and analytical thinking.""",

    "Cat": """You align closely with the **Cat** — independent, observant, and adaptable. In OCEAN, you exhibit higher Openness and moderate Introversion. Typically resembling ISFP or INTP (MBTI), your traits match Enneagram type 5 or 9, driven by a desire for peace and knowledge.""",

    "Dolphin": """You resonate with the **Dolphin** — energetic, outgoing, and social. High in Extraversion and Agreeableness (OCEAN), you often reflect ESFP or ENFP (MBTI) personality types. Your playful and empathetic nature aligns closely with Enneagram types 2 or 7.""",

    "Elephant": """You match the **Elephant** — wise, cooperative, and empathetic. Exhibiting high Agreeableness and Conscientiousness (OCEAN), your personality aligns closely with ISFJ or ESFJ (MBTI). You often reflect Enneagram types 2 or 6, highlighting loyalty and helpfulness.""",

    "Fox": """You share traits with the **Fox** — clever, resourceful, and adaptable. Typically high in Openness and Conscientiousness (OCEAN), aligning with ENTP or INTJ (MBTI). Your dynamic, strategic personality aligns with Enneagram types 3 or 5.""",

    "Lion": """You embody the **Lion** — confident, assertive, and natural leader. High in Extraversion and low Neuroticism (OCEAN), typically matching ENTJ or ESTJ (MBTI). Your assertive and ambitious personality aligns closely with Enneagram types 3 or 8.""",

    "Owl": """You match the **Owl** — analytical, wise, and introspective. High Openness and Introversion (OCEAN), resembling INTP or INTJ (MBTI). Known for intellectual curiosity and independent thinking, often aligning with Enneagram type 5.""",

    "Parrot": """You align with the **Parrot** — expressive, enthusiastic, and sociable. Highly Extraverted and Open (OCEAN), often resembling ESFP or ENFP (MBTI). You are cheerful and expressive, aligning closely with Enneagram types 7 or 2.""",

    "Snake": """You share traits with the **Snake** — intuitive, calm, and mysterious. You exhibit higher Introversion, moderate Openness, and emotional stability (OCEAN). Typically INFJ or INFP (MBTI), aligning strongly with Enneagram type 4, reflecting emotional depth and introspection.""",

    "Tiger": """You resonate with the **Tiger** — brave, dynamic, and assertive. High in Extraversion, moderate Neuroticism (OCEAN), closely matching ESTP or ENFP (MBTI). Energetic and action-oriented, aligning closely with Enneagram types 7 or 8.""",

    "Turtle": """You identify with the **Turtle** — calm, patient, and resilient. Exhibiting high Agreeableness, low Extraversion (OCEAN), typically matching ISFJ or ISTJ (MBTI). You often align with Enneagram type 9, seeking harmony and steadiness.""",

    "Wolf": """You reflect qualities of the **Wolf** — loyal, intuitive, and community-oriented. Balanced Extraversion and Agreeableness (OCEAN), often INFJ or ENFJ (MBTI). You resonate deeply with Enneagram types 6 or 9, focused on trust, loyalty, and group harmony."""
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

# Initialize session state
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.answers = []

# Display questions one by one
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

        st.success(f"🌟 Your Spirit Animal is: **{predicted_animal}**")

        message = animal_profiles.get(predicted_animal, "You have a unique spirit!")
        st.markdown(message)

    if st.button("Restart Quiz 🔄"):
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.rerun()
