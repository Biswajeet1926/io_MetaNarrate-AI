import streamlit as stl  
import google.generativeai as gai   
from gtts import gTTS 
import base64 
from io import BytesIO  
import re  
from concurrent.futures import ThreadPoolExecutor

stl.set_page_config(page_title="Interactive AI Storyteller", page_icon="📚", layout="wide")
stl.markdown("""
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

stl.logo("https://play-lh.googleusercontent.com/QIez0eyZVAi_EvKssJmsn8nlgC024DWjmUrRmTMNvUb06-BIbQuYi1HJwuHfdF-w")
stl.sidebar.markdown("MetaNarrate AI")
gai.configure(api_key=stl.secrets["GOOGLE_API_KEY"])
@stl.cache_resource
def get_model():
    return gai.GenerativeModel('gemini-1.5-flash')
model = get_model()
def generate_content(prompt, safety_settings):
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        if response.parts:
            return response.text
        elif hasattr(response, 'prompt_feedback'):
            blocked_reasons = [rating.reason for rating in response.prompt_feedback.safety_ratings if rating.probability == "HIGH"]
            if blocked_reasons:
                return f"Content generation was blocked due to potential safety concerns: {', '.join(blocked_reasons)}. Please try a different input."
            else:
                return "Content generation was blocked. Please try a different input."
        else:
            return "Unable to generate content. Please try again with a different input."
    except Exception as e:
        stl.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please try again."
