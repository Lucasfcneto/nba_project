# 🏀 nba_project  
**Automated NBA Data Pipeline using Python, SQLite, and GitHub Actions**

A fully automated data engineering pipeline that retrieves, processes, and stores NBA statistics.  
The project uses `nba_api` to access the (undocumented) JSON endpoints that power https://www.nba.com/stats, and stores all processed data in a versioned SQLite database updated daily via GitHub Actions.

Built for SQL learning, analytics, reproducible research, and real-world data engineering practice.

---

# 🚀 Purpose

This project aims to provide a **clean, reliable, continuously updated NBA dataset**, enabling:

- SQL training and practice  
- Exploratory data analysis  
- Machine learning experiments  
- Dashboard creation (Power BI, Superset, Metabase)  
- Player evaluation (TS%, usage, impact metrics, on/off splits)  
- Game-level analytics and scouting models  
- Demonstration of an end-to-end automated data pipeline  

---

# 📡 How NBA Data Is Retrieved

## Not an official API — but real JSON endpoints

The NBA does **not** publish a public REST API.

However, all pages on:

- https://www.nba.com/stats  
- https://www.nba.com/game  

…fetch their data from **internal JSON endpoints**.  
These endpoints power everything you see on pages such as:

- Player page → https://www.nba.com/stats/player/1629029  
- Team page → https://www.nba.com/stats/team/1610612747  
- Game page → https://www.nba.com/game/0022500253  
- Game charts → https://www.nba.com/game/uta-vs-lal-0022500253/game-charts  
- Box score → https://www.nba.com/game/lal-vs-mil-0022500231/box-score  

Behind each of these pages, the browser makes requests to URLs under:

```
https://stats.nba.com/stats/
```

Examples of real endpoints (not directly accessible via browser):

- `boxscoretraditionalv2`
- `boxscoreadvancedv2`
- `playbyplayv2`
- `commonplayerinfo`
- `leaguegamelog`

These require special headers, so they **do not work** when opened directly.

---

## Why this project uses `nba_api`

Instead of manually handling headers and raw JSON, this project uses:

```
pip install nba_api
```

`nba_api` is a stable wrapper that:

- Manages all required headers  
- Abstracts away endpoint URLs  
- Converts results into pandas DataFrames  
- Handles rate limiting  
- Ensures reproducibility  

Example:

```python
from nba_api.stats.endpoints import boxscoretraditionalv2

df = boxscoretraditionalv2.BoxScoreTraditionalV2(
    game_id="0022500253"
).get_data_frames()[0]
```

This returns a clean DataFrame containing player-level box score data.

---

# 📥 ETL Process (Daily Automated Pipeline)

The pipeline runs automatically every day at **10:00 AM (UTC-3)** via GitHub Actions.

### 1. **Extract**
- Download all games for the configured season  
- Identify new games + previously stored games that may have updated stats  
- Fetch box scores and other endpoints for every relevant `game_id`

### 2. **Transform**
- Standardize column names and dtypes  
- Normalize team, player, and game metadata  
- Apply integrity checks  
- Prepare UPSERT-ready tables  

### 3. **Load**
Store all processed data into SQLite with UPSERT logic:

```sql
ON CONFLICT(game_id, player_id) DO UPDATE SET ...
```

Prevents duplication and ensures always-updated data.

### 4. **Version & Commit**
After the ETL finishes, GitHub Actions automatically:

- Commits the updated `nba.db`  
- Pushes it to the repository  
- Preserves historical versions (perfect for reproducibility)

This turns the repository itself into a mini data warehouse.

---

# 🧱 Project Architecture

```
nba_project/
│
├── analytics/          # Jupyter notebooks & analyses
├── data/               # SQLite database (nba.db)
├── etl/                # Extraction, transformation & loading scripts
├── sql/                # Table schemas & SQL models
├── utils/              # Logging, helpers, shared utilities
└── .github/workflows   # GitHub Actions automation
```

---

# ⚙️ Technologies Used

- **Python 3.11+**  
- **nba_api**  
- **SQLite**  
- **Pandas**  
- **GitHub Actions (cron automation)**  
- **Jupyter Notebook**  

---

# 🗄 Database Schema (Current)

### **teams**
- team_id  
- name  
- abbreviation  
- city  
- conference  
- division  

### **players**
- player_id  
- name  
- position  
- height  
- weight  
- birthdate  
- team_current  

### **games**
- game_id  
- season  
- date  
- home_team_id  
- away_team_id  
- arena  

### **boxscore_traditional**
- game_id  
- player_id  
- team_id  
- minutes  
- points  
- rebounds  
- assists  

*(More tables coming as pipeline evolves.)*

---

# ▶️ Run Locally

### Install dependencies
```
pip install -r requirements.txt
```

### Run ETL manually
```
python etl/etl.py
```

Database will be generated inside `/data`.

---

# 🧪 Roadmap

### ETL & Data Expansion
- Add **advanced stats** ingestion (`boxscoreadvancedv2`)
- Add **play-by-play** ingestion  
- Add **shot chart** data  
- Add **lineups & on/off splits**  
- Add **team-level tables** (ratings, four factors)

### Modeling & Analytics
- Build a **star-schema warehouse**  
- Create **Power BI / Superset dashboards**  
- Compute rolling per-game metrics  
- Build a **player similarity model**  
- ELO or Bayesian game prediction models  

### Engineering Enhancements
- Logging & monitoring  
- Data validation (Great Expectations-style checks)  
- Automated season roll-over  

---

# 📎 Disclaimer  

This repository uses publicly available JSON data served by **NBA Stats** for technical, educational, and analytical purposes.  
It is **not affiliated with, endorsed, or approved** by the NBA or any related organization.

