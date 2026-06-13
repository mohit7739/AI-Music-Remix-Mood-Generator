import streamlit as st
import os
import pandas as pd
from utils import audio_processor, mood_detector, remix_generator, visualizer, chatbot

# Page config
st.set_page_config(page_title="AI Music Remix & Mood Generator", page_icon="🎵", layout="wide")

# Custom CSS for dark theme accents
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #00ffcc;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎵 AI Music Remix & Mood Generator")
st.markdown("Upload a track, discover its mood, and generate AI-powered remix ideas!")

# Sidebar
with st.sidebar:
    st.header("Settings & Upload")
    hf_api_key = st.text_input("Hugging Face API Key (Optional for Chat)", type="password")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=['mp3', 'wav'])

# Initialize session state
if 'features' not in st.session_state:
    st.session_state.features = None
if 'y' not in st.session_state:
    st.session_state.y = None
if 'sr' not in st.session_state:
    st.session_state.sr = None
if 'pydub_audio' not in st.session_state:
    st.session_state.pydub_audio = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

# Process uploaded file
if uploaded_file is not None and uploaded_file.name != st.session_state.file_name:
    with st.spinner("Analyzing audio... This may take a moment."):
        file_bytes = uploaded_file.read()
        
        # Load for librosa
        # Save temporarily to let librosa load it (librosa prefers file paths for some formats)
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
            
        try:
            y, sr = audio_processor.load_audio(temp_path)
            st.session_state.y = y
            st.session_state.sr = sr
            st.session_state.features = audio_processor.extract_features(y, sr)
            
            # Load for pydub
            file_ext = uploaded_file.name.split('.')[-1]
            st.session_state.pydub_audio = audio_processor.load_pydub_audio(file_bytes, format=file_ext)
            st.session_state.file_name = uploaded_file.name
        except Exception as e:
            st.error(f"Error processing audio: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if st.session_state.features is not None:
    # Top level metrics
    col1, col2, col3 = st.columns(3)
    features = st.session_state.features
    
    top_mood, mood_scores = mood_detector.predict_mood(features)
    genre_scores = mood_detector.predict_genre(features)
    top_genre = list(genre_scores.keys())[0]
    
    col1.metric("Predicted Mood", top_mood)
    col2.metric("Predicted Genre", top_genre)
    col3.metric("Tempo (BPM)", f"{int(features['tempo'])}")
    
    # Audio Player
    st.audio(uploaded_file, format=f'audio/{uploaded_file.name.split(".")[-1]}')
    
    st.markdown("---")
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visual Analytics", "🎛️ Remix & Prompts", "🎧 Audio Effects", "💬 AI Assistant"])
    
    with tab1:
        st.header("Visual Analytics Dashboard")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Waveform")
            fig_wave = visualizer.plot_waveform(st.session_state.y, st.session_state.sr)
            st.pyplot(fig_wave)
            
            st.subheader("Mood Radar")
            fig_mood = visualizer.plot_mood_chart(mood_scores)
            st.plotly_chart(fig_mood, use_container_width=True)
            
        with c2:
            st.subheader("Mel Spectrogram")
            fig_spec = visualizer.plot_spectrogram(st.session_state.y, st.session_state.sr)
            st.pyplot(fig_spec)
            
            st.subheader("Genre Probabilities")
            fig_genre = visualizer.plot_genre_probabilities(genre_scores)
            st.plotly_chart(fig_genre, use_container_width=True)
            
    with tab2:
        st.header("Remix & AI Prompt Generator")
        remix_genre = st.selectbox("Select Target Remix Genre", 
                                  ["EDM Remix", "Lo-fi Remix", "Chill Remix", "Rock Remix", "Classical Remix", "Synthwave Remix"])
        
        remix_ideas = remix_generator.generate_remix_ideas(remix_genre, features['tempo'])
        
        st.subheader("Production Ideas")
        st.write(f"**Vibe:** {remix_ideas['description']}")
        st.write(f"**Recommended Tempo:** {remix_ideas['tempo_recommendation']}")
        st.write(f"**Instruments:** {', '.join(remix_ideas['instruments'])}")
        st.write(f"**Beat Pattern:** {remix_ideas['beat_pattern']}")
        st.info(f"**Production Notes:** {remix_ideas['production_notes']}")
        
        st.markdown("---")
        st.subheader("AI Prompt Generator")
        st.write("Use this prompt in tools like Suno AI, MusicGen, or Stable Audio:")
        prompt = remix_generator.generate_ai_prompt(remix_genre, top_mood, features['tempo'])
        st.code(prompt, language="text")
        
    with tab3:
        st.header("Audio Effects")
        st.write("Apply basic effects to preview ideas.")
        
        effect_choice = st.selectbox("Select Effect", ["None", "Speed Up (1.2x)", "Slow Down (0.8x)", "Bass Boost (+5dB)"])
        
        if st.button("Apply Effect"):
            with st.spinner("Applying effect..."):
                modified_audio = st.session_state.pydub_audio
                if effect_choice == "Speed Up (1.2x)":
                    modified_audio = audio_processor.apply_speed_change(modified_audio, 1.2)
                elif effect_choice == "Slow Down (0.8x)":
                    modified_audio = audio_processor.apply_speed_change(modified_audio, 0.8)
                elif effect_choice == "Bass Boost (+5dB)":
                    modified_audio = audio_processor.apply_bass_boost(modified_audio, 5)
                
                if effect_choice != "None":
                    out_bytes = audio_processor.export_audio(modified_audio, format="mp3")
                    st.audio(out_bytes, format="audio/mp3")
                    st.download_button(label="Download Modified Audio",
                                       data=out_bytes,
                                       file_name=f"modified_{st.session_state.file_name.split('.')[0]}.mp3",
                                       mime="audio/mp3")
    with tab4:
        st.header("AI Production Assistant")
        if not hf_api_key:
            st.warning("Please enter your Hugging Face API key in the sidebar to chat with the assistant.")
        
        st.write("Ask for music production tips, instrument choices, or how to improve your track.")
        user_query = st.text_area("Your Question:")
        if st.button("Ask Assistant"):
            if user_query:
                with st.spinner("Thinking..."):
                    context_prompt = f"Context: The user uploaded a {top_genre} track at {int(features['tempo'])} BPM with a {top_mood} mood. Question: {user_query}"
                    response = chatbot.get_chat_response(context_prompt, hf_api_key)
                    st.write("🤖 **Assistant:**")
                    st.write(response)
            else:
                st.error("Please enter a question.")
else:
    st.info("👈 Upload an audio file in the sidebar to get started!")
