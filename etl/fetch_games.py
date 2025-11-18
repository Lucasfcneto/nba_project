import pandas as pd
from nba_api.stats.endpoints import leaguegamelog
from datetime import datetime

def fetch_games(season="2024-25", season_type="Regular Season"):
    """
    Fetches all NBA games for a specific season.

    Returns:
        DataFrame with GAME_ID, TEAM_ID, DATE, MATCHUP, RESULT, etc.
    """

    print(f"[INFO] Fetching games for {season}...")

    raw = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star=season_type
    ).get_data_frames()[0]

    raw["GAME_DATE"] = pd.to_datetime(raw["GAME_DATE"])

    return raw
