import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit.components.v1 as components

import hashlib
import os


st.set_page_config(page_title="LeApp | The LeBron Experience", layout="wide")
import sqlite3




# --- Database Setup ---
DB_NAME = "users.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

# --- Password Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- User Storage using SQLite ---
def save_user(email, username, password_hash):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, password_hash)
            )
            conn.commit()
        return "Success"
    except sqlite3.IntegrityError as e:
        if "username" in str(e).lower():
            return "Username already exists"
        elif "email" in str(e).lower():
            return "Email already registered"
        else:
            return "Unknown error occurred"

def authenticate(username, password):
    password_hash = hash_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password_hash)
        )
        return cursor.fetchone() is not None

# --- Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- Login / Sign Up Interface ---
if not st.session_state.authenticated:
    st.title("🔐 Welcome to LeApp")
    st.subheader("Login or Sign Up to Access the LeBron James Experience")

    auth_mode = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)

    if auth_mode == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:  # Sign Up
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            result = save_user(email, username, hash_password(password))
            if result == "Success":
                st.success("Account created. You can now log in.")
            else:
                st.error(result)

    st.stop()

# ================================
# If user is authenticated, show app
# ================================
if st.session_state.authenticated:
    st.sidebar.success(f"👑 Logged in as {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = ""
        st.rerun()


    # ⬇️ Place your entire app content BELOW this point:
    # Page config, tabs, LeResume, LeLive, LeTalk, LeDiscussion, etc.

    st.markdown("""
        <style>
        /* Default: light mode */
        .stApp {
            background-color: #f9f9f9;
            color: #111111;
        }
        h1, h2, h3, h4, p, span, label {
            color: #222222;
        }
        .stMarkdown > div {
            background-color: #ffffff;
            color: #111111;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 1px 8px rgba(0,0,0,0.05);
        }
        input, textarea {
            background-color: #f2f2f2;
            color: #111111;
        }

        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #0e1117;
                color: #f0f0f0;
            }
            h1, h2, h3, h4, p, span, label {
                color: #f0f0f0;
            }
            .stMarkdown > div {
                background-color: #1e1e1e;
                color: #f0f0f0;
                box-shadow: 0 1px 6px rgba(255,255,255,0.1);
            }
            input, textarea {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            section[data-testid="stSidebar"] {
                background-color: #1a1a1a;
                color: #f0f0f0;
            }
        }
        </style>
        """, unsafe_allow_html=True)


    # Title (always at the top)
    st.title("👑 LeApp: The LeBron James Experience 👑")

    st.markdown("""
        <style>
        /* Container for both views */
        .lebron-container {
            position: relative;
            width: 100%;
        }

        /* Desktop version: float top-right */
        .lebron-img-desktop {
            position: absolute;
            top: 0.5rem;
            right: 0;
            width: 240px;
            z-index: 10;
        }

        /* Mobile version: hidden by default */
        .lebron-img-mobile {
            display: none;
            margin-top: 1rem;
            text-align: center;
        }

        /* Tighten spacing under title */
        .block-container h1 {
            margin-bottom: 0.2rem;
        }

        .block-container {
            padding-top: 1rem !important;
        }

        /* Mobile view override */
        @media (max-width: 768px) {
            .lebron-img-desktop {
                display: none !important;
            }

            .lebron-img-mobile {
                display: block;
            }
        }
        </style>

        <div class="lebron-container">
            <!-- Desktop Image -->
            <img src="https://i.imgur.com/NRHdCTs.png" class="lebron-img-desktop">
        </div>

        <!-- Mobile Image -->
        <div class="lebron-img-mobile">
            <img src="https://i.imgur.com/NRHdCTs.png" width="160">
        </div>
    """, unsafe_allow_html=True)




    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 LeResume", 
        "🕒 LeLive", 
        "🎤 Bronify", 
        "🛡️ LeDefend", 
        "🧠 LeTalk", 
        "💬 LeDiscussion"
    ])

    # ========== TAB 1 ==========
    with tab1:
        st.header("📈 LeResume: Career Stats (Live from NBA API)")

        player_id = "2544"
        seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(2003, 2025)]
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com"}

        all_data = []
        for season in seasons:
            params = {
                "PlayerID": player_id,
                "Season": season,
                "SeasonType": "Regular Season"
            }
            try:
                res = requests.get("https://stats.nba.com/stats/playergamelog", params=params, headers=headers, timeout=10)
                data = res.json()
                columns = data["resultSets"][0]["headers"]
                rows = data["resultSets"][0]["rowSet"]
                df = pd.DataFrame(rows, columns=columns)
                df["Season"] = season
                all_data.append(df)
            except:
                continue

        if not all_data:
            st.error("❌ No data loaded from NBA API.")
            st.stop()

        career_df = pd.concat(all_data)
        career_df["GAME_DATE"] = pd.to_datetime(career_df["GAME_DATE"])
        career_df = career_df.sort_values("GAME_DATE")

        # Season selector
        all_seasons = ["Career"] + seasons[::-1]
        selected_season = st.selectbox("Select a season", all_seasons)

        if selected_season == "Career":
            display_df = career_df.copy()
        else:
            display_df = career_df[career_df["Season"] == selected_season]

        # Season averages
        avg_pts = display_df["PTS"].mean()
        avg_ast = display_df["AST"].mean()
        avg_reb = display_df["REB"].mean()

        st.subheader(f"{selected_season} Averages")
        st.write({
            "Points Per Game": round(avg_pts, 1),
            "Assists Per Game": round(avg_ast, 1),
            "Rebounds Per Game": round(avg_reb, 1)
        })

        # Chart logic
        if selected_season == "Career":
            season_averages = career_df.groupby("Season")[["PTS"]].mean().reset_index()
            st.subheader("Points Per Game by Season")
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(season_averages["Season"], season_averages["PTS"], marker="o", color="goldenrod", linewidth=2)
            ax.set_title("LeBron's PPG Each Season", fontsize=10)
            ax.set_xlabel("Season")
            ax.set_ylabel("PTS")
            ax.set_xticks(range(len(season_averages["Season"])))
            ax.set_xticklabels(season_averages["Season"], rotation=45, ha="right", fontsize=8)
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.subheader(f"{selected_season} Game-by-Game Points")
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(display_df["GAME_DATE"], display_df["PTS"], marker="o", linestyle="-", color="purple", alpha=0.7)
            ax.set_title(f"LeBron's Points – {selected_season}", fontsize=10)
            ax.set_xlabel("Date")
            ax.set_ylabel("PTS")
            fig.autofmt_xdate()
            st.pyplot(fig)

        st.subheader("👑 Why LeBron Is the Greatest")
        st.markdown("""
        - 🏆 **4× NBA Champion**
        - 👑 **All-Time Leading Scorer**
        - 🧠 **First with 30K points, 10K boards, 10K dimes**
        - 🗓️ **20+ Seasons of Greatness**
        - 🏀 **Most All-NBA Selections**
        - 💪 **19 straight 25+ PPG seasons**
        """)

        st.subheader("🔥 Top 10 Scoring Games")
        top_games = career_df.sort_values("PTS", ascending=False).head(10)
        st.dataframe(top_games[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST"]].reset_index(drop=True))

    # TAB 2
    from lebron_next_game import render_tab2
    render_tab2(tab2)

    # TAB 3
    with tab3:
        st.header("🎤 Bronify: Parody Songs About the King")
        st.markdown("""
        - 🎶 *"LeMVP Baby"*  
        - 🎶 *"Can't Stop LeBron"*  
        - 🎶 *"King of the Court"*
        """)

    # TAB 4
    with tab4:
        st.header("🛡️ LeDefend: Fight the Hate, Defend the King")
        st.warning("Coming soon: Real-time hate tweet detection.")
        st.caption("“Not everyone sees the crown. That’s why we wear it loud.”")
    # ========== TAB 5 ==========
    with tab5:
        st.header("🧠 LeTalk: Chat with LeBron AI")
        st.info("Coming soon: Ask the King anything—stats, legacy, life advice, and more.")
        st.markdown("""
            Imagine chatting with a LeBron-powered AI.
            - 🤖 Simulate convo with the GOAT
            - 💡 Ask about his career, mindset, or off-court greatness
            - 🧬 Built using LLMs and custom LeBron data
        """)

    from datetime import datetime
    from streamlit_autorefresh import st_autorefresh

    # Auto-refresh every 10 seconds (10,000 milliseconds)
    import time



    # # ========== TAB 6 ========== 
    from tab6_chat import render_tab6
    render_tab6(tab6)
    # with tab6:
    #     import csv
    #     from datetime import datetime
    #     from streamlit_autorefresh import st_autorefresh

    #     st.header("💬 LeDiscussion: Group Chat for LeBron Fans")

    #     # Adaptive styling for light/dark mode
    #     st.markdown("""
    #     <style>
    #     .chat-bubble {
    #         background-color: #ffffff;
    #         color: #111111;
    #         padding: 0.6rem 1rem;
    #         margin-bottom: 0.6rem;
    #         border-radius: 10px;
    #         box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    #         font-size: 0.95rem;
    #         line-height: 1.4;
    #     }
    #     .chat-user {
    #         font-weight: 600;
    #         color: #4b0082;
    #     }
    #     .chat-timestamp {
    #         font-size: 0.75rem;
    #         color: #666666;
    #         float: right;
    #         margin-left: 10px;
    #     }
    #     @media (prefers-color-scheme: dark) {
    #         .chat-bubble {
    #             background-color: #1f1f1f;
    #             color: #f0f0f0;
    #             box-shadow: 0 1px 4px rgba(255,255,255,0.05);
    #         }
    #         .chat-user {
    #             color: #d4aaff;
    #         }
    #         .chat-timestamp {
    #             color: #aaa;
    #         }
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)

    #     st_autorefresh(interval=10000, key="chat_autorefresh")

    #     CHAT_FILE = "chat_history.csv"
    #     if not os.path.exists(CHAT_FILE):
    #         with open(CHAT_FILE, "w", newline="") as f:
    #             writer = csv.DictWriter(f, fieldnames=["user", "msg", "timestamp"])
    #             writer.writeheader()

    #     # Ensure input session state exists
    #     if "chat_input_temp" not in st.session_state:
    #         st.session_state.chat_input_temp = ""

    #     def send_message():
    #         msg = st.session_state.chat_input_temp.strip()
    #         if msg:
    #             now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             with open(CHAT_FILE, "a", newline="") as f:
    #                 writer = csv.DictWriter(f, fieldnames=["user", "msg", "timestamp"])
    #                 writer.writerow({
    #                     "user": st.session_state.current_user,
    #                     "msg": msg,
    #                     "timestamp": now
    #                 })
    #             # ✅ Reset field
    #             st.session_state.chat_input_temp = ""

    #     # ✅ Use value= to force refresh
    #     st.text_input("Your Message", key="chat_input_temp", max_chars=200, value=st.session_state.chat_input_temp)
    #     st.button("Send", on_click=send_message)

    #     with open(CHAT_FILE, "r") as f:
    #         chat_history = list(csv.DictReader(f))

    #     import re
    #     from html import escape

    #     def parse_message(msg):
    #         # Convert URLs to clickable links
    #         msg = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', msg)
    #         # Escape other content (so emojis show but script tags don’t execute)
    #         return escape(msg).replace("\n", "<br>")

    #     # Reaction counts (basic in-memory demo — reset on rerun)
    #     if "reactions" not in st.session_state:
    #         st.session_state.reactions = {}

    #     def add_reaction(msg_id, emoji):
    #         if msg_id not in st.session_state.reactions:
    #             st.session_state.reactions[msg_id] = {}
    #         st.session_state.reactions[msg_id][emoji] = st.session_state.reactions[msg_id].get(emoji, 0) + 1

    #     st.subheader("📜 Chat History")

    #     # Create colors for different users
    #     def get_user_color(username):
    #         import hashlib
    #         hex_color = hashlib.md5(username.encode()).hexdigest()[:6]
    #         return f"#{hex_color}"

    #     for i, chat in enumerate(reversed(chat_history[-50:])):
    #         parsed_msg = parse_message(chat['msg'])
    #         user_color = get_user_color(chat['user'])
    #         timestamp = chat['timestamp']
    #         msg_id = f"{chat['user']}_{chat['timestamp']}_{i}"

    #         st.markdown(f"""
    #         <div class="chat-bubble" title="Sent at {timestamp}">
    #             <span class="chat-user" style="color: {user_color}">{chat['user']}</span>
    #             <span class="chat-timestamp">{timestamp}</span><br>
    #             {parsed_msg}
    #         </div>
    #         """, unsafe_allow_html=True)

    #         # 🔥 Reaction buttons
    #         col1, col2, col3 = st.columns(3)
    #         with col1:
    #             if st.button(f"👍 {st.session_state.reactions.get(msg_id, {}).get('👍', 0)}", key=f"{msg_id}_like"):
    #                 add_reaction(msg_id, "👍")
    #         with col2:
    #             if st.button(f"🔥 {st.session_state.reactions.get(msg_id, {}).get('🔥', 0)}", key=f"{msg_id}_fire"):
    #                 add_reaction(msg_id, "🔥")
    #         with col3:
    #             if st.button(f"😂 {st.session_state.reactions.get(msg_id, {}).get('😂', 0)}", key=f"{msg_id}_lol"):
    #                 add_reaction(msg_id, "😂")


