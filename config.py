"""
Configuration file for Football League Standings Dashboard
Contains league IDs, database settings, and API configurations
"""

# League Configuration
LEAGUES = {
    "premier_league": {
        "id": 2,
        "name": "Premier League",
        "country": "England",
        "table_name": "standings_premier_league"
    },
    "ligue_1": {
        "id": 5,
        "name": "Ligue 1",
        "country": "France", 
        "table_name": "standings_ligue_1"
    }
}

# API Configuration
API_BASE_URL = "https://livescore-api.com/api-client/leagues/table.json"
API_TIMEOUT = 30

# Database Configuration
DB_CONNECTION_TIMEOUT = 10
DB_MAX_RETRIES = 3

# Data Processing Configuration
DEFAULT_SEASON = 2025
BATCH_SIZE = 100

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
