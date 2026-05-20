from pathlib import Path
import json

import pandas as pd


RAW_JSON_DIR = Path("data/raw/ipl_json")
OUTPUT_PATH = Path("data/deliveries.csv")


def parse_match(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        match = json.load(file)

    info = match["meta"]
    match_info = match["info"]

    season = match_info.get("season", "Unknown")
    venue = match_info.get("venue", "Unknown")
    teams = match_info.get("teams", [])

    rows = []

    for innings_number, innings in enumerate(match["innings"], start=1):
        batting_team = innings["team"]

        if len(teams) == 2:
            bowling_team = teams[1] if teams[0] == batting_team else teams[0]
        else:
            bowling_team = "Unknown"

        for over_data in innings["overs"]:
            over_number = over_data["over"]

            for ball_number, delivery in enumerate(over_data["deliveries"], start=1):
                batter = delivery["batter"]
                bowler = delivery["bowler"]

                batter_runs = delivery["runs"]["batter"]
                extra_runs = delivery["runs"]["extras"]
                total_runs = delivery["runs"]["total"]

                wickets = delivery.get("wickets", [])
                is_wicket = 1 if len(wickets) > 0 else 0

                player_out = ""
                wicket_type = ""

                if is_wicket:
                    player_out = wickets[0].get("player_out", "")
                    wicket_type = wickets[0].get("kind", "")

                rows.append(
                    {
                        "match_id": json_path.stem,
                        "season": season,
                        "venue": venue,
                        "batting_team": batting_team,
                        "bowling_team": bowling_team,
                        "innings": innings_number,
                        "over": over_number,
                        "ball": ball_number,
                        "batter": batter,
                        "bowler": bowler,
                        "batter_runs": batter_runs,
                        "extra_runs": extra_runs,
                        "total_runs": total_runs,
                        "is_wicket": is_wicket,
                        "player_out": player_out,
                        "wicket_type": wicket_type,
                        "target_runs": 0,
                        "required_run_rate": 0,
                    }
                )

    return rows


def prepare_data():
    all_rows = []

    json_files = list(RAW_JSON_DIR.glob("*.json"))

    print(f"Found {len(json_files)} JSON files.")

    for json_file in json_files:
        match_rows = parse_match(json_file)
        all_rows.extend(match_rows)

    deliveries = pd.DataFrame(all_rows)

    deliveries.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved cleaned deliveries data to: {OUTPUT_PATH}")
    print(f"Total rows: {len(deliveries)}")


if __name__ == "__main__":
    prepare_data()