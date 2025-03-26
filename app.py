import streamlit as st
from auth import init_db, authenticate, save_user, hash_password
from tabs import tab1_resume, tab3_bronify, tab4_defend, tab5_letalk, tab6_discussion
from lebron_next_game import render_tab2

# --- App Config ---
st.set_page_config(page_title="LeApp | The LeBron Experience", layout="wide")
import base64

favicon_path = "assets/lebron_fav.png"

def set_custom_favicon(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
        <head>
            <link rel="icon" type="image/png" href="data:image/png;base64,{encoded}">
        </head>
        """, unsafe_allow_html=True)

set_custom_favicon(favicon_path)

init_db()

# --- Session State Setup ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- Login / Sign Up ---
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
    else:
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

# ======================
# If Authenticated, Show App
# ======================
st.sidebar.success(f"👑 Logged in as {st.session_state.current_user}")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.current_user = ""
    st.rerun()

# Inject styling
st.markdown(open("ui/theme.css").read(), unsafe_allow_html=True)

# Title & image banner
st.title("👑 LeApp: The LeBron James Experience 👑")
st.markdown(open("ui/lebron_header.html").read(), unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 LeResume", 
    "🕒 LeLive", 
    "🎤 Bronify", 
    "🛡️ LeDefend", 
    "🧠 LeTalk", 
    "💬 LeDiscussion"
])

# Tab routers
tab1_resume.render(tab1)
render_tab2(tab2)
tab3_bronify.render(tab3)
tab4_defend.render(tab4)
tab5_letalk.render(tab5)
tab6_discussion.render(tab6)
