import streamlit as st

from utils.data_loader import load_deliveries

#BETTER UI
st.set_page_config(
    page_title="IPL Intelligence Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("IPL Intelligence Dashboard")

st.write("A smart cricket analytics platform built from ball-by-ball IPL data.")

deliveries = load_deliveries()

total_matches = deliveries["match_id"].nunique()
total_balls = len(deliveries)
total_runs = deliveries["batter_runs"].sum()
total_wickets = deliveries["is_wicket"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Matches", total_matches)
col2.metric("Balls", total_balls)
col3.metric("Runs", total_runs)
col4.metric("Wickets", total_wickets)

st.divider()

st.subheader("Project Goal")

st.write(
    """
    This dashboard analyzes cricket beyond basic scorecards.
    It helps answer questions like:
    
    - Which players perform under pressure?
    - Who scores fastest in death overs?
    - Which teams are stronger in different phases?
    - Which venues favor batting or bowling?
    """
)
st.divider()
st.subheader("Available Sections")

st.write(
    """
    Use the sidebar to open Player Analytics.
    More sections like Team Analytics, Venue Analytics, and Match Insights
    will be added step by step.
    """
)

st.divider()
st.subheader("Data Source")

st.write(
    """
    The dashboard uses ball-by-ball IPL data from Cricsheet.
    Raw JSON files are downloaded, extracted, and converted into a clean CSV file
    for analysis.
    """
)

# st.subheader("Sample Data")

# st.dataframe(deliveries)
with st.expander("Ball-by-Ball Data Preview"):
    st.dataframe(deliveries)