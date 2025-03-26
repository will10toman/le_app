import streamlit as st
from streamlit_autorefresh import st_autorefresh
from logic.chat_db import init_db, add_message, get_messages, clear_chat
from ui.chat_ui import render_chat_message, inject_chat_styles
from utils.chat_utils import parse_message, get_user_color, get_msg_id
from datetime import datetime

def render_tab6(tab6):
    with tab6:
        init_db()
        st.header("💬 LeDiscussion: Group Chat for LeBron Fans")
        inject_chat_styles()
        st_autorefresh(interval=10000, key="chat_autorefresh")

        if "chat_input_temp" not in st.session_state:
            st.session_state.chat_input_temp = ""
        if "reactions" not in st.session_state:
            st.session_state.reactions = {}

        # 💬 Message Input
        with st.form(key="chat_form", clear_on_submit=True):
            user_message = st.text_input("Your Message", key="chat_input_temp", max_chars=200)
            submitted = st.form_submit_button("Send")
            if submitted and user_message.strip():
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                add_message(st.session_state.current_user, user_message.strip(), now)

        # 📜 Chat History
        st.subheader("📜 Chat History")
        chat_history = get_messages()
        for i, chat in enumerate(chat_history):
            render_chat_message(chat, i)

        # 🔐 Admin Option
        if st.session_state.current_user == "admin":
            if st.button("🧹 Clear Chat History"):
                clear_chat()
                st.success("Chat history cleared.")
