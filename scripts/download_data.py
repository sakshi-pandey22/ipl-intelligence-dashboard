from pathlib import Path
import requests


CRICSHEET_URL = "https://cricsheet.org/downloads/ipl_json.zip"
RAW_DATA_DIR = Path("data/raw")
ZIP_PATH = RAW_DATA_DIR / "ipl_json.zip"


def download_ipl_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading IPL data from Cricsheet...")

    response = requests.get(CRICSHEET_URL)

    with open(ZIP_PATH, "wb") as file:
        file.write(response.content)

    print(f"Downloaded file saved to: {ZIP_PATH}")


if __name__ == "__main__":
    download_ipl_data()