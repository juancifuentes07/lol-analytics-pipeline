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
# print(
#     mine.groupby("championName")
#     .agg(
#         partidas=("win", "size"),
#         winrate=("win", "mean"),
#         kills_prom=("kills", "mean"),
#     )
#     .sort_values("partidas", ascending=False)
#     .round(2)
# )

# # 4. Colas 
# print(mine.groupby("queue_id").agg(
#     partidas=("win", "size"),
#     winrate=("win", "mean"),
# ))

# 5. KDA 
# mine["KDA"] = (mine["kills"] + mine["assists"]) / mine["deaths"].replace(0, 1)
# print(mine[["match_id", "championName", "kills", "deaths", "assists", "KDA"]])

# # 6. Duración de partidas
# mine["game_duration_min"] = (mine["game_duration_s"] / 60).round(2)
# print(mine[["match_id", "game_duration_min"]])

# Guardo los Champs en una variable para poder usarla en el notebook
champs = mine.groupby("championName").agg(
    partidas=("win", "size"),
    winrate=("win", "mean"),
    kills_prom=("kills", "mean"),
)

# Filtramos los campeones con al menos 5 partidas y ordenamos por winrate
champs_5 = (
    champs[champs["partidas"] >= 5]
    .sort_values("winrate", ascending=False)
    .round(2)
)

print(champs_5)

# Que posición de equipo es la que más jugamos y cuál es nuestro winrate en cada una
by_role = (
    mine.groupby("teamPosition").agg(
        partidas=("win", "size"),
        winrate=("win", "mean"),
    ).round(2)
)
print(by_role)

# En que rol jugamos con Jinx y cuántas veces
print(mine[mine["championName"] == "Jinx"]["teamPosition"].value_counts())

print(mine["game_start"].min(), mine["game_start"].max()) # Rango de fechas de las partidas

# Agrupamos por mes y calculamos el winrate de cada mes
mine["month"] = mine["game_start"].dt.to_period("M")
by_month = mine.groupby("month").agg(
    partidas=("win", "size"),
    winrate=("win", "mean"),
).round(2)
print(by_month)

# Cuándo jugué con Jinx?
print(mine[mine["championName"] == "Jinx"].groupby("month").size())

others = df_clean[df_clean["puuid"] != PUUID]

print(mine[["visionScore", "goldEarned"]].mean())
print(others[["visionScore", "goldEarned"]].mean())

print(mine.groupby("teamPosition")[["visionScore", "goldEarned"]].mean().round(0))
print(others.groupby("teamPosition")[["visionScore", "goldEarned"]].mean().round(0))

no_jinx = mine[mine["championName"] != "Jinx"]
print(len(no_jinx), no_jinx["win"].mean())

nov = mine[mine["game_start"] >= "2026-11-01"]
print(nov.groupby(["teamPosition", "championName"]).agg(
    partidas=("win", "size"),
    victorias=("win", "sum"),
))