import re
from pathlib import Path


home_team_rx = re.compile(r"Top 1st - (?P<hteam>.+)")
away_team_rx = re.compile(r"Bottom 1st - (?P<ateam>.+)")
age_rx = re.compile(r"\d{1,2}[Uu]")

def clean_team_name(team: str) -> str:
    return "".join(age_rx.sub("", team).lower().split())

def get_teams(gamelog: str) -> dict:
    return {
        "home_team": clean_team_name(home_team_rx.search(gamelog).group("hteam")),
        "away_team": clean_team_name(away_team_rx.search(gamelog).group("ateam"))
    }


file = Path("./data/raw/20240111_01.txt")
gamelog = file.read_text()

teams = get_teams(gamelog)


# Rename filenames to include teams
game_date = file.stem.split("_")[0]

from datetime import datetime
def to_iso_date(date: str) -> str:
	return datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")













new_name = f"{game_date}_{teams["home_team"]}_{teams["away_team"]}"

file.rename(file.with_name(new_name))