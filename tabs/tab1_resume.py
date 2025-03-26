import streamlit as st
import matplotlib.pyplot as plt
from logic.logic import fetch_lebron_game_logs, calculate_averages, get_top_games
import pandas as pd

def render(tab):
    with tab:
        st.header("📈 LeResume: Career Stats (Live from NBA API)")

        # Get and prep data
        career_df = fetch_lebron_game_logs()

        # Handle empty or invalid DataFrame
        if career_df is None or career_df.empty:
            st.error("⚠️ Failed to load LeBron's data. Please try again later.")
            return

        if "GAME_DATE" not in career_df.columns:
            st.error("⚠️ NBA API returned data without GAME_DATE.")
            st.dataframe(career_df)  # Help debug
            return

        # Data preprocessing
        career_df["GAME_DATE"] = pd.to_datetime(career_df["GAME_DATE"], errors="coerce")
        career_df = career_df.dropna(subset=["GAME_DATE"])
        career_df = career_df.sort_values("GAME_DATE")

        # Season selection
        seasons = sorted(career_df["Season"].unique(), reverse=True)
        all_seasons = ["Career"] + seasons
        selected_season = st.selectbox("Select a season", all_seasons)

        display_df = career_df if selected_season == "Career" else career_df[career_df["Season"] == selected_season]
        averages = calculate_averages(display_df)

        st.subheader(f"{selected_season} Averages")
        st.write(averages)

        # Chart
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

        # GOAT Stuff
        st.subheader("🔊 Why LeBron Is the Greatest")
        st.markdown("""
        - 🏆 **4× NBA Champion**
        - 👑 **All-Time Leading Scorer**
        - 🧠 **First with 30K points, 10K boards, 10K dimes**
        - 🗓️ **20+ Seasons of Greatness**
        - 🏀 **Most All-NBA Selections**
        - 💪 **19 straight 25+ PPG seasons**
        """)

        # Top Games
        st.subheader("🔥 Top 10 Scoring Games")
        top_games = get_top_games(career_df)
        st.dataframe(top_games)
