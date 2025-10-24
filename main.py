import os
import json
import requests
import pandas as pd
from mysql import connector
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_batch

# Load environment variables
load_dotenv()

# PostgreSQL Config
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# API Config
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Leagues
LEAGUE_INFO = [
    {"league_id": 5, "league_name": "Ligue 1", "country": "France"},
    {"league_id": 2, "league_name": "Premier League", "country": "England"},
    {"league_id": 3, "league_name": "LaLiga Santander", "country": "Spain"},
]

LEAGUE_INFO[0]["league_id"]


# Connect to PostgresSql
def get_db_connection():
    return psycopg2.connect(
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
    )


# fetch league data
def fetch_league_standings(league_id, league_name):
    url = (
        f"https://livescore-api.com/api-client/leagues/table.json?"
        f"key={API_KEY}&secret={API_SECRET}&competition_id={league_id}&include_form=1"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            print(f"API returned error for {league_name}: {data}")
            return None
        print(f"{league_name}: fetched {len(data['data']['table'])} teams")
        # print(data["data"]["table"])
        return data["data"]["table"]

    except Exception as e:
        print(f"Error fetching {league_name}: {e}")
        return None


# Create league table if not exists


def create_table_if_not_exists(cur, table_name):
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
        id SERIAL,
        season INT NOT NULL,
        position INT NOT NULL,
        team_id INT NOT NULL,
        team VARCHAR(100) NOT NULL,
        played INT NOT NULL,
        won INT NOT NULL,
        draw INT NOT NULL,
        lost INT NOT NULL,
        goals_for INT NOT NULL,
        goals_against INT NOT NULL,
        goal_diff INT NOT NULL,
        points INT NOT NULL,
        form VARCHAR(6) NOT NULL,
        PRIMARY KEY (season,team_id),
        UNIQUE(season, position)
        );

        """
    )
    print(f"Table '{table_name}' ready.")


# Upsert Data
def upsert_standings(cur, table_name, records):
    UPSERT_SQL = f"""
        INSERT INTO {table_name}
        (season, position, team_id, team, played, won, draw, lost,
         goals_for, goals_against, goal_diff, points, form)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (season, team_id) DO UPDATE SET
            position = EXCLUDED.position,
            team = EXCLUDED.team,
            played = EXCLUDED.played,
            won = EXCLUDED.won,
            draw = EXCLUDED.draw,
            lost = EXCLUDED.lost,
            goals_for = EXCLUDED.goals_for,
            goals_against = EXCLUDED.goals_against,
            goal_diff = EXCLUDED.goal_diff,
            points = EXCLUDED.points,
            form = EXCLUDED.form;
    """
    execute_batch(cur, UPSERT_SQL, records)
    print(f"✅ Upserted {len(records)} rows into '{table_name}'")


def main():
    with get_db_connection() as conn:
        cur = conn.cursor()

        for league in LEAGUE_INFO:
            league_id = league["league_id"]
            league_name = league["league_name"]
            table_name = f"standings_{league_name.replace(' ', '_').lower()}"

            standings = fetch_league_standings(league_id, league_name)
            if not standings:
                continue

            create_table_if_not_exists(cur, table_name)

            # Prepare records
            records = [
                (
                    2025,
                    int(team["rank"]),
                    int(team["team_id"]),
                    team["name"],
                    int(team["matches"]),
                    int(team["won"]),
                    int(team["drawn"]),
                    int(team["lost"]),
                    int(team["goals_scored"]),
                    int(team["goals_conceded"]),
                    int(team["goal_diff"]),
                    int(team["points"]),
                    "".join(team.get("form", [])) if team.get("form") else "WWDDLL",
                )
                for team in standings
            ]
            # Upsert into DB
            upsert_standings(cur, table_name, records)
            conn.commit()
    cur.close()
    print("Connection closed")
    print("All leagues processed successfully")


# -----------------------------------
# Entry point
# -----------------------------------
if __name__ == "__main__":
    main()
