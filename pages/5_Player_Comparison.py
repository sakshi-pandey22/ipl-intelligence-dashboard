import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_player_metrics

st.set_page_config(
    page_title="Player Comparison",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Player Comparison")
st.caption("Compare two batters across scoring, strike rate, boundaries, and pressure score.")

deliveries = load_deliveries()

seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

player_ball_counts = deliveries.groupby("batter")["ball"].count()

minimum_balls = st.slider(
    "Minimum balls faced",
    min_value=1,
    max_value=500,
    value=30
)

eligible_players = player_ball_counts[player_ball_counts >= minimum_balls].index

players = sorted(eligible_players.dropna())

if len(players) < 2:
    st.warning("Not enough players found for this filter. Lower the minimum balls value.")
    st.stop()

player_1 = st.selectbox("Choose first player", players)

second_player_options = [player for player in players if player != player_1]

player_2 = st.selectbox("Choose second player", second_player_options)

metrics_1 = calculate_player_metrics(deliveries, player_1)
metrics_2 = calculate_player_metrics(deliveries, player_2)

comparison_data = pd.DataFrame(
    [
        {
            "Player": player_1,
            "Runs": metrics_1["player_runs"],
            "Balls": metrics_1["player_balls"],
            "Strike Rate": metrics_1["player_strike_rate"],
            "Boundary %": metrics_1["boundary_percentage"],
            "Dot Ball %": metrics_1["dot_ball_percentage"],
            "Pressure Score": metrics_1["pressure_score"],
        },
        {
            "Player": player_2,
            "Runs": metrics_2["player_runs"],
            "Balls": metrics_2["player_balls"],
            "Strike Rate": metrics_2["player_strike_rate"],
            "Boundary %": metrics_2["boundary_percentage"],
            "Dot Ball %": metrics_2["dot_ball_percentage"],
            "Pressure Score": metrics_2["pressure_score"],
        },
    ]
)

st.subheader("Comparison Table")

st.dataframe(comparison_data)
#STORYTELLING FEATURE
if metrics_1["pressure_score"] > metrics_2["pressure_score"]:
    st.success(f"{player_1} has the higher Pressure Score.")
elif metrics_2["pressure_score"] > metrics_1["pressure_score"]:
    st.success(f"{player_2} has the higher Pressure Score.")
else:
    st.info("Both players have the same Pressure Score.")

if metrics_1["player_strike_rate"] > metrics_2["player_strike_rate"]:
    st.info(f"{player_1} has the higher Strike Rate.")
elif metrics_2["player_strike_rate"] > metrics_1["player_strike_rate"]:
    st.info(f"{player_2} has the higher Strike Rate.")
else:
    st.info("Both players have the same Strike Rate.")

##DONE STORY

st.subheader("Runs Comparison")

runs_chart = px.bar(
    comparison_data,
    x="Player",
    y="Runs",
    text="Runs",
    title="Runs Comparison"
)

st.plotly_chart(runs_chart)

st.subheader("Strike Rate Comparison")

strike_rate_chart = px.bar(
    comparison_data,
    x="Player",
    y="Strike Rate",
    text="Strike Rate",
    title="Strike Rate Comparison"
)

st.plotly_chart(strike_rate_chart)

st.subheader("Pressure Score Comparison")

pressure_chart = px.bar(
    comparison_data,
    x="Player",
    y="Pressure Score",
    text="Pressure Score",
    title="Pressure Score Comparison"
)

st.plotly_chart(pressure_chart)
metric_columns = [
    "Strike Rate",
    "Boundary %",
    "Dot Ball %",
    "Pressure Score",
]

comparison_long = comparison_data.melt(
    id_vars="Player",
    value_vars=metric_columns,
    var_name="Metric",
    value_name="Value"
)

st.subheader("Multi-Metric Comparison")

multi_metric_chart = px.bar(
    comparison_long,
    x="Metric",
    y="Value",
    color="Player",
    barmode="group",
    text="Value",
    title="Player Comparison Across Key Metrics"
)

st.plotly_chart(multi_metric_chart)