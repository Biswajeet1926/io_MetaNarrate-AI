import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from io import BytesIO
import re
from concurrent.futures import ThreadPoolExecutor
