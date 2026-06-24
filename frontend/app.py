import streamlit as st
import os, sys

# Add backend folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from fusion_engine import fuse_inputs
from event_tracker import save_event, get_events
from art_generator import generate_art

st.set_page_config(page_title="DreamWeaver AI", layout="wide", page_icon="🌌")

st.markdown(
    """
    <style>
    .title {
        color: #6A5ACD;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #555555;
        font-family: 'Segoe UI', sans-serif;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .timeline-card {
        padding: 1rem;
        border: 1px solid #e6e6fa;
        border-radius: 14px;
        background: #fbf8ff;
        margin-bottom: 1rem;
    }
    .timeline-card strong {
        color: #4b0082;
    }
    .timeline-card p {
        margin: 0.25rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='title'>🌌 DreamWeaver AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A local dream art generator that fuses text, image, and audio into surreal visuals without external API keys.</p>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])
with col_left:
    text_input = st.text_area("✨ Dream fragment (text)", height=180)
    image_input = st.file_uploader("🖼️ Sketch or image", type=["png", "jpg", "jpeg"])
    audio_input = st.file_uploader("🎧 Audio clip", type=["wav", "mp3"])
    if audio_input:
        st.audio(audio_input, format="audio/wav")

with col_right:
    st.markdown("### Input notes")
    st.write("- Share a short dream phrase or feeling.")
    st.write("- Upload a sketch to inspire the scene.")
    st.write("- Add audio for mood and atmosphere.")
    st.write("\n")
    st.markdown("**Tip:** CPU generation is slower; GPU is faster if available.")

if st.button("Generate Dream"):
    inputs = []
    if text_input:
        inputs.append(f"Text: {text_input}")
    if image_input:
        inputs.append(f"Image: {image_input.name}")
    if audio_input:
        inputs.append(f"Audio: {audio_input.name}")

    if not inputs:
        st.warning("Add at least one input before generating your dream.")
    else:
        dream_description = fuse_inputs(inputs)
        save_event(inputs, dream_description)

        status_text = st.empty()
        status_text.info("Still generating… hang tight. This may take a few seconds.")
        with st.spinner("Generating dream imagery... this may take a moment"):
            art = generate_art(dream_description, save=False)
        status_text.empty()

        result_col, art_col = st.columns([1, 1.2])
        with result_col:
            st.markdown("<h2 style='color:#6A5ACD;'>✨ Dream Description</h2>", unsafe_allow_html=True)
            st.write(dream_description)
            st.markdown("**Captured Inputs:**")
            for item in inputs:
                st.write(f"- {item}")

        with art_col:
            st.markdown("<h2 style='color:#6A5ACD;'>🎨 Dream Visual</h2>", unsafe_allow_html=True)
            if art is not None:
                st.image(art, caption="AI‑Generated Dream Visual", use_column_width=True)
            else:
                st.warning("Could not generate the visual. Please try again or check the backend model setup.")

st.markdown("<h2 style='color:#6A5ACD;'>🕒 Dream Timeline</h2>", unsafe_allow_html=True)
events = get_events(limit=5)
if events:
    for ts, inp, desc in events:
        st.markdown(
            f"<div class='timeline-card'><strong>{ts}</strong><p><strong>Inputs:</strong> {inp}</p><p><strong>Description:</strong> {desc}</p></div>",
            unsafe_allow_html=True,
        )
else:
    st.info("No dreams recorded yet. Generate one to start your timeline.")
