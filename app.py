

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Gemini AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini AI Chatbot")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Initialize chat session and message history in Streamlit state
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful, friendly, and concise AI assistant."
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(model="gemini-2.5-flash")
        st.rerun()

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
            except Exception as e:
                st.error(f"Error generating response: {e}")
