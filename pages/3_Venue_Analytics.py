import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_venue_metrics
st.set_page_config(
    page_title="Venue Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Venue Analytics")
st.caption("Understand scoring behavior across IPL venues and match phases.")

deliveries = load_deliveries()

# seasons = sorted(deliveries["season"].unique())
seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

# deliveries = deliveries[deliveries["season"] == selected_season]
deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

# venues = deliveries["venue"].unique()
venues = sorted(deliveries["venue"].dropna().unique())

selected_venue = st.selectbox("Choose a venue", venues)

metrics = calculate_venue_metrics(deliveries, selected_venue)

venue_col1, venue_col2, venue_col3, venue_col4 = st.columns(4)

venue_col1.metric("Matches", metrics["matches"])
venue_col2.metric("Total Runs", metrics["total_runs"])
venue_col3.metric("Avg Runs / Match", round(metrics["average_runs_per_match"], 2))
venue_col4.metric("Run Rate", round(metrics["run_rate"], 2))

innings_runs = metrics["venue_data"].groupby("innings", as_index=False)["total_runs"].sum()

st.subheader("Runs by Innings")

innings_chart = px.bar(
    innings_runs,
    x="innings",
    y="total_runs",
    title="Runs by Innings at Venue",
    text="total_runs"
)

st.plotly_chart(innings_chart)

phase_runs = metrics["venue_data"].groupby("phase", as_index=False)["total_runs"].sum()

st.subheader("Venue Runs by Match Phase")

phase_chart = px.bar(
    phase_runs,
    x="phase",
    y="total_runs",
    title="Runs by Phase at Venue",
    text="total_runs"
)

st.plotly_chart(phase_chart)

st.subheader("Selected Venue Ball-by-Ball Data")

st.dataframe(metrics["venue_data"])