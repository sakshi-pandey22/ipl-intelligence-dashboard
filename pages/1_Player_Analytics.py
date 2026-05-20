import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_player_metrics

#BETTER UI
st.set_page_config(
    page_title="Player Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Player Analytics")
st.caption("Analyze batting performance, pressure impact, and phase-wise scoring patterns.")

deliveries = load_deliveries()

# seasons = sorted(deliveries["season"].unique())
seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

# deliveries = deliveries[deliveries["season"] == selected_season]
deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

# players = deliveries["batter"].unique()
# players = sorted(deliveries["batter"].dropna().unique())

# selected_player = st.selectbox("Choose a batter", players)

player_ball_counts = deliveries.groupby("batter")["ball"].count()

minimum_balls = st.slider(
    "Minimum balls faced",
    min_value=1,
    max_value=500,
    value=30
)

eligible_players = player_ball_counts[player_ball_counts >= minimum_balls].index

players = sorted(eligible_players.dropna())

if len(players) == 0:
    st.warning("No players found for this minimum balls filter. Lower the slider value.")
    st.stop()

selected_player = st.selectbox("Choose a batter", players)

metrics = calculate_player_metrics(deliveries, selected_player)

player_col1, player_col2, player_col3, player_col4, player_col5 = st.columns(5)

player_col1.metric("Player Runs", metrics["player_runs"])
player_col2.metric("Balls Faced", metrics["player_balls"])
player_col3.metric("Strike Rate", round(metrics["player_strike_rate"], 2))
player_col4.metric("Boundary %", round(metrics["boundary_percentage"], 2))
player_col5.metric("Dot Ball %", round(metrics["dot_ball_percentage"], 2))

pressure_col1, pressure_col2, pressure_col3, pressure_col4 = st.columns(4)

pressure_col1.metric("Pressure Runs", metrics["pressure_runs"])
pressure_col2.metric("Pressure Balls", metrics["pressure_balls"])
pressure_col3.metric("Pressure Strike Rate", round(metrics["pressure_strike_rate"], 2))
pressure_col4.metric("Pressure Score", round(metrics["pressure_score"], 2))
st.divider()

pressure_comparison = {
    "Situation": ["Pressure", "Non-Pressure"],
    "Runs": [metrics["pressure_runs"], metrics["non_pressure_runs"]],
    "Balls": [metrics["pressure_balls"], metrics["non_pressure_balls"]],
}

pressure_chart = px.bar(
    pressure_comparison,
    x="Situation",
    y="Runs",
    text="Runs",
    title="Pressure vs Non-Pressure Runs"
)

st.plotly_chart(pressure_chart)

phase_summary = (
    metrics["player_data"]
    .groupby("phase", as_index=False)
    .agg(
        runs=("batter_runs", "sum"),
        balls=("ball", "count")
    )
)

phase_summary["strike_rate"] = (phase_summary["runs"] / phase_summary["balls"]) * 100

st.divider()
st.subheader("Phase-wise Runs")

phase_runs_chart = px.bar(
    phase_summary,
    x="phase",
    y="runs",
    title="Runs by Match Phase",
    text="runs"
)

st.plotly_chart(phase_runs_chart)

phase_sr_chart = px.line(
    phase_summary,
    x="phase",
    y="strike_rate",
    markers=True,
    title="Strike Rate by Match Phase"
)

st.plotly_chart(phase_sr_chart,use_container_width=True)

st.divider()
# st.subheader("Selected Player Ball-by-Ball Data")

# st.dataframe(metrics["player_data"])

#USING EXPANDER TO MAKE CLEAN PAGE NOW
with st.expander("Selected Player Ball-by-Ball Data"):
    st.dataframe(metrics["player_data"])