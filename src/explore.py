import pandas as pd

from build_dataframe import load_matches
from get_match_ids import PUUID  

pd.set_option("display.max_columns", None)  # que print muestre todas las columnas

df = load_matches()
MIN_DURATION_S = 600  # partidas de menos de 10 min no son analizables (remakes, desconexiones)

df_clean = df[~df["gameEndedInEarlySurrender"] & (df["game_duration_s"] >= MIN_DURATION_S)]
print(df_clean.shape)

# 1. Tus filas: es un WHERE puuid = '...'
mine = df_clean[df_clean["puuid"] == PUUID].copy()
print(len(mine))  # debería ser 20, una por partida

# 2. Tu winrate: win es True/False, y el promedio de una booleana es la proporción de True
print(mine["win"].mean())

# 3. Campeones
print(
    mine.groupby("championName")
    .agg(
        partidas=("win", "size"),
        winrate=("win", "mean"),
        kills_prom=("kills", "mean"),
    )
    .sort_values("partidas", ascending=False)
    .round(2)
)

# 4. Colas 
print(mine.groupby("queue_id").agg(
    partidas=("win", "size"),
    winrate=("win", "mean"),
))

# 5. KDA 
mine["KDA"] = (mine["kills"] + mine["assists"]) / mine["deaths"].replace(0, 1)
print(mine[["match_id", "championName", "kills", "deaths", "assists", "KDA"]])

# 6. Duración de partidas
mine["game_duration_min"] = (mine["game_duration_s"] / 60).round(2)
print(mine[["match_id", "game_duration_min"]])
