import streamlit as st
import json
import requests
from state import get_timestamp

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"
OLLAMA_MODEL = "tinyllama:1.1b"

def render_sidebar(messages):
    st.sidebar.title("🗂️ Chat Sessions")

    # Handle new session creation
    if st.sidebar.button("➕ New Session"):
        session_id = get_timestamp()
        st.session_state.current_session = session_id
        st.session_state.all_sessions[session_id] = [
            {"role": "assistant", "content": "Hi Hemanth, how can I assist you?"}
        ]
        st.rerun()  # Force rerun to update UI

    # Display existing sessions
    st.sidebar.markdown("### Existing Sessions")
    for sid in sorted(st.session_state.all_sessions.keys(), reverse=True):
        if sid == st.session_state.current_session:
            st.sidebar.markdown(f"- **{sid}**")
        else:
            if st.sidebar.button(f"{sid}", key=f"switch_{sid}"):
                st.session_state.current_session = sid
                st.rerun()

    # Chat export
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="Download Chat",
        data=json.dumps(messages, indent=2),
        file_name=f"chat_{st.session_state.current_session.replace(':', '-')}.json",
        mime="application/json"
    )


def render_header():
    st.markdown("<h1 style='text-align:center;'>💬 KnowledgeBot </h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:18px;'> - Powered by an <b>Offline LLM</b></p>", unsafe_allow_html=True)
    st.markdown("---")

def render_messages(messages):
    for msg in messages:
        align = "right" if msg["role"] == "user" else "left"
        bg_color = "#dcf8c6" if msg["role"] == "user" else "#f1f0f0"
        st.markdown(f"""
        <div style='text-align:{align}; background-color:{bg_color}; color:#000; padding:10px; margin:10px; border-radius:10px; max-width:80%; float:{align}; clear:both;'>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

def handle_chat_input(messages):
    prompt = st.chat_input("Type your message...")
    if prompt:
        messages.append({"role": "user", "content": prompt})
        show_user_bubble(prompt)

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a concise and professional chatbot. Respond only with direct, short, and relevant answers."
                        "Do not ask for user goals unless specifically requested."
                        "Avoid marketing language. Do not ask follow-up questions unless prompted."
                    )
                },
                *messages
            ],
            "stream": True
        }

        response_text = stream_response(payload)
        messages.append({"role": "assistant", "content": response_text})
        st.session_state.all_sessions[st.session_state.current_session] = messages

def show_user_bubble(text):
    st.markdown(f"""
    <div style='text-align:right; background-color:#dcf8c6; color:#000; padding:10px; margin:10px; border-radius:10px; max-width:80%; float:right; clear:both;'>
        {text}
    </div>
    """, unsafe_allow_html=True)

def stream_response(payload):
    response_text = ""
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        placeholder = st.empty()
        placeholder.markdown(loading_bubble(), unsafe_allow_html=True)

        for line in r.iter_lines():
            if line:
                if line.startswith(b"data: "):
                    line = line.replace(b"data: ", b"")
                decoded_line = line.decode("utf-8").strip()
                if not decoded_line or decoded_line == "[DONE]":
                    continue
                try:
                    data = json.loads(decoded_line)
                    delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    response_text += delta
                    placeholder.markdown(bot_bubble(response_text), unsafe_allow_html=True)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        st.error(f"❌ Error: {e}")
        response_text = "Sorry, something went wrong."
    return response_text

def loading_bubble():
    return """
    <div style='text-align:left; background-color:#f1f0f0; padding:10px; margin:10px; border-radius:10px; max-width:80%; float:left; clear:both;'>
        <span class="typing-dot"></span>
        <span class="typing-dot" style="animation-delay: 0.2s;"></span>
        <span class="typing-dot" style="animation-delay: 0.4s;"></span>
    </div>
    <style>
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 5px;
        background-color: #555;
        border-radius: 50%;
        animation: blink 1.4s infinite;
    }
    @keyframes blink {
        0%, 80%, 100% { opacity: 0; }
        40% { opacity: 1; }
    }
    </style>
    """



def bot_bubble(text):
    return f"""
    <div style='text-align:left; background-color:#f1f0f0; color:#000; padding:10px; margin:10px; border-radius:10px; max-width:80%; float:left; clear:both;'>
        {text}
    </div>
    """
def loading_dots():
    return """
    <span class="typing-dot"></span>
    <span class="typing-dot" style="animation-delay: 0.2s;"></span>
    <span class="typing-dot" style="animation-delay: 0.4s;"></span>
    <style>
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-left: 3px;
        background-color: #555;
        border-radius: 50%;
        animation: blink 1.4s infinite;
    }
    @keyframes blink {
        0%, 80%, 100% { opacity: 0; }
        40% { opacity: 1; }
    }
    </style>
    """
