import streamlit as st
import numpy as np
import pickle
import base64

# Define the background function first
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
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Call the background function here
set_background("background.png")

# Load model and label encoder
with open("rf_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# App config
st.set_page_config(page_title="Spirit Animal Finder", page_icon="🧿", layout="centered")
st.title("🧭 Spirit Animal Finder")
st.markdown("Answer the 10 questions below to discover your spirit animal.")

# List of questions and options (same as yours)
questions = [...]
options = [...]

# Collect user input
answers = []
for i, question in enumerate(questions):
    answer = st.radio(f"**Q{i+1}. {question}**", options[i], index=0, key=f"q{i+1}")
    answers.append(options[i].index(answer) + 1)

# Prediction
if st.button("Find My Spirit Animal 🐾"):
    input_array = np.array([answers])
    prediction = model.predict(input_array)[0]
    predicted_animal = label_encoder.inverse_transform([prediction])[0]
    st.success(f"🌟 Your Spirit Animal is: **{predicted_animal}**")
    st.markdown(f"You share qualities with the **{predicted_animal}** — intuitive, driven, and deeply in tune with your inner world.")
