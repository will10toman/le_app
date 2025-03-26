import streamlit as st

def render(tab):
    with tab:
        st.header("🎤 Bronify: Parody Songs About the King")
        st.markdown("""
        - 🎶 *"LeMVP Baby"*
        - 🎶 *"Can't Stop LeBron"*
        - 🎶 *"King of the Court"*
        """)