import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
PUUID = os.getenv("PUUID")

BASE_URL = "https://americas.api.riotgames.com"


def get_match_ids(puuid, count=20):
    """Devuelve la lista de IDs de las últimas `count` partidas del jugador."""
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": API_KEY}
    params = {"count": count}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=(5, 15))
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
        return []

    if response.status_code == 200:
        return response.json()

    print(f"Error {response.status_code}: {response.text}")
    return []


if __name__ == "__main__":
    if not API_KEY or not PUUID:
        raise SystemExit("Faltan RIOT_API_KEY o PUUID en el .env")

    ids = get_match_ids(PUUID)
    print(f"Partidas encontradas: {len(ids)}")
    for match_id in ids:
        print(match_id)