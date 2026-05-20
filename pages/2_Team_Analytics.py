import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_team_metrics

st.set_page_config(
    page_title="Team Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)


st.title("Team Analytics")
st.caption("Compare team scoring strength, wickets, run rate, and phase-wise performance.")

deliveries = load_deliveries()

# seasons = sorted(deliveries["season"].unique())
seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

# deliveries = deliveries[deliveries["season"] == selected_season]
deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

# teams = deliveries["batting_team"].unique()
teams = sorted(deliveries["batting_team"].dropna().unique())

selected_team = st.selectbox("Choose a team", teams)

metrics = calculate_team_metrics(deliveries, selected_team)

team_col1, team_col2, team_col3, team_col4 = st.columns(4)

team_col1.metric("Team Runs", metrics["team_runs"])
team_col2.metric("Balls Faced", metrics["team_balls"])
team_col3.metric("Wickets Lost", metrics["wickets_lost"])
team_col4.metric("Run Rate", round(metrics["run_rate"], 2))

phase_summary = (
    metrics["team_data"]
    .groupby("phase", as_index=False)
    .agg(
        runs=("total_runs", "sum"),
        balls=("ball", "count")
    )
)

phase_summary["run_rate"] = (phase_summary["runs"] / phase_summary["balls"]) * 6

st.subheader("Phase-wise Team Runs")

phase_runs_chart = px.bar(
    phase_summary,
    x="phase",
    y="runs",
    title="Team Runs by Match Phase",
    text="runs"
)

st.plotly_chart(phase_runs_chart,use_container_width=True)

phase_run_rate_chart = px.line(
    phase_summary,
    x="phase",
    y="run_rate",
    markers=True,
    title="Team Run Rate by Match Phase"
)

st.plotly_chart(phase_run_rate_chart)

# st.subheader("Selected Team Ball-by-Ball Data")

# st.dataframe(metrics["team_data"])
with st.expander("Selected Team Ball-by-Ball Data"):
    st.dataframe(metrics["team_data"])