import streamlit as st

# === Inject Dark/Light Theme Styles ===
def load_theme():
    st.markdown("""
    <style>
    /* Light mode defaults */
    .stApp {
        background-color: #f9f9f9;
        color: #111;
    }
    h1, h2, h3, h4, p, span, label {
        color: #222;
    }
    .stMarkdown > div {
        background-color: #fff;
        color: #111;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 1px 8px rgba(0,0,0,0.05);
    }
    input, textarea {
        background-color: #f2f2f2;
        color: #111;
    }

    /* Dark mode overrides */
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
            color: #fff;
        }
        section[data-testid="stSidebar"] {
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# === LeBron Header Block (Responsive Image) ===
def render_header_image():
    st.markdown("""
    <style>
    .lebron-container {
        position: relative;
        width: 100%;
    }
    .lebron-img-desktop {
        position: absolute;
        top: 0.5rem;
        right: 0;
        width: 240px;
        z-index: 10;
    }
    .lebron-img-mobile {
        display: none;
        margin-top: 1rem;
        text-align: center;
    }
    .block-container h1 {
        margin-bottom: 0.2rem;
    }
    .block-container {
        padding-top: 1rem !important;
    }

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
        <img src="https://i.imgur.com/NRHdCTs.png" class="lebron-img-desktop">
    </div>

    <div class="lebron-img-mobile">
        <img src="https://i.imgur.com/NRHdCTs.png" width="160">
    </div>
    """, unsafe_allow_html=True)
