import re
import json
from pathlib import Path
from datetime import datetime

# precompile
_AGE_TAG_RX = re.compile(r"\d{1,2}[Uu]")
_HOME_TEAM_RX = re.compile(r"Top 1st - (?P<team>.+)")
_AWAY_TEAM_RX = re.compile(r"Bottom 1st - (?P<team>.+)")


def parse_date(raw: str) -> str:
    return datetime.strptime(raw, "%Y%m%d").strftime("%Y-%m-%d")


def clean_team_name(raw_name: str) -> str:
    return "".join(_AGE_TAG_RX.sub("", raw_name).lower().split())


def parse_team_from_log(raw_text: str, pattern: re.Pattern) -> str:
    match = pattern.search(raw_text)
    return clean_team_name(match["team"]) if match else "unknown"


def parse_game_metadata(log_path: Path, processed_dir: Path) -> dict[str, object]:
    """Parse one log, write its processed copy, and return metadata. Assumes processed_dir exists."""
    raw_text = log_path.read_text(encoding="utf-8")
    raw_date = log_path.stem.split("_", 1)[0]
    date = parse_date(raw_date)

    home_team = parse_team_from_log(raw_text, _HOME_TEAM_RX)
    away_team = parse_team_from_log(raw_text, _AWAY_TEAM_RX)

    game_id = f"{date}_{home_team}_{away_team}"
    processed_filename = f"{game_id}.txt"
    save_path = processed_dir / processed_filename

    save_path.write_text(raw_text, encoding="utf-8")  # assumes processed_dir is already present

    return {
        "game_id": game_id,
        "date": date,
        "home_team": home_team,
        "away_team": away_team,
        "raw_text": raw_text,
        "processed_filename": processed_filename,
    }


def collect_metadata(raw_logs_dir: Path, processed_dir: Path) -> list[dict[str, object]]:
    return [
        parse_game_metadata(f, processed_dir)
        for f in sorted(raw_logs_dir.iterdir())
        if f.is_file()
    ]


def write_metadata(metadata: list[dict[str, object]], output_path: Path) -> None:
    """Serialize metadata. Assumes output_path.parent exists."""
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)


from pathlib import Path
from your_module import collect_metadata, write_metadata

RAW = Path("data/raw")
PROCESSED = Path("data/preproc_gamelogs")
OUTPUT = Path("data/game_metadata/parsed_game_metadata.json")

metadata = collect_metadata(RAW, PROCESSED)
write_metadata(metadata, OUTPUT)
