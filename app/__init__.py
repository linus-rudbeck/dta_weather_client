from app.api_client import get_measurements_df, get_station_metadata, get_measurements
from app.config import Config
import pandas as pd
import json
from tqdm import tqdm

def get_all_stations():
    stations = []
    
    for station_id in Config.STATION_IDS:
        station_data = get_station_metadata(station_id)
        stations.append(station_data)
    
    return stations


def save_stations_to_json():
    data = get_all_stations()
    with open("data/stations.json", "w", encoding="utf-8") as f:
        data_json = json.dumps(data)
        f.write(data_json)


def run():
    dates = pd.date_range("2024-01-02", "2024-12-31", freq="D")
    
    df = get_measurements_df("SE01", "2024", "01", "01")
    
    for d in tqdm(dates):
        month_str = str(d.month).zfill(2)
        day_str = str(d.day).zfill(2)
        df_d = get_measurements_df("SE01", d.year, month_str, day_str)
        df = pd.concat([df, df_d])
    
    df.to_csv("data/test.csv", index=False)