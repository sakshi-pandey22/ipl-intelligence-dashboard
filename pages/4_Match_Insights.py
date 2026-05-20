import plotly.express as px
import streamlit as st

from utils.data_loader import load_deliveries
from utils.metrics import calculate_match_metrics

st.set_page_config(
    page_title="Match Insights",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Match Insights")
st.caption("Track match momentum, innings progression, and wickets by over.")

deliveries = load_deliveries()

# seasons = sorted(deliveries["season"].unique())
seasons = sorted(deliveries["season"].astype(str).unique())

selected_season = st.selectbox("Choose a season", seasons)

# deliveries = deliveries[deliveries["season"] == selected_season]
deliveries = deliveries[deliveries["season"].astype(str) == selected_season]

# matches = deliveries["match_id"].unique()
matches = sorted(deliveries["match_id"].dropna().unique())

selected_match = st.selectbox("Choose a match", matches)

metrics = calculate_match_metrics(deliveries, selected_match)

teams_text = " vs ".join(metrics["teams"])

st.subheader(teams_text)

match_col1, match_col2 = st.columns(2)

match_col1.metric("Total Runs", metrics["total_runs"])
match_col2.metric("Total Wickets", metrics["total_wickets"])

st.subheader("Momentum Graph")

momentum_chart = px.line(
    metrics["over_summary"],
    x="over",
    y="cumulative_runs",
    color="innings",
    markers=True,
    title="Cumulative Runs by Over"
)

st.plotly_chart(momentum_chart,use_container_width=True)

wickets_by_over = (
    metrics["match_data"]
    .groupby(["innings", "over"], as_index=False)["is_wicket"]
    .sum()
)

st.subheader("Wickets by Over")

wickets_chart = px.bar(
    wickets_by_over,
    x="over",
    y="is_wicket",
    color="innings",
    barmode="group",
    title="Wickets Lost by Over",
    text="is_wicket"
)

st.plotly_chart(wickets_chart)

st.subheader("Selected Match Ball-by-Ball Data")

st.dataframe(metrics["match_data"])