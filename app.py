import streamlit as st
import numpy as np
import pickle
import base64
import os

# Page configuration
st.set_page_config(page_title="What's your spirit animal?", page_icon="🐾", layout="centered")

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
st.markdown("""<h1 style='color:black;'>🐾 What's your spirit animal?</h1>""", unsafe_allow_html=True)
st.markdown("<p style='color:black;'>Answer the questions to discover your spirit animal.</p>", unsafe_allow_html=True)

# Enneagram explanations
enneagram_types = {
    "1": "Type 1 – The Reformer: principled, purposeful, self-controlled.",
    "2": "Type 2 – The Helper: caring, interpersonal, generous.",
    "3": "Type 3 – The Achiever: success-oriented, adaptable, driven.",
    "4": "Type 4 – The Individualist: sensitive, introspective, expressive.",
    "5": "Type 5 – The Investigator: analytical, perceptive, private.",
    "6": "Type 6 – The Loyalist: committed, security-oriented, responsible.",
    "7": "Type 7 – The Enthusiast: spontaneous, versatile, optimistic.",
    "8": "Type 8 – The Challenger: self-confident, decisive, powerful.",
    "9": "Type 9 – The Peacemaker: easygoing, accommodating, reassuring."
}

# Animal profiles (add your full dictionary here, same as before)
from animal_profiles import animal_profiles

# Questions and options
questions = [
    "You begin your solo hike just after sunrise. What’s going through your head as you walk?",
    "You see a deer on the trail. What do you do?",
    "You sit beside a river. What color do you see in the reflection?",
    "You’re tasked with assembling a tent you’ve never used before. What do you do first?",
    "By the fire, you open your journal. What do you write about?",
    "At the river crossing, what kind of boat is waiting for you?",
    "Another hiker smiles at you. How do you respond?",
    "You reach a hilltop. What are you feeling?",
    "As you lie quietly in your tent under the stars, what mental image drifts into your mind?",
    "As the journey ends, what do you take home with you?"
]

options = [
    ["Reviewing goals and plans", "Tuned into nature's sounds", "Reflecting on something emotional", "Enjoying the moment, not thinking much"],
    ["Freeze and observe", "Take a photo", "Whisper something", "Step off the trail to give space"],
    ["Blue — calm", "Gold — energized", "Green — peaceful", "Grey — introspective"],
    ["I read the manual and follow each step carefully", "I scan the pieces and start putting it together based on feel", "I try to follow the steps, but keep second-guessing myself", "I skip the instructions and rely on trial and error"],
    ["Something emotional", "Gratitude for nature", "A new idea", "Someone I care about"],
    ["Canoe for one", "Sturdy rowboat", "Sailboat", "Large shared boat"],
    ["Smile and walk on", "Short chat", "Ask and share stories", "Invite to walk with me"],
    ["Clarity and purpose", "Deep calm", "Desire to share", "Creative inspiration"],
    ["A distant light flickering in the darkness", "The subtle sound of footsteps — something approaches", "Leaves rustling in the breeze above you", "A mountain partially hidden behind the clouds"],
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
    st.markdown("### 🌿 You're almost there!")
    if st.button("Discover My Spirit Animal 🐾"):
        input_array = np.array([st.session_state.answers])
        prediction = model.predict(input_array)[0]
        predicted_animal = label_encoder.inverse_transform([prediction])[0]

        profile = animal_profiles.get(predicted_animal, None)
        image_path = f"images/{predicted_animal.lower()}.png"

        if profile and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                encoded_img = base64.b64encode(img_file.read()).decode()

            enneagram_parts = profile['enneagram'].split(" or ")
            enneagram_explained = "<br>".join([f"{enneagram_types.get(e.strip(), '')}" for e in enneagram_parts])

            result_html = f"""
            <h2 style='color:black;'>🌟 Your Spirit Animal is: {predicted_animal} 🌟</h2>
            <div style="display: flex; align-items: center; gap: 2rem; flex-wrap: wrap; justify-content: flex-start;">
                <img src="data:image/png;base64,{encoded_img}" style="width:220px; border-radius:10px;" />
                <div style="flex: 1; min-width: 250px; text-align: left;">
                    {profile['description']}
                </div>
            </div>
            <br>
            <div style="text-align: left;">
                <strong>OCEAN Traits:</strong> {profile['ocean']}<br>
                <strong>MBTI Match:</strong> {profile['mbti']}<br>
                <strong>Enneagram Type:</strong><br>{enneagram_explained}
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)

    if st.button("Restart Quiz 🔄"):
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.rerun()
