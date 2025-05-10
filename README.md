# THE FINALS Leaderboard API Wrapper

A Python API wrapper for accessing leaderboard data from THE FINALS game. This library simplifies fetching and processing leaderboard data across multiple seasons, platforms, and community events.

## Features
- Retrieve leaderboard data for various seasons (S1–S6), closed/open betas, and community events.
- Support for crossplay and platform-specific data (Steam, Xbox, PSN).
- Processed leaderboard data with multi-platform user detection.
- Return data as pandas DataFrames for easy analysis.

Clone the repository and place the `the_finals.py` file in your project directory.

## Usage
```python
from the_finals_api import TheFinals

# Initialize the API wrapper
api = TheFinals()

# Fetch Season 3 leaderboard
s3_lb = api.get_s3_lb()

# Fetch player-specific leaderboard data
player_lb = api.get_s3_lb(name="PlayerName")

# Fetch community event leaderboard
ce44_lb = api.get_ce44_lb()

# Fetch crossplay leaderboard for Season 1
s1_crossplay = api.get_s1_lb()
```

## Methods
- `get_cb1_lb(name="")`: Closed Beta 1 leaderboard.
- `get_cb2_lb(name="")`: Closed Beta 2 leaderboard.
- `get_ob_lb(name="")`: Open Beta leaderboard.
- `get_s1_lb(name="")`: Season 1 leaderboard (crossplay).
- `get_s2_lb(name="")`: Season 2 leaderboard (crossplay).
- `get_s3_lb(name="", type="")`: Season 3 leaderboard (crossplay, optional type: 'worldtour', 'sponsor').
- `get_s4_lb(name="", type="")`: Season 4 leaderboard (crossplay, optional type).
- `get_s5_lb(name="", type="")`: Season 5 leaderboard (crossplay, optional type).
- `get_s6_lb(name="", type="")`: Season 6 leaderboard (crossplay, optional type).
- `get_the_finals_lb(name="")`: THE FINALS leaderboard (crossplay).
- `get_the_orf_lb(name="")`: ORF leaderboard (crossplay).
- `get_ce44_lb(name="")`: Community Event 44 leaderboard.
- `get_ce48_lb(name="")`: Community Event 48 leaderboard.

## Requirements
- Python 3.6+
- `pandas`
- `requests`

## Disclaimer
This is an unofficial wrapper and is not affiliated with Embark Studios or THE FINALS.
