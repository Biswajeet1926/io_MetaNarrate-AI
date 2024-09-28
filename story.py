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

@stl.cache_data(ttl=3600)
def gen_st_starter(genre: str, tone: str) -> str:
    prompt = f"Create a brief, engaging story starter for a {genre} story with a {tone} tone."
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"}
    ]
    return generate_content(prompt, safety_settings)

def gen_aud_pl_html(audio_base64):
    return f"""
        <audio controls autoplay=true>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """

def wrd_cnt(text):
    return len(re.findall(r'\w+', text))

stl.title("🌟 AI Storyteller: Interactive Narrative Creation")
stl.write("Embark on a journey of collaborative storytelling with AI. Shape your narrative and watch it come to life!")

with stl.sidebar:
    stl.header("📝 Story Settings")
    with stl.container():
        stl.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        genre = stl.selectbox("Choose your genre", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Historical Fiction"])
        tone = stl.selectbox("Set the tone", ["Humorous", "Dark", "Inspirational", "Suspenseful", "Whimsical", "Melancholic", "Upbeat"])
        length = stl.select_slider("Continuation length", options=["Short", "Medium", "Long"], value="Medium")
        stl.markdown('</div>', unsafe_allow_html=True)

    if stl.button("🔄 Start New Story", key="new_story"):
        with stl.spinner("Generating a new story starter..."):
            gen_ns = gen_st_starter(genre, tone)
            if not gen_ns.startswith("Content generation was blocked") and not gen_ns.startswith("Unable to generate content"):
                stl.session_state.story_context = gen_ns
                stl.session_state.full_story = gen_ns
                stl.session_state.turn_count = 0
                stl.success("New story started successfully!")
            else:
                stl.error(gen_ns)
        stl.rerun()

if "story_context" not in stl.session_state:
    stl.session_state.story_context = gen_st_starter(genre, tone)
if "full_story" not in stl.session_state:
    stl.session_state.full_story = stl.session_state.story_context
if "turn_count" not in stl.session_state:
    stl.session_state.turn_count = 0
stl.header("📜 Your Unfolding Tale")
with stl.container():
    stl.markdown('<div class="story-container">', unsafe_allow_html=True)
    stl.markdown(stl.session_state.full_story)
    stl.markdown('</div>', unsafe_allow_html=True)

stl.header("✍ Shape Your Narrative")
user_input = stl.text_area("What happens next in your story?", "", height=100)

col1, col2 = stl.columns(2)
with col1:
    if stl.button("🚀 Continue Story", key="continue"):
        if user_input:
            with stl.spinner("Weaving your ideas into the narrative tapestry..."):
                next_part = gen_st(stl.session_state.story_context, user_input, genre, tone, length)
            
            if not next_part.startswith("Content generation was blocked") and not next_part.startswith("Unable to generate content"):
                stl.session_state.story_context += f"\nUser Input: {user_input}\nAI Response: {next_part}"
                stl.session_state.full_story += f"\n\n{next_part}"
                stl.session_state.turn_count += 1

                stl.success("🌟 The story continues...")
                with stl.container():
                    stl.markdown('<div class="story-container">', unsafe_allow_html=True)
                    stl.markdown(next_part)
                    stl.markdown('</div>', unsafe_allow_html=True)

                with stl.spinner("Generating audio..."):
                    with ThreadPoolExecutor() as executor:
                        new_part_audio = executor.submit(gen_aud, next_part).result()
                if new_part_audio:
                    stl.markdown("🔊 Listen to the new part:")
                    stl.markdown(gen_aud_pl_html(new_part_audio), unsafe_allow_html=True)
            else:
                stl.warning(next_part)
        else:
            stl.warning("Please enter some input to continue the story.")

with col2:
    if stl.button("🎭 Surprise Me", key="surprise"):
        with stl.spinner("Crafting an unexpected turn of events..."):
            surprise_input = generate_content(f"Generate a surprising event for a {genre} story with a {tone} tone.", [])
            if not surprise_input.startswith("Content generation was blocked") and not surprise_input.startswith("Unable to generate content"):
                next_part = gen_st(stl.session_state.story_context, surprise_input, genre, tone, length)
                
                if not next_part.startswith("Content generation was blocked") and not next_part.startswith("Unable to generate content"):
                    stl.session_state.story_context += f"\nSurprise Event: {surprise_input}\nAI Response: {next_part}"
                    stl.session_state.full_story += f"\n\n{next_part}"
                    stl.session_state.turn_count += 1

                    stl.success("🎉 A twist in the tale!")
                    with stl.container():
                        stl.markdown('<div class="story-container">', unsafe_allow_html=True)
                        stl.markdown(next_part)
                        stl.markdown('</div>', unsafe_allow_html=True)

                
                    with stl.spinner("Generating audio..."):
                        with ThreadPoolExecutor() as executor:
                            new_part_audio = executor.submit(gen_aud, next_part).result()
                    if new_part_audio:
                        stl.markdown("🔊 Listen to the surprise twist:")
                        stl.markdown(gen_aud_pl_html(new_part_audio), unsafe_allow_html=True)
                else:
                    stl.warning(next_part)
            else:
                stl.warning(surprise_input)
