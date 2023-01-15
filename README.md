# Deutsche Bahn Api

This is a small Python package to access the Deutsche Bahn timetables api.
The timetable api is able to request the timetable of a specific station and access all dynamic changes on the timetable e.g. changed departure or arrival of the train, changed platform of arrival or a changed path of the train.

## Setup

- Create a account at: https://developers.deutschebahn.com
- Create a new application using this url: https://developers.deutschebahn.com/db-api-marketplace/apis/application/new and choose a name that you want
- After that save you the client id and the client secret. You need it to interact with the api
- Navigate to all available apis page at: https://developers.deutschebahn.com/db-api-marketplace/apis/product and select the "Timetables" api
- And click the red subscribe button and select your application
- Now you are done and can start using the api

### ApiAuthentication

Create a new ApiAuthentication class and pass to it the newly created client id and client secret.
And test with the ```api.test_credentials()``` function if the api authentication works.

```python
api = ApiAuthentication("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
success: bool = api.test_credentials()
```

### Stations

To get the timetable of a specific train station you can use the name or lat and long values.

```python
station_helper = StationHelper()
station_helper.load_stations()
found_stations = station_helper.find_stations_by_lat_long(47.996713, 7.842174, 10)
found_stations_by_name = station_helper.find_stations_by_name("Freiburg")
```

### Timetable

With the station object you are able to request the timetable from the station using the following code.

```python
timetable_helper = TimetableHelper(YOUR_STATION_OBJECT, YOUR_API_AUTHENTICATION_OBJECT)
trains_in_this_hour = timetable_helper.get_timetable()
trains_at_given_hour = timetable_helper.get_timetable(12)
```

This method returns you a list with all trains that are scheduled for departure at this station in the current hour.
You can also pass the ```get_timetable()``` function the hour you want to request.
**Important** this list **don't** contains delays, platform changes or changed stations.
This can be achieved by using the ```get_timetable_changes()``` function and passing the list from the previous step.

```python
trains_with_changes = timetable_helper.get_timetable_changes(trains)
```
