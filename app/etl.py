import json
import sqlite3
from matplotlib import pyplot as plt
import pandas as pd
from tqdm import tqdm

from app.api_client import get_measurements_df, get_station_metadata
from app.config import Config




def extract_station_data():
    stations = []
    
    for station_id in Config.STATION_IDS:
        station_data = get_station_metadata(station_id)
        stations.append(station_data)
    
    return stations


def load_stations_to_json():
    data = extract_station_data()
    with open("data/stations.json", "w", encoding="utf-8") as f:
        data_json = json.dumps(data)
        f.write(data_json)


def extract_station_measurements(station_id):
    dates = pd.date_range("2024-01-02", "2024-12-31", freq="D")
    
    df = get_measurements_df(station_id, "2024", "01", "01")
    
    for d in tqdm(dates):
        month_str = str(d.month).zfill(2)
        day_str = str(d.day).zfill(2)
        df_d = get_measurements_df(station_id, d.year, month_str, day_str)
        df = pd.concat([df, df_d])
    
    df.to_csv(f"data/measurements_{station_id}.csv", index=False)
    

def extract_all_stations_measurements():
    for station_id in Config.STATION_IDS:
        extract_station_measurements(station_id)


def load_measurements_to_db():
    conn = sqlite3.connect(Config.DB_CONNECTION)
    conn.execute("DROP TABLE IF EXISTS measurements")
    
    for station_id in Config.STATION_IDS:
        print(f"Loading {station_id} to SQL")
        df = pd.read_csv(f"data/measurements_{station_id}.csv")
        df.to_sql("measurements", conn, if_exists="append")
    
    conn.commit()
    conn.close()
    
    print("All stations loaded to SQL")


def create_max_temp_plot():

    for station_id in Config.STATION_IDS:
        df = pd.read_csv(f"data/measurements_{station_id}.csv", parse_dates=["datetime"])
        df["date"] = df["datetime"].dt.date
        daily = df.groupby("date").agg({"temp": "max"}).reset_index()
        plt.plot(daily["date"], daily["temp"], label=station_id)

    plt.title("Max daily temp for all station")
    plt.xlabel("Date")
    plt.ylabel("Max temp")
    plt.savefig("data/daily_max_temp.png")