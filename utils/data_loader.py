import pandas as pd
import streamlit as st

def get_phase(over):
    if over <= 5:
        return "Powerplay"
    elif over <= 15:
        return "Middle Overs"
    else:
        return "Death Overs"

@st.cache_data
def load_deliveries():
    # deliveries = pd.read_csv("data/sample_deliveries.csv")
    deliveries = pd.read_csv("data/deliveries.csv")

    deliveries["phase"] = deliveries["over"].apply(get_phase)

    deliveries["is_pressure_ball"] = (
        (deliveries["over"] >= 16)
        | ((deliveries["innings"] == 2) & (deliveries["required_run_rate"] >= 12))
    )

    return deliveries