from pathlib import Path

import pandas as pd
import streamlit as st

from scripts.download_data import download_ipl_data
from scripts.extract_data import extract_ipl_data
from scripts.prepare_data import prepare_data

def get_phase(over):
    if over <= 5:
        return "Powerplay"
    elif over <= 15:
        return "Middle Overs"
    else:
        return "Death Overs"

# @st.cache_data
# def load_deliveries():
#     # deliveries = pd.read_csv("data/sample_deliveries.csv")
#     deliveries = pd.read_csv("data/deliveries.csv")

#     if not deliveries_path.exists():
#         with st.spinner("Preparing IPL data. This may take a few minutes on first launch..."):
#             download_ipl_data()
#             extract_ipl_data()
#             prepare_data()

#     deliveries = pd.read_csv(deliveries_path)

#     deliveries["phase"] = deliveries["over"].apply(get_phase)

#     deliveries["is_pressure_ball"] = (
#         (deliveries["over"] >= 16)
#         | ((deliveries["innings"] == 2) & (deliveries["required_run_rate"] >= 12))
#     )

#     return deliveries
@st.cache_data
def load_deliveries():
    deliveries_path = Path("data/deliveries.csv")

    if not deliveries_path.exists():
        with st.spinner("Preparing IPL data. This may take a few minutes on first launch..."):
            download_ipl_data()
            extract_ipl_data()
            prepare_data()

    deliveries = pd.read_csv(deliveries_path)

    deliveries["phase"] = deliveries["over"].apply(get_phase)

    deliveries["is_pressure_ball"] = (
        (deliveries["over"] >= 16)
        | ((deliveries["innings"] == 2) & (deliveries["over"] >= 12))
    )

    return deliveries