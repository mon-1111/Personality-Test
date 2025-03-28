import streamlit as st
import numpy as np
import pickle
import base64

# Page configuration
st.set_page_config(page_title="Spirit Animal Finder", page_icon="🐾", layout="centered")

# Background setup
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

set_background("background.png")

# Load model and encoder
with open("rf_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Title
st.title("🐾 Spirit Animal Finder")
st.markdown("Answer the questions to discover your spirit animal.")

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

# Initialize session state variables
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.answers = []

# Display one question at a time
if st.session_state.current_q < len(questions):
    q_idx = st.session_state.current_q
    st.markdown(f"### Question {q_idx + 1} of {len(questions)}")
    answer = st.radio(questions[q_idx], options[q_idx], key=f"q{q_idx}")

    if st.button("Next"):
        # Save answer and proceed
        st.session_state.answers.append(options[q_idx].index(answer) + 1)
        st.session_state.current_q += 1
        st.experimental_rerun()

# After all questions answered, make prediction
else:
    st.markdown("### 🎉 You're almost there!")
    if st.button("Discover My Spirit Animal 🐾"):
        input_array = np.array([st.session_state.answers])
        prediction = model.predict(input_array)[0]
        predicted_animal = label_encoder.inverse_transform([prediction])[0]

        st.success(f"🌟 Your Spirit Animal is: **{predicted_animal}**")
        st.markdown(f"You share qualities with the **{predicted_animal}** — intuitive, driven, and deeply in tune with your inner world.")

    if st.button("Restart Quiz 🔄"):
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.experimental_rerun()
