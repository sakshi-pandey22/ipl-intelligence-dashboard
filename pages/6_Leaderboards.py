import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_player_metrics

st.set_page_config(
    page_title="Leaderboards",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Leaderboards")
st.caption("Rank players using custom pressure-performance metrics.")

deliveries = load_deliveries()

seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

player_ball_counts = deliveries.groupby("batter")["ball"].count()

minimum_balls = st.slider(
    "Minimum balls faced",
    min_value=1,
    max_value=500,
    value=100
)

# Adding sliders here

minimum_pressure_balls = st.slider(
    "Minimum pressure balls faced",
    min_value=1,
    max_value=100,
    value=20
)

eligible_players = player_ball_counts[player_ball_counts >= minimum_balls].index

leaderboard_rows = []

for player in eligible_players:
    metrics = calculate_player_metrics(deliveries, player)

# condition to check slider part
    if metrics["pressure_balls"] < minimum_pressure_balls:
        continue

    leaderboard_rows.append(
        {
            "Player": player,
            "Runs": metrics["player_runs"],
            "Balls": metrics["player_balls"],
            "Strike Rate": metrics["player_strike_rate"],
            "Boundary %": metrics["boundary_percentage"],
            "Dot Ball %": metrics["dot_ball_percentage"],
            "Pressure Score": metrics["pressure_score"],
        }
    )

leaderboard = pd.DataFrame(leaderboard_rows)
if leaderboard.empty:
    st.warning("No players found for these filters. Lower the minimum balls or pressure balls.")
    st.stop()

leaderboard = leaderboard.sort_values("Pressure Score", ascending=False)
# Rounding off values
leaderboard["Strike Rate"] = leaderboard["Strike Rate"].round(2)
leaderboard["Boundary %"] = leaderboard["Boundary %"].round(2)
leaderboard["Dot Ball %"] = leaderboard["Dot Ball %"].round(2)
leaderboard["Pressure Score"] = leaderboard["Pressure Score"].round(2)

top_10 = leaderboard.head(10)

st.subheader("Top 10 Pressure Performers")

st.dataframe(top_10)

leaderboard_chart = px.bar(
    top_10,
    x="Player",
    y="Pressure Score",
    text="Pressure Score",
    title="Top 10 Players by Pressure Score"
)

st.plotly_chart(leaderboard_chart,use_container_width=True)