import json
import sys
import time
from pathlib import Path

import requests

from get_match_ids import API_KEY, BASE_URL, PUUID, get_match_ids

RAW_DIR = Path("data/raw/matches")
PAUSE_SECONDS = 1.3  # ~92 peticiones cada 2 minutos, debajo del límite de 100


def get_match_detail(match_id, max_retries=3):
    """Devuelve el JSON de una partida, o None si no se pudo obtener."""
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": API_KEY}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=(5, 15))
        except requests.exceptions.RequestException as e:
            wait = 2 ** (attempt + 1)
            print(f"Error de red en {match_id} (intento {attempt + 1}): {e}. Reintentando en {wait}s...")
            time.sleep(wait)
            continue

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 10))
            print(f"Límite de peticiones alcanzado. Esperando {wait}s...")
            time.sleep(wait)
            continue

        print(f"Error {response.status_code} en {match_id}: {response.text}")
        return None

    return None


def main():
    def get_all_match_ids(puuid, total=100, page_size=100):
    #Pide IDs por páginas hasta juntar `total` o hasta que Riot no tenga más.
        ids = []
        while len(ids) < total:
            page = get_match_ids(puuid, count=min(page_size, total - len(ids)), start=len(ids))
            if not page:
                break
            ids.extend(page)
        return ids

    if not API_KEY or not PUUID:
        sys.exit("Faltan RIOT_API_KEY o PUUID en el .env")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    match_ids = get_all_match_ids(PUUID, total=100)
    print(f"{len(match_ids)} partidas por revisar")

    for match_id in match_ids:
        path = RAW_DIR / f"{match_id}.json"

        if path.exists():
            print(f"{match_id}: ya existe, se omite")
            continue

        detail = get_match_detail(match_id)
        if detail is None:
            continue

        path.write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        print(f"{match_id}: guardada")
        time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    main()