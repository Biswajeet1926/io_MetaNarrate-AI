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

gai.configure(api_key=stl.secrets["GOOGLE_API_KEY"])

def access_model():
    return gai.GenerativeModel('gemini-1.5-flash')

m = access_model()

def generate_content(prompt, safety_settings):
    try:
        r = m.generate_content(prompt, safety_settings=safety_settings)
        
        if r.parts:
            return r.text
        elif hasattr(r, 'prompt_feedback'):
            br = [rating.reason for rating in r.prompt_feedback.safety_ratings if rating.probability == "HIGH"]
            if br:
                return f"Content generation was blocked due to potential safety concerns: {', '.join(br)}. Please try a different input."
            else:
                return "Content generation was blocked. Please try a different input."
        else:
            return "Unable to generate content. Please try again with a different input."
    except Exception as e:
        stl.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please try again."

def gen_aud(text: str, lang: str = 'en'):
    try:
        tts = gTTS(text=text, lang=lang)
        au_bu = BytesIO()
        tts.write_to_fp(au_bu)
        au_by = au_bu.getvalue()
        return base64.b64encode(au_by).decode()
    except Exception as e:
        stl.error(f"An error occurred while generating audio: {str(e)}")
        return None


def gen_st(context: str, user_input: str, genre: str, tone: str, length: str) -> str:
    prompt = (
        f"Continue the story based on the current context and the user's input.\n"
        f"Context: {context}\n"
        f"User Input: {user_input}\n"
        f"Genre: {genre}\n"
        f"Tone: {tone}\n"
        f"Length: {length}\n"
        f"Continue the story in an engaging and creative way, keeping the narrative cohesive and dynamic. "
        f"Maintain the specified genre and tone throughout."
    )
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"}
    ]
    return generate_content(prompt, safety_settings)
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

gai.configure(api_key=stl.secrets["GOOGLE_API_KEY"])

def access_model():
    return gai.GenerativeModel('gemini-1.5-flash')

m = access_model()

def generate_content(prompt, safety_settings):
    try:
        r = m.generate_content(prompt, safety_settings=safety_settings)
        
        if r.parts:
            return r.text
        elif hasattr(r, 'prompt_feedback'):
            br = [rating.reason for rating in r.prompt_feedback.safety_ratings if rating.probability == "HIGH"]
            if br:
                return f"Content generation was blocked due to potential safety concerns: {', '.join(br)}. Please try a different input."
            else:
                return "Content generation was blocked. Please try a different input."
        else:
            return "Unable to generate content. Please try again with a different input."
    except Exception as e:
        stl.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please try again."

def gen_aud(text: str, lang: str = 'en'):
    try:
        tts = gTTS(text=text, lang=lang)
        au_bu = BytesIO()
        tts.write_to_fp(au_bu)
        au_by = au_bu.getvalue()
        return base64.b64encode(au_by).decode()
    except Exception as e:
        stl.error(f"An error occurred while generating audio: {str(e)}")
        return None


def gen_st(context: str, user_input: str, genre: str, tone: str, length: str) -> str:
    prompt = (
        f"Continue the story based on the current context and the user's input.\n"
        f"Context: {context}\n"
        f"User Input: {user_input}\n"
        f"Genre: {genre}\n"
        f"Tone: {tone}\n"
        f"Length: {length}\n"
        f"Continue the story in an engaging and creative way, keeping the narrative cohesive and dynamic. "
        f"Maintain the specified genre and tone throughout."
    )
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"}
    ]
    return generate_content(prompt, safety_settings)
