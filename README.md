# IPL Intelligence Dashboard

A smart cricket analytics dashboard that turns IPL ball-by-ball data into meaningful insights.

## Project Goal

The goal of this project is to go beyond basic scorecards and create an analytics platform that answers deeper cricket questions:

- Which players perform under pressure?
- Which players score fastest in death overs?
- Which teams are strongest in different match phases?
- Which venues are high-scoring?
- How does match momentum change over time?

## Tech Stack

- Python
- Streamlit
- pandas
- Plotly
- Cricsheet IPL ball-by-ball data

## Features

- Home dashboard with overall IPL metrics
- Player Analytics
- Team Analytics
- Venue Analytics
- Match Insights
- Player Comparison
- Team Comparison
- Pressure Performance Score
- Pressure vs non-pressure analysis
- Phase-wise batting analysis
- Match momentum chart
- Wickets by over chart
- Leaderboards for top pressure performers

## Data Source

The data comes from Cricsheet IPL JSON files.

Raw JSON files are downloaded and extracted into:

```text
data/raw/
```

The project converts them into a cleaned CSV file:

```text
data/deliveries.csv
```

## How to Run

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download data:

```bash
python scripts/download_data.py
```

Extract data:

```bash
python scripts/extract_data.py
```

Prepare cleaned CSV:

```bash
python scripts/prepare_data.py
```

Run the dashboard:

```bash
streamlit run app.py
```

## Project Structure

```text
ipl-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── deliveries.csv
│   ├── sample_deliveries.csv
│   └── raw/
├── pages/
│   ├── 1_Player_Analytics.py
│   ├── 2_Team_Analytics.py
│   ├── 3_Venue_Analytics.py
│   ├── 4_Match_Insights.py
│   ├── 5_Player_Comparison.py
│   ├── 6_Leaderboards.py
│   └── 7_Team_Comparison.py
├── scripts/
│   ├── download_data.py
│   ├── extract_data.py
│   └── prepare_data.py
└── utils/
    ├── data_loader.py
    └── metrics.py
```

## Future Improvements

- More advanced pressure score
- Win probability model
- Bowler analytics
- Partnership analytics
- Venue chasing advantage
- Player form trends across seasons