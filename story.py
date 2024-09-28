import streamlit as st   #Used for creating and deploying the web application interface.
import google.generativeai as genai   #Provides access to Google's Gemini AI model.
from gtts import gTTS  #Google Text-to-Speech library for audio generation.
import base64   #Used for encoding audio data for web playback.

# BytesIO stores it in the computer's memory (RAM). This can be much faster for certain operations, especially when dealing with smaller amounts of data.
from io import BytesIO   #Allows working with bytes in memory.

import re   #Regular expressions module for word counting.
from concurrent.futures import ThreadPoolExecutor   #Enables concurrent execution for performance improvement. Speeding up I/O-bound tasks. Parallelizing CPU-bound tasks

# Web page configuration
st.set_page_config(page_title="Interactive AI Storyteller", page_icon="📚", layout="wide")

# Applies custom CSS for styling the application. The unsafe_allow_html=True allows the use of HTML in the markdown.
st.markdown("""
<style>
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .story-container, .sidebar-content {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)   
# Configuration for Google Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
