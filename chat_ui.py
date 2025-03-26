import streamlit as st
from utils.chat_utils import parse_message, get_user_color, get_msg_id

def inject_chat_styles():
    st.markdown("""<style>
    .chat-bubble {
        background-color: #ffffff;
        color: #111111;
        padding: 0.6rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        font-size: 0.95rem;
        line-height: 1.4;
        position: relative;
        word-wrap: break-word;
        overflow-wrap: anywhere;
        max-width: 100%;
    }
    .chat-user {
        font-weight: 600;
        color: #4b0082;
    }
    .chat-timestamp {
        font-size: 0.7rem;
        color: #999999;
        position: absolute;
        top: 6px;
        right: 10px;
    }
    @media (prefers-color-scheme: dark) {
        .chat-bubble {
            background-color: #1f1f1f;
            color: #f0f0f0;
        }
        .chat-user {
            color: #d4aaff;
        }
        .chat-timestamp {
            color: #aaa;
        }
    }
    </style>""", unsafe_allow_html=True)

def render_chat_message(chat, i):
    msg_id = get_msg_id(chat["user"], chat["timestamp"], i)
    parsed_msg = parse_message(chat["msg"])
    user_color = get_user_color(chat["user"])
    timestamp = chat["timestamp"]

    st.markdown(f"""
    <div class="chat-bubble" title="Sent at {timestamp}">
        <span class="chat-user" style="color: {user_color}">{chat['user']}</span>
        <span class="chat-timestamp">{timestamp}</span><br>
        {parsed_msg}
    </div>
    """, unsafe_allow_html=True)
