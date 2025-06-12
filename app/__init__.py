import app.etl as etl


def run():
    etl.load_stations_to_json()
    etl.extract_station_measurements("SE01")