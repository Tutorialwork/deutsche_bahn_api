```python
from deutsche_bahn_api.api_authentication import ApiAuthentication
from deutsche_bahn_api.station_helper import StationHelper
from deutsche_bahn_api.timetable_helper import TimetableHelper

api = ApiAuthentication("b47bcf839594dbc0ab1e22b5db9efc61", "89005b9d47fa377c682c13326fbf167f")
success: bool = api.test_credentials()

station_helper = StationHelper()
station_helper.load_stations()
found_stations = station_helper.find_stations_by_lat_long(47.9872898, 7.7262088, 10)

for station in found_stations:
    print(station.NAME)
    print(station.EVA_NR)

timetable_helper = TimetableHelper(found_stations[0], api)
trains = timetable_helper.get_timetable()
trains_with_changes = timetable_helper.get_timetable_changes(trains)

for train in trains_with_changes:
    print(train.__dict__)
    print(train.train_changes.__dict__)
```