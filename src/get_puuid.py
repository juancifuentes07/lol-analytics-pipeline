
import os
import requests

from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("RIOT_API_KEY")

GAME_NAME = "Juanpa ツ"
TAG_LINE = "deuS"

# Validate API Key
if not API_KEY:
    raise SystemExit("Error: RIOT_API_KEY not found in environment variables.")

# Build API URL
url = (
    "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    f"{quote(GAME_NAME, safe='')}/{quote(TAG_LINE, safe='')}"
)

# Request headers
headers = {
    "X-Riot-Token": API_KEY
}

# API Request
try:
    response = requests.get(
        url,
        headers=headers,
        timeout=(5, 15)
    )

    if response.status_code == 200:
        data = response.json()
        print("Account information:")
        print(data)

    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.Timeout:
    print("Error: The request exceeded the timeout limit.")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
