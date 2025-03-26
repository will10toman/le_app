import pandas as pd
import requests

# === Fetch LeBron Game Logs from NBA API ===
def fetch_lebron_game_logs(player_id="2544", seasons=None):
    if seasons is None:
        seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(2003, 2025)]

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nba.com"
    }

    all_data = []
    for season in seasons:
        params = {
            "PlayerID": player_id,
            "Season": season,
            "SeasonType": "Regular Season"
        }
        try:
            res = requests.get(
                "https://stats.nba.com/stats/playergamelog",
                params=params,
                headers=headers,
                timeout=10
            )
            data = res.json()
            columns = data["resultSets"][0]["headers"]
            rows = data["resultSets"][0]["rowSet"]
            df = pd.DataFrame(rows, columns=columns)
            df["Season"] = season
            all_data.append(df)
        except Exception as e:
            print(f"Failed for season {season}: {e}")
            continue

    return pd.concat(all_data) if all_data else pd.DataFrame()

# === Calculate Averages ===
def calculate_averages(df):
    return {
        "Points Per Game": round(df["PTS"].mean(), 1),
        "Assists Per Game": round(df["AST"].mean(), 1),
        "Rebounds Per Game": round(df["REB"].mean(), 1),
    }

# === Get Top Scoring Games ===
def get_top_games(df, top_n=10):
    return df.sort_values("PTS", ascending=False).head(top_n)[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST"]].reset_index(drop=True)
