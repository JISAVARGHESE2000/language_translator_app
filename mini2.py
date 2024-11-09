import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# Custom button styling with HTML
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;  /* Darker green */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("Language Translation App")

# Add image on top
st.image(r"C:\Users\HP\OneDrive\Desktop\python\pythonProject1\bmi\lld_wordle.jpg", use_column_width=True)

# Source text input
source_text = st.text_area("Enter text to translate:", height=100)

# Language selection for translation
target_language = st.selectbox("Select target language:", list(LANGUAGES.values()))

# Source language detection and selection
translator = Translator()
detected_lang = None
if source_text:
    detected_lang = translator.detect(source_text).lang
    st.write(f"Detected language: {LANGUAGES.get(detected_lang, 'Unknown')}")

# Buttons for interaction
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    translate_button = st.button('Translate')
with col2:
    tts_button = st.button('Hear Translation')
with col3:
    clear_button = st.button('Clear')

# Translation logic
if translate_button:
    if not source_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        target_lang_code = [code for code, lang in LANGUAGES.items() if lang == target_language][0]
        translation = translator.translate(source_text, src=detected_lang, dest=target_lang_code)
        st.subheader("Translated Text:")
        st.write(translation.text)

        # Store translation in session state
        if 'translations' not in st.session_state:
            st.session_state['translations'] = []
        st.session_state['translations'].append(translation.text)

# Display translation history
if 'translations' in st.session_state and st.session_state['translations']:
    with st.sidebar:
        st.write("Translation History")
        for i, translated_text in enumerate(st.session_state['translations']):
            st.write(f"{i + 1}. {translated_text}")

# Text-to-Speech logic
if tts_button and source_text:
    target_lang_code = [code for code, lang in LANGUAGES.items() if lang == target_language][0]
    translation = translator.translate(source_text, src=detected_lang, dest=target_lang_code)
    tts = gTTS(translation.text, lang=target_lang_code)
    tts.save("translated_audio.mp3")
    audio_file = open("translated_audio.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
    audio_file.close()
    os.remove("translated_audio.mp3")

# Clear button logic
if clear_button:
    st.session_state['translations'] = []

