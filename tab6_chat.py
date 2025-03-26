import streamlit as st
import sqlite3
import os
import re
from datetime import datetime
from html import escape
from streamlit_autorefresh import st_autorefresh
import hashlib

DB_PATH = "leapp_chat.db"

# === Initialize DB ===
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                msg TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()

def render_tab6(tab6):
    with tab6:
        init_db()

        st.header("💬 LeDiscussion: Group Chat for LeBron Fans")

        st.markdown("""
        <style>
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
                box-shadow: 0 1px 4px rgba(255,255,255,0.05);
            }
            .chat-user {
                color: #d4aaff;
            }
            .chat-timestamp {
                color: #aaa;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        st_autorefresh(interval=10000, key="chat_autorefresh")

        if "chat_input_temp" not in st.session_state:
            st.session_state.chat_input_temp = ""
        if "reactions" not in st.session_state:
            st.session_state.reactions = {}

        def add_message(user, msg, timestamp):
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO chat_messages (user, msg, timestamp) VALUES (?, ?, ?)", (user, msg, timestamp))
                conn.commit()

        def get_messages(limit=50):
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("SELECT user, msg, timestamp FROM chat_messages ORDER BY id DESC LIMIT ?", (limit,))
                rows = c.fetchall()
            return [{"user": r[0], "msg": r[1], "timestamp": r[2]} for r in rows]


        def clear_chat():
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM chat_messages")
                conn.commit()

        def parse_message(msg):
            msg = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', msg)
            return escape(msg).replace("\n", "<br>")

        def get_user_color(username):
            hex_color = hashlib.md5(username.encode()).hexdigest()[:6]
            return f"#{hex_color}"

        def add_reaction(msg_id, emoji):
            if msg_id not in st.session_state.reactions:
                st.session_state.reactions[msg_id] = {}
            st.session_state.reactions[msg_id][emoji] = st.session_state.reactions[msg_id].get(emoji, 0) + 1

        # 💬 Message Input
        with st.form(key="chat_form", clear_on_submit=True):
            user_message = st.text_input("Your Message", key="chat_input_temp", max_chars=200)
            submitted = st.form_submit_button("Send")
            if submitted:
                msg = user_message.strip()
                if msg:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    add_message(st.session_state.current_user, msg, now)

        # 📜 Message History
        chat_history = get_messages()
        st.subheader("📜 Chat History")
        for i, chat in enumerate(chat_history):
            parsed_msg = parse_message(chat["msg"])
            user_color = get_user_color(chat["user"])
            timestamp = chat["timestamp"]
            msg_id = f"{chat['user']}_{timestamp}_{i}"

            st.markdown(f"""
            <div class="chat-bubble" title="Sent at {timestamp}">
                <span class="chat-user" style="color: {user_color}">{chat['user']}</span>
                <span class="chat-timestamp">{timestamp}</span><br>
                {parsed_msg}
            </div>
            """, unsafe_allow_html=True)
            # Horizontal emoji buttons with real Streamlit buttons
            # st.markdown(
            #     """
            #     <style>
            #     .emoji-row {
            #         display: flex;
            #         gap: 12px;
            #         margin-top: 6px;
            #         margin-bottom: 12px;
            #     }
            #     .emoji-row button {
            #         padding: 6px 14px;
            #         font-size: 0.9rem;
            #         border-radius: 6px;
            #     }
            #     </style>
            #     """,
            #     unsafe_allow_html=True
            # )

            # # Render buttons in a single row using Streamlit columns with narrow gaps
            # with st.container():
            #     col1, col2, col3 = st.columns([1, 1, 1], gap="small")

            #     with col1:
            #         if st.button(f"👍 {st.session_state.reactions.get(msg_id, {}).get('👍', 0)}", key=f"{msg_id}_like"):
            #             add_reaction(msg_id, "👍")
            #     with col2:
            #         if st.button(f"🔥 {st.session_state.reactions.get(msg_id, {}).get('🔥', 0)}", key=f"{msg_id}_fire"):
            #             add_reaction(msg_id, "🔥")
            #     with col3:
            #         if st.button(f"😂 {st.session_state.reactions.get(msg_id, {}).get('😂', 0)}", key=f"{msg_id}_lol"):
            #             add_reaction(msg_id, "😂")




        # 🔐 Admin option to clear chat
        if st.session_state.current_user == "admin":
            if st.button("🧹 Clear Chat History"):
                clear_chat()
                st.success("Chat history cleared.")
