import os

host = os.getenv("HOST", "localhost")

class Config:
    API_BASE_URL = f"http://{host}:5555/"
    STATION_IDS = ["SE01","SE02","SE03","SE04"]
    DB_CONNECTION = "data/weather_measurements.db"