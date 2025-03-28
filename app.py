import streamlit as st

st.set_page_config(page_title="Spirit Animal Finder", layout="centered")

# Spirit animal descriptions
animal_traits = {
    "Wolf": "loyal, instinctive, and thrives in both solitude and community.",
    "Owl": "wise, perceptive, and drawn to deep knowledge and mysteries.",
    "Dolphin": "playful, empathetic, and deeply connected to social bonds.",
    "Lion": "courageous, confident, and a natural leader.",
    "Butterfly": "transformative, adaptable, and embraces change with grace.",
    "Bear": "strong, protective, and deeply introspective.",
    "Fox": "clever, agile, and always thinking three steps ahead.",
    "Elephant": "gentle, strong, and values deep connections and memories.",
    "Snake": "intuitive, driven, and deeply in tune with your inner world.",
    "Deer": "sensitive, graceful, and guided by compassion.",
    "Tiger": "fierce, passionate, and unafraid of challenges.",
    "Turtle": "wise, patient, and carries a deep sense of inner peace."
}

# Styling
st.markdown(
    """
    <style>
    h1, .spirit-result {
        color: black !important;
    }
    .result-box {
        background-color: #d3f2dd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown("<h1 class='title'>🐾 Spirit Animal Finder</h1>", unsafe_allow_html=True)
st.write("Answer the questions to discover your spirit animal.")

# Placeholder for questions (this is a mockup — integrate your actual questions here)
if "answers" not in st.session_state:
    st.session_state.answers = []

# Simulated final step
st.markdown("### 🎉 You're almost there!")

if st.button("Discover My Spirit Animal 🐾"):
    # This is where your scoring logic goes; here we pick a random animal
    import random
    spirit_animal = random.choice(list(animal_traits.keys()))
    st.session_state.spirit_animal = spirit_animal

if "spirit_animal" in st.session_state:
    animal = st.session_state.spirit_animal
    traits = animal_traits[animal]

    st.markdown(f"""
    <div class='result-box'>
        <span class='spirit-result'>🌟 <strong>Your Spirit Animal is: <span style='color:black'>{animal}</span></strong></span><br><br>
        You share qualities with the <strong>{animal}</strong> — {traits}
    </div>
    """, unsafe_allow_html=True)

    st.button("Restart Quiz 🔁", on_click=lambda: st.session_state.clear())
