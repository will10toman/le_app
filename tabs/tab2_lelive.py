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

def render(tab2):
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

        st.markdown(f"""
        <div style='
            padding: 1.2rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #3a0ca3, #7209b7);
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        '>
            <div style='font-size:1.3rem; font-weight: bold;'>🔥 The King is gearing up.</div>
            <div style='font-size:1.1rem; margin-top:0.5rem;'>LeBron faces off against <span style='color:#fdd835'>{game['opponent']}</span> <b>{game['location']}</b> on</div>
            <div style='font-size:1.5rem; font-weight:bold; margin-top:0.3rem;'>{game['formatted_time']}</div>
        </div>
        """, unsafe_allow_html=True)


        # Countdown logic
        now = datetime.now(pytz.timezone("US/Eastern"))
        game_time = game["datetime"]
        time_left = game_time - now
        total_seconds = (game_time - now).total_seconds()

        # Metrics
        days, seconds = time_left.days, time_left.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        st.markdown("### ⏳ Countdown to Tip-Off")
        st.metric("Days", days)
        st.metric("Hours", hours)
        st.metric("Minutes", minutes)

        # Progress bar visualization
        total_until_game = (game_time - now).total_seconds()
        total_window = 7 * 24 * 3600  # Assume hype window is 7 days before tipoff
        percent_complete = 100 - min(100, max(0, (total_until_game / total_window) * 100))

        st.markdown("#### 🔥 Hype Level")
        st.progress(percent_complete / 100)

        # LeBron image
        st.image("https://i.imgur.com/16Kjx2u.jpeg", caption="The Calm Before the Storm", use_container_width=True)


        st.caption("👑 Auto-refreshing every 60 seconds to keep hype levels maxed.")

