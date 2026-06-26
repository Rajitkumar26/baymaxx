import streamlit as st
from groq import Groq
import time
import requests

st.set_page_config(layout="wide", page_title="Baymax - Friendly Neighborhood AI By Rajit D R", page_icon="🤖")

def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Set up the Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL_NAME = "llama-3.3-70b-versatile"

lottie_html = """
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<div style="display: flex; justify-content: right; align-items: right; height: 500vh;">
    <dotlottie-player src="https://lottie.host/4ff3d5f4-1d6b-4f35-ac12-ac93de643c6e/3Ic3MV6yIu.lottie"
                      background="transparent" speed="1" style="width: 150px; height: 150px" loop autoplay>
    </dotlottie-player>
</div>
"""

st.components.v1.html(lottie_html, height=150, width=150)

st.markdown("""
    <h1 style='color: black; text-align: center;'>Baymax - Your friendly neighborhood AI</h1>
    <p style='color: black; text-align: center;'>Hello Human! I am Baymax. I was created by Rajit DR. I am here to fetch you valuable information whenever you need some!</p>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .stApp {
            background: url('https://img.freepik.com/free-vector/pastel-ombre-background-pink-purple_53876-120750.jpg') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
        }
        .message-box {
            display: flex;
            margin: 10px 0;
        }
        .user-message {
            background-color: #74EBD5;
            background-image: linear-gradient(90deg, #74EBD5 0%, #9FACE6 100%);
            color: black;
            padding: 10px 20px;
            border-radius: 15px;
            margin-left: auto;
            max-width: 70%;
            word-wrap: break-word;
        }
        .ai-message {
            background-color: #4158D0;
            background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        input[type="text"] {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        .stButton>button {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_message_displayed' not in st.session_state:
    st.session_state.last_message_displayed = True

def typewrite_effect(text):
    placeholder = st.empty()
    typewritten_text = ""
    for char in text:
        typewritten_text += char
        placeholder.markdown(f'<div class="ai-message">{typewritten_text}</div>', unsafe_allow_html=True)
        time.sleep(0.006)
    placeholder.markdown(f'<div class="ai-message">{text}</div>', unsafe_allow_html=True)

def build_messages():
    messages = [{"role": "system", "content": "You are Baymax, a friendly and caring AI assistant created by Rajit DR."}]
    for message in st.session_state.history:
        role = "user" if message['role'] == 'user' else "assistant"
        messages.append({"role": role, "content": message['text']})
    return messages

def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append({'role': 'user', 'text': user_input})

        messages = build_messages()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=1,
            max_tokens=2048,
        )

        reply_text = response.choices[0].message.content

        st.session_state.history.append({'role': 'chatbot', 'text': reply_text})
        st.session_state.last_message_displayed = False
        st.session_state.user_input = ""

for idx, message in enumerate(st.session_state.history):
    if message['role'] == 'user':
        st.markdown(f'<div class="message-box"><div class="user-message">{message["text"]}</div></div>', unsafe_allow_html=True)
    elif idx == len(st.session_state.history) - 1 and not st.session_state.last_message_displayed:
        typewrite_effect(message["text"])
        st.session_state.last_message_displayed = True
    else:
        st.markdown(f'<div class="message-box"><div class="ai-message">{message["text"]}</div></div>', unsafe_allow_html=True)

st.text_input("You:", key="user_input", placeholder="Type your message here...", on_change=handle_input)

if st.button('Reset Chat'):
    st.session_state.history = []
    st.session_state.last_message_displayed = True
    st.write("Chat has been reset.")