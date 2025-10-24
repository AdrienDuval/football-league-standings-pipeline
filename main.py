import os
import json
import requests
import pandas as pd
from mysql import connector
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
API_SECRET = os.getenv("API_SECRET")
SEASON = 2025
LEAGUE_ID = 5
print(API_KEY)

# url = f"https://livescore-api.com/api-client/leagues/table.json?competition_id={LEAGUE_ID}&key={API_KEY}&secret={API_SECRET}"
url = f"https://livescore-api.com/api-client/leagues/table.json?key={API_KEY}&secret={API_SECRET}&competition_id={LEAGUE_ID}&include_form=1"
headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}

# https://livescore-api.com/api-client/leagues/table.json?competition_id=2&key=jAgOFcvg5LCvM1zm&secret=vTsEc5W4cHdOTPCdqS165wnaiZG41frw

querystring = {"league": LEAGUE_ID, "season": SEASON}
print(querystring)


response = requests.get(url=url)

payload = response.json()
payload

formatted_response = json.dumps(payload, indent=4)

print(formatted_response)

standings_list = payload["data"]["table"]
formatted_standings = json.dumps(standings_list, indent=4)
print(formatted_standings)

arseille_points = standings_list[0]["points"]
print(arseille_points)


rows = []
column_names = [
    "season",
    "position",
    "team__id",
    "team",
    "played",
    "won",
    "draw",
    "lost",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "form",
]
for club in standings_list:
    season = 2025
    position = club["rank"]
    team_id = club["team_id"]
    team = club["name"]
    played = club["matches"]
    won = club["won"]
    draw = club["drawn"]
    lost = club["lost"]
    goals_for = club["goals_scored"]
    goals_against = club["goals_conceded"]
    goal_diff = club["goal_diff"]
    points = club["points"]
    form = "LLDDWW"

    tuple_of_club_records = (
        season,
        position,
        team_id,
        team,
        played,
        won,
        draw,
        lost,
        goals_for,
        goals_against,
        goal_diff,
        points,
        form,
    )
    rows.append(tuple_of_club_records)


df = pd.DataFrame(rows, columns=column_names)
df.head(18)

df.info()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
print(MYSQL_USER)


import psycopg2

# server_conn = connector.connect(
#     host = MYSQL_HOST,
#     port = MYSQL_PORT,
#     user = MYSQL_USER,
#     password = MYSQL_PASSWORD,
#     # connection_timeout = 10,
#     autocommit = False,
#     raise_on_warning=True
# )

try:
    server_conn = psycopg2.connect(
        database=MYSQL_DATABASE,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )
    server_conn
    # Open a cursor to perform database operations
    cur = server_conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS standings_ligue_1(
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
    print("Connection to PostgresSQL succesfull!")

    sql_table = "standings_ligue_1"
    cur.execute(
        """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = %s
    )
    """,
        (sql_table,),
    )

    exists = cur.fetchone()[0]

    if not exists:
        raise SystemExit(
            f"❌ This table '{sql_table}' is NOT found... please create it."
        )
    else:
        print(f"✅ This table '{sql_table}' exists!")

except Exception as e:
    print("connection failed!", e)


# finally:
#     if server_conn:
#         # make the changes to the database persistent
#         server_conn.commit()
#         # close cursor and communication with the database
#         cur.close()
#         server_conn.close()

table_cols = [
    "season",
    "position",
    "team__id",
    "team",
    "played",
    "won",
    "draw",
    "lost",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "form",
]

standing_df = df[table_cols]

standings_records_tuples = standing_df.itertuples(index=False, name=None)

list_of_standings_records_tuples = list(standings_records_tuples)

UPSERT_SQL = f"""
INSERT INTO {sql_table}
(season, position, team_id, team, played, won, draw, lost, goals_for, goals_against, goal_diff, points, form)
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

no_of_rows_uploaded_to_mysql = len(list_of_standings_records_tuples)

try:
    cur.executemany(UPSERT_SQL, list_of_standings_records_tuples)
    server_conn.commit()
    print(f"[SUCCESS] - Upsert attempted for {no_of_rows_uploaded_to_mysql} rows!")

except Exception as e:
    server_conn.rollback()
    print(f"[ERROR] - ROlled back due to this...: {e}")
finally:
    cur.close()
    server_conn.close()
    print("All database connection was closed. \n\nClean up completed.")
