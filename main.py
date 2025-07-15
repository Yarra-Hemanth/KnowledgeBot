import streamlit as st
import requests
import json
from datetime import datetime
from state import initialize_state, get_timestamp

# === Page Config ===
st.set_page_config(page_title="KnowledgeBot", page_icon="💬", layout="centered")

# === Initialize Session State ===
initialize_state()
messages = st.session_state.all_sessions[st.session_state.current_session]

# === UI ===
from ui import render_sidebar, render_header, render_messages, handle_chat_input

render_sidebar(messages)
render_header()
render_messages(messages)
handle_chat_input(messages)
