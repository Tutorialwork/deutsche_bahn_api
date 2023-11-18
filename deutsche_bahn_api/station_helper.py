import json
import pkgutil
import mpu

from deutsche_bahn_api.station import Station


class StationHelper:
    stations: list

    def __init__(self) -> None:
        self.stations = []
        self.load_stations()

    def load_stations(self):
        if len(self.stations) > 0:
            return

        json_raw = pkgutil.get_data(__name__, "static/train_stations_list.json")
        stations = json.loads(json_raw)
        for item in stations:
            self.stations.append(Station(**item))

    def find_stations_by_lat_long(self, target_lat: float, target_long: float, radius: int) -> list[Station]:
        results: list[Station] = []

        for station in self.stations:
            distance = mpu.haversine_distance(
                (station.lat, station.long),
                (target_lat, target_long))
            if distance < radius:
                results.append(station)

        return results

    def find_stations_by_name(self, query: str) -> list[Station]:
        return [station for station in self.stations if query in station.name]
