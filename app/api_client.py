import requests
from app.config import Config
import pandas as pd

def get_station_metadata(station_id):
    # http://localhost:5555/SE01
    # url = f"{Config.API_BASE_URL}{station_id}"
    url = Config.API_BASE_URL + station_id
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response)


def get_measurements(station_id, year, month, day):
    # http://localhost:5555/SE01/2024/04/24
    url = Config.API_BASE_URL + f"{station_id}/{year}/{month}/{day}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(response)
    
    
def get_measurements_df(station_id, year, month, day):
    url = Config.API_BASE_URL + f"{station_id}/{year}/{month}/{day}"
    df = pd.read_csv(url, sep="\t", names=["time", "temp", "rain"])
    df["date"] = f"{year}-{month}-{day}"
    df["station_id"] = station_id
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df.drop(columns=["date", "time"], inplace=True)
    return df