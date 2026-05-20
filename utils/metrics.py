def calculate_player_metrics(deliveries, selected_player):
    player_data = deliveries[deliveries["batter"] == selected_player]

    player_runs = player_data["batter_runs"].sum()
    player_balls = len(player_data)

    non_pressure_data = player_data[player_data["is_pressure_ball"] == False]
    non_pressure_runs = non_pressure_data["batter_runs"].sum()
    non_pressure_balls = len(non_pressure_data)


    if player_balls > 0:
        player_strike_rate = (player_runs / player_balls) * 100
    else:
        player_strike_rate = 0

    boundaries = player_data[player_data["batter_runs"].isin([4, 6])]
    boundary_percentage = (len(boundaries) / player_balls) * 100

    dot_balls = player_data[player_data["total_runs"] == 0]
    dot_ball_percentage = (len(dot_balls) / player_balls) * 100

    pressure_data = player_data[player_data["is_pressure_ball"] == True]

    pressure_runs = pressure_data["batter_runs"].sum()
    pressure_balls = len(pressure_data)

    if pressure_balls > 0:
        pressure_strike_rate = (pressure_runs / pressure_balls) * 100
    else:
        pressure_strike_rate = 0

    pressure_score = pressure_strike_rate + boundary_percentage - dot_ball_percentage

    return {
        "player_data": player_data,
        "player_runs": player_runs,
        "player_balls": player_balls,
        "player_strike_rate": player_strike_rate,
        "boundary_percentage": boundary_percentage,
        "dot_ball_percentage": dot_ball_percentage,
        "pressure_runs": pressure_runs,
        "pressure_balls": pressure_balls,
        "non_pressure_runs": non_pressure_runs,
        "non_pressure_balls": non_pressure_balls,
        "pressure_strike_rate": pressure_strike_rate,
        "pressure_score": pressure_score,
    }

def calculate_team_metrics(deliveries, selected_team):
    team_data = deliveries[deliveries["batting_team"] == selected_team]

    team_runs = team_data["total_runs"].sum()
    team_balls = len(team_data)
    wickets_lost = team_data["is_wicket"].sum()

    if team_balls > 0:
        run_rate = (team_runs / team_balls) * 6
    else:
        run_rate = 0

    return {
        "team_data": team_data,
        "team_runs": team_runs,
        "team_balls": team_balls,
        "wickets_lost": wickets_lost,
        "run_rate": run_rate,
    }


def calculate_venue_metrics(deliveries, selected_venue):
    venue_data = deliveries[deliveries["venue"] == selected_venue]

    total_runs = venue_data["total_runs"].sum()
    total_balls = len(venue_data)
    total_wickets = venue_data["is_wicket"].sum()
    matches = venue_data["match_id"].nunique()

    if matches > 0:
        average_runs_per_match = total_runs / matches
    else:
        average_runs_per_match = 0

    if total_balls > 0:
        run_rate = (total_runs / total_balls) * 6
    else:
        run_rate = 0

    return {
        "venue_data": venue_data,
        "total_runs": total_runs,
        "total_balls": total_balls,
        "total_wickets": total_wickets,
        "matches": matches,
        "average_runs_per_match": average_runs_per_match,
        "run_rate": run_rate,
    }

def calculate_match_metrics(deliveries, selected_match):
    match_data = deliveries[deliveries["match_id"] == selected_match]

    total_runs = match_data["total_runs"].sum()
    total_wickets = match_data["is_wicket"].sum()
    teams = match_data["batting_team"].unique()

    over_summary = (
        match_data
        .groupby(["innings", "over"], as_index=False)["total_runs"]
        .sum()
    )

    over_summary["cumulative_runs"] = (
        over_summary
        .groupby("innings")["total_runs"]
        .cumsum()
    )

    return {
        "match_data": match_data,
        "total_runs": total_runs,
        "total_wickets": total_wickets,
        "teams": teams,
        "over_summary": over_summary,
    }