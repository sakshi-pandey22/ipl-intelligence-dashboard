from pathlib import Path
import zipfile


ZIP_PATH = Path("data/raw/ipl_json.zip")
EXTRACT_DIR = Path("data/raw/ipl_json")


def extract_ipl_data():
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    print("Extracting IPL JSON files...")

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_file:
        zip_file.extractall(EXTRACT_DIR)

    print(f"Files extracted to: {EXTRACT_DIR}")


if __name__ == "__main__":
    extract_ipl_data()