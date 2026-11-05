import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw/matches")

PLAYER_COLUMNS = [
    "puuid", "riotIdGameName", "championName", "teamPosition", "win",
    "kills", "deaths", "assists", "goldEarned",
    "totalDamageDealtToChampions", "visionScore",
    "totalMinionsKilled", "neutralMinionsKilled", "gameEndedInEarlySurrender"
]


def load_matches(raw_dir=RAW_DIR):
    """Lee todos los JSON y devuelve un DataFrame: una fila por jugador por partida."""
    rows = []

    for path in raw_dir.glob("*.json"):
        match = json.loads(path.read_text(encoding="utf-8"))
        info = match["info"]

        for player in info["participants"]:
            row = {col: player.get(col) for col in PLAYER_COLUMNS}
            row["match_id"] = match["metadata"]["matchId"]
            row["queue_id"] = info["queueId"]
            row["game_duration_s"] = info["gameDuration"]
            row["game_start"] = pd.to_datetime(info["gameCreation"], unit="ms")
            rows.append(row)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load_matches()
    print(df.shape)
    print(df.head())
    print(df.dtypes)