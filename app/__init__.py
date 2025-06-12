import app.etl as etl
from pathlib import Path


def run():
    Path("data/").mkdir(parents=True, exist_ok=True)
    etl.load_stations_to_json()
    etl.extract_all_stations_measurements()
    etl.load_measurements_to_db()
    etl.create_max_temp_plot()