import psycopg
from dotenv import load_dotenv

load_dotenv()

with psycopg.connect() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version(), current_database()")
        print(cur.fetchone())