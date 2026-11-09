import psycopg
from dotenv import load_dotenv

from build_dataframe import load_matches

load_dotenv()

COLUMN_MAP = {
    "match_id": "match_id",
    "puuid": "puuid",
    "riotIdGameName": "riot_id_game_name",
    "championName": "champion_name",
    "teamPosition": "team_position",
    "win": "win",
    "kills": "kills",
    "deaths": "deaths",
    "assists": "assists",
    "goldEarned": "gold_earned",
    "totalDamageDealtToChampions": "total_damage_dealt_to_champions",
    "visionScore": "vision_score",
    "totalMinionsKilled": "total_minions_killed",
    "neutralMinionsKilled": "neutral_minions_killed",
    "gameEndedInEarlySurrender": "game_ended_in_early_surrender",
    "queue_id": "queue_id",
    "game_duration_s": "game_duration_s",
    "game_start": "game_start",
}

DDL = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.match_participants (
    match_id text NOT NULL,
    puuid text NOT NULL,
    riot_id_game_name text,
    champion_name text,
    team_position text,
    win boolean,
    kills integer,
    deaths integer,
    assists integer,
    gold_earned integer,
    total_damage_dealt_to_champions integer,
    vision_score integer,
    total_minions_killed integer,
    neutral_minions_killed integer,
    game_ended_in_early_surrender boolean,
    queue_id integer,
    game_duration_s integer,
    game_start timestamp,
    PRIMARY KEY (match_id, puuid)
);
"""


def main():
    df = load_matches()
    df = df[list(COLUMN_MAP)].rename(columns=COLUMN_MAP)

    # Pandas usa NaN para vacíos; Postgres espera NULL (None en Python)
    rows = list(df.astype(object).where(df.notna(), None).itertuples(index=False, name=None))

    columns = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_sql = (
        f"INSERT INTO raw.match_participants ({columns}) "
        f"VALUES ({placeholders}) ON CONFLICT (match_id, puuid) DO NOTHING"
    )

    with psycopg.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
            cur.executemany(insert_sql, rows)
            print(f"{len(rows)} filas leídas, {cur.rowcount} insertadas")


if __name__ == "__main__":
    main()