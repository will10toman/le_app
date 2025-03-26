import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
from datetime import datetime
import pytz
from time import sleep

def get_lebron_next_game():
    try:
        url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
        response = requests.get(url)
        data = response.json()

        games = data["leagueSchedule"]["gameDates"]

        for game_day in games:
            for game in game_day["games"]:
                if game["homeTeam"]["teamTricode"] == "LAL" or game["awayTeam"]["teamTricode"] == "LAL":
                    game_utc = datetime.strptime(game["gameDateTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
                    if game_utc <= datetime.utcnow():
                        continue

                    eastern = pytz.timezone("US/Eastern")
                    game_local = game_utc.replace(tzinfo=pytz.utc).astimezone(eastern)
                    formatted_time = game_local.strftime("%A, %B %d at %I:%M %p %Z")

                    opponent = game["awayTeam"]["teamTricode"] if game["homeTeam"]["teamTricode"] == "LAL" else game["homeTeam"]["teamTricode"]
                    location = "Home" if game["homeTeam"]["teamTricode"] == "LAL" else "Away"

                    return {
                        "formatted_time": formatted_time,
                        "opponent": opponent,
                        "location": location,
                        "datetime": game_local
                    }

        return None

    except Exception as e:
        return {"error": str(e)}

def render_tab2(tab2):
    with tab2:
        st_autorefresh(interval=60000, key="lebron_next_game_refresh")
        st.markdown("## 🕒 The Countdown to Greatness Begins")

        game = get_lebron_next_game()

        if game is None:
            st.warning("🚫 No upcoming Lakers games found.")
            return

        if "error" in game:
            st.error(f"⚠️ {game['error']}")
            return

        # Hype Text
        st.markdown(f"""
        <div style='font-size:1.2rem; background-color:#111; padding:1rem; border-radius:10px; color:white; text-align:center'>
            <strong>🔥 The King is gearing up.</strong><br>
            <span style='font-size:1.1rem;'>LeBron faces off against <span style='color:gold;'>{game['opponent']}</span> {game['location']} on</span><br>
            <span style='font-size:1.4rem; color:lightgreen'><b>{game['formatted_time']}</b></span>
        </div>
        """, unsafe_allow_html=True)

        # Countdown
        time_left = game["datetime"] - datetime.now(pytz.timezone("US/Eastern"))
        days, seconds = time_left.days, time_left.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        st.markdown("### ⏳ Countdown to Tip-Off")
        st.metric("Days", days)
        st.metric("Hours", hours)
        st.metric("Minutes", minutes)

        # LeBron image
        st.image("https://i.imgur.com/wHjHQMZ.jpeg", width=300, caption="The Calm Before the Storm", use_column_width="always")

        st.caption("👑 Auto-refreshing every 60 seconds to keep hype levels maxed.")

