import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
from datetime import datetime
import pytz

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

                    return f"LeBron's next game is vs {opponent} on {formatted_time} ({location})"

        return "No upcoming Lakers games found."

    except Exception as e:
        return f"Error: {e}"

def render_tab2(tab2):
    with tab2:
        st_autorefresh(interval=60000, key="lebron_next_game_refresh")
        st.subheader("🗓 LeBron's Next Game")
        st.info(get_lebron_next_game())
