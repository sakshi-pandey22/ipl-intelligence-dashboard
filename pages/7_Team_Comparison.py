import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_team_metrics

st.set_page_config(
    page_title="Team Comparison",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Team Comparison")
st.caption("Compare two teams across runs, wickets, and scoring rate.")

deliveries = load_deliveries()

seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

teams = sorted(deliveries["batting_team"].dropna().unique())

if len(teams) < 2:
    st.warning("Not enough teams found for this season.")
    st.stop()

team_1 = st.selectbox("Choose first team", teams)

second_team_options = [team for team in teams if team != team_1]

team_2 = st.selectbox("Choose second team", second_team_options)

metrics_1 = calculate_team_metrics(deliveries, team_1)
metrics_2 = calculate_team_metrics(deliveries, team_2)

comparison_data = pd.DataFrame(
    [
        {
            "Team": team_1,
            "Runs": metrics_1["team_runs"],
            "Balls": metrics_1["team_balls"],
            "Wickets Lost": metrics_1["wickets_lost"],
            "Run Rate": metrics_1["run_rate"],
        },
        {
            "Team": team_2,
            "Runs": metrics_2["team_runs"],
            "Balls": metrics_2["team_balls"],
            "Wickets Lost": metrics_2["wickets_lost"],
            "Run Rate": metrics_2["run_rate"],
        },
    ]
)

comparison_data["Run Rate"] = comparison_data["Run Rate"].round(2)

st.subheader("Comparison Table")

st.dataframe(comparison_data)

metric_columns = [
    "Runs",
    "Wickets Lost",
    "Run Rate",
]

comparison_long = comparison_data.melt(
    id_vars="Team",
    value_vars=metric_columns,
    var_name="Metric",
    value_name="Value"
)

st.subheader("Team Multi-Metric Comparison")

comparison_chart = px.bar(
    comparison_long,
    x="Metric",
    y="Value",
    color="Team",
    barmode="group",
    text="Value",
    title="Team Comparison Across Key Metrics"
)

st.plotly_chart(comparison_chart)