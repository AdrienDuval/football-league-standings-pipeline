# Football League Standings Dashboard

A data engineering project that automatically fetches and displays real-time football league standings for bars and public venues, eliminating the need for individual phone usage and reducing WiFi congestion.

## 🎯 Project Overview

This project addresses a common problem in sports bars and public venues: multiple people simultaneously checking league standings on their phones, which overloads the WiFi network and creates a poor user experience. Instead, this solution provides a centralized, real-time display of league standings that can be shown on a single screen or display.

## 🚀 Learning Objectives

As a **Data Engineering Portfolio Project**, this demonstrates:

- **API Integration**: Fetching real-time data from external sports APIs
- **Data Processing**: Transforming raw API responses into structured data
- **Database Management**: PostgreSQL operations with upsert functionality
- **Data Pipeline**: End-to-end ETL process from API to database
- **Error Handling**: Robust error management and connection handling
- **Environment Management**: Secure credential handling with environment variables
- **Data Validation**: Ensuring data integrity and consistency

## 🏆 Supported Leagues

Currently supports:
- **Premier League** (England) - League ID: 2
- **Ligue 1** (France) - League ID: 5

*Easily extensible to support additional leagues by modifying the league ID configuration.*

## 🛠️ Technical Stack

- **Python 3.x**
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP API calls
- **PostgreSQL** - Database storage
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variable management
- **Jupyter Notebooks** - Data exploration and testing

## 📊 Data Schema

The project stores comprehensive team statistics:

```sql
CREATE TABLE standings_ligue_1 (
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
    PRIMARY KEY (season, team_id),
    UNIQUE(season, position)
);
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7+
- PostgreSQL database
- LiveScore API credentials

### 1. Clone the Repository
```bash
git clone <repository-url>
cd PL-Standings-2020-25
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure your credentials:
```bash
cp env.example .env
```

Edit the `.env` file with your actual credentials:
```env
API_KEY=your_livescore_api_key
API_HOST=your_api_host
API_SECRET=your_api_secret
MYSQL_HOST=your_postgres_host
MYSQL_PORT=5432
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database_name
```

### 5. Database Setup
Ensure your PostgreSQL database is running and accessible with the credentials specified in your `.env` file.

## 📁 Project Structure

```
PL-Standings-2020-25/
├── main.py                 # Main data pipeline script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup script
├── env.example          # Environment variables template
├── .env                 # Your environment variables (create from env.example)
├── .gitignore           # Git ignore rules
├── Premier_league.ipynb # Premier League data analysis
├── ligue-1.ipynb        # Ligue 1 data analysis
└── README.md            # This file
```

## 🚀 Usage

### Running the Data Pipeline
```bash
python main.py
```

### Jupyter Notebooks
For data exploration and testing:
- `Premier_league.ipynb` - Premier League data analysis
- `ligue-1.ipynb` - Ligue 1 data analysis

## 📈 Features

- **Real-time Data**: Fetches current league standings from LiveScore API
- **Upsert Operations**: Updates existing records or inserts new ones
- **Data Validation**: Ensures data integrity with primary keys and constraints
- **Error Handling**: Robust error management with rollback capabilities
- **Scalable Design**: Easy to extend for additional leagues
- **Environment Security**: Secure credential management

## 🔄 Data Flow

1. **Extract**: Fetch data from LiveScore API
2. **Transform**: Process and structure the data using Pandas
3. **Load**: Upsert data into PostgreSQL database
4. **Validate**: Ensure data integrity and handle conflicts

## 🎯 Use Cases

- **Sports Bars**: Display current standings on screens
- **Public Venues**: Reduce WiFi congestion during matches
- **Data Analysis**: Historical performance tracking
- **Fan Engagement**: Real-time league updates

## 🔮 Future Enhancements

- [ ] Web dashboard for real-time display
- [ ] Support for additional leagues (La Liga, Bundesliga, Serie A)
- [ ] Historical data analysis and trends
- [ ] Automated scheduling with cron jobs
- [ ] REST API for external integrations
- [ ] Data visualization components

## 📝 API Reference

### LiveScore API Endpoints
- **Base URL**: `https://livescore-api.com/api-client/leagues/table.json`
- **Parameters**:
  - `key`: API key
  - `secret`: API secret
  - `competition_id`: League identifier
  - `include_form`: Include team form data

### Supported League IDs
- Premier League: `2`
- Ligue 1: `5`

## 🤝 Contributing

This is a learning project for portfolio purposes. Feel free to:
- Report issues
- Suggest improvements
- Fork for your own learning

## 📄 License

This project is for educational and portfolio purposes.

## 👨‍💻 Author

**Adrien Duval** - Data Engineering Student
- Portfolio project demonstrating data engineering skills
- Focus on real-world problem solving and technical implementation

---

*This project showcases practical data engineering skills including API integration, database management, and ETL processes in a real-world scenario.*
