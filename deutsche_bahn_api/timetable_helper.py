from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import requests
import xml.etree.ElementTree as elementTree

from deutsche_bahn_api.api_authentication import ApiAuthentication
from deutsche_bahn_api.message import Message, resolve_message_by_code
from deutsche_bahn_api.station import Station
from deutsche_bahn_api.train import Train
from deutsche_bahn_api.train_changes import TrainChanges


class TimetableHelper:
    station: Station
    api_authentication: ApiAuthentication

    def __init__(self, station: Station, api_authentication: ApiAuthentication) -> None:
        self.station = station
        self.api_authentication = api_authentication

    def get_timetable_xml(self, hour: Optional[int] = None, date: Optional[datetime] = None) -> str:
        hour_date: datetime = datetime.now()
        if hour:
            hour_date = datetime.strptime(str(hour), "%H")
        date_string: str = datetime.now().strftime("%y%m%d")
        if date is not None:
            date_string = date.strftime("%y%m%d")
        hour: str = hour_date.strftime("%H")
        response = requests.get(
            f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
            f"/plan/{self.station.EVA_NR}/{date_string}/{hour}",
            headers=self.api_authentication.get_headers()
        )
        if response.status_code == 410:
            return self.get_timetable_xml(int(hour), datetime.now() + timedelta(days=1))
        elif response.status_code == 401:
            raise Exception("Can't request timetable because the credentials are not correct. Please make sure that "
                            "you providing the correct credentials.")
        elif response.status_code != 200:
            raise Exception("Can't request timetable! The request failed with the HTTP status code {}: {}"
                            .format(response.status_code, response.text))
        return response.text

    def get_timetable(self, hour: Optional[int] = None) -> list[Train]:
        train_list: list[Train] = []
        trains = elementTree.fromstringlist(self.get_timetable_xml(hour))
        for train in trains:
            trip_label_object: dict[str, str] | None = None
            arrival_object: dict[str, str] | None = None
            departure_object: dict[str, str] | None = None
            for train_details in train:
                if train_details.tag == "tl":
                    trip_label_object = train_details.attrib
                if train_details.tag == "dp":
                    departure_object = train_details.attrib
                if train_details.tag == "ar":
                    arrival_object = train_details.attrib

            if not departure_object:
                """ Arrival without department """
                continue

            train_object: Train = Train()
            train_object.stop_id = train.attrib["id"]
            train_object.train_type = trip_label_object["c"]
            train_object.train_number = trip_label_object["n"]
            train_object.platform = departure_object['pp']
            train_object.stations = departure_object['ppth']
            train_object.departure = departure_object['pt']

            if "f" in trip_label_object:
                train_object.trip_type = trip_label_object["f"]

            if "l" in departure_object:
                train_object.train_line = departure_object['l']

            if arrival_object:
                train_object.passed_stations = arrival_object['ppth']
                train_object.arrival = arrival_object['pt']

            train_list.append(train_object)

        return train_list

    def get_timetable_changes(self, trains: list) -> list[Train]:
        response = requests.get(
            f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{self.station.EVA_NR}",
            headers=self.api_authentication.get_headers()
        )
        changed_trains = elementTree.fromstringlist(response.text)

        train_list: list[Train] = []

        for changed_train in changed_trains:
            found_train: Train | None = None
            train_changes: TrainChanges = TrainChanges()
            train_changes.messages = []

            for train in trains:
                if train.stop_id == changed_train.attrib["id"]:
                    found_train = train

            if not found_train:
                continue

            for changes in changed_train:
                if changes.tag == "dp":
                    if "ct" in changes.attrib:
                        train_changes.departure = changes.attrib["ct"]
                    if "cpth" in changes.attrib:
                        train_changes.stations = changes.attrib["cpth"]
                    if "cp" in changes.attrib:
                        train_changes.platform = changes.attrib["cp"]

                if changes.tag == "ar":
                    if "ct" in changes.attrib:
                        train_changes.arrival = changes.attrib["ct"]
                    if "cpth" in changes.attrib:
                        train_changes.passed_stations = changes.attrib["cpth"]

                for message in changes:
                    new_message = Message()
                    new_message.id = message.attrib["id"]
                    new_message.code = message.attrib["c"]
                    new_message.time = message.attrib["ts"]
                    new_message.message = resolve_message_by_code(int(message.attrib["c"]))
                    train_changes.messages.append(new_message)

            found_train.train_changes = train_changes
            train_list.append(found_train)

        return train_list
