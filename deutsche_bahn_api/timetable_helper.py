from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import xml.etree.ElementTree as elementTree

from deutsche_bahn_api.api.requester import Requester
from deutsche_bahn_api.message import Message, code_to_message
from deutsche_bahn_api.station import Station
from deutsche_bahn_api.train import Train


class TimetableHelper:
    station: Station
    requester: Requester

    def __init__(self, station: Station, requester: Requester) -> None:
        self.station = station
        self.requester = requester

    def get_timetable_complete(self, hour: Optional[int] = None, date: Optional[datetime] = None) -> list[Train]:
        trains = self.get_timetable(hour, date)
        return self.get_timetable_changes(trains)

    def get_timetable(self, hour: Optional[int] = None, date: Optional[datetime] = None) -> list[Train]:
        trains: list[Train] = []
        trains_xml = elementTree.fromstringlist(self.requester.request_timetable(self.station.eva_nr, hour, date))
        for train_xml in trains_xml:
            trip_label_object: dict[str, str] | None = None
            arrival_object: dict[str, str] | None = None
            departure_object: dict[str, str] | None = None
            for train_details in train_xml:
                if train_details.tag == "tl":
                    trip_label_object = train_details.attrib
                if train_details.tag == "dp":
                    departure_object = train_details.attrib
                if train_details.tag == "ar":
                    arrival_object = train_details.attrib

            train: Train = Train()

            train.id = train_xml.attrib.get("id")

            if trip_label_object:
                train.train_type = trip_label_object.get("c")
                train.train_number = trip_label_object.get("n")

            if arrival_object:
                train.planned_arrival_path = arrival_object['ppth']
                train.planned_arrival = datetime.strptime(arrival_object['pt'], "%y%m%d%H%M")

            if departure_object:
                train.train_line = departure_object.get('l')
                train.planned_platform = departure_object.get('pp')
                train.planned_departure_path = departure_object.get('ppth')
                train.planned_departure = datetime.strptime(departure_object.get('pt'), "%y%m%d%H%M")

            trains.append(train)

        return trains

    def get_timetable_changes(self, trains: list) -> list[Train]:
        changed_trains = elementTree.fromstringlist(self.requester.request_timetable_changes(self.station.eva_nr))

        for changed_train in changed_trains:
            found_train: Train | None = None

            for train in trains:
                if train.id == changed_train.attrib["id"]:
                    found_train = train

            if not found_train:
                continue

            for changes in changed_train:
                if changes.tag == "m":
                    found_train.message = Message(
                        id=changes.get("id"),
                        code=changes.get("c"),
                        timestamp=changes.get("ts-tts"),
                        type_code=changes.get("t"),
                        priority=changes.get("pr"),
                        category=changes.get("cat"),
                        from_timestamp=changes.get("from"),
                        to_timestamp=changes.get("to"),
                    )

                if changes.tag == "dp":
                    ct = changes.get("ct")
                    found_train.changed_departure = datetime.strptime(changes.get("ct"), "%y%m%d%H%M") if ct else None
                    found_train.changed_departure_path = changes.get("cpth")
                    found_train.planned_platform = changes.get("cp")

                    for message in changes:
                        found_train.departure_messages.append(Message(
                            id=message.get("id"),
                            code=message.get("c"),
                            timestamp=message.get("ts-tts"),
                            type_code=message.get("t"),
                        ))

                if changes.tag == "ar":
                    ct = changes.get("ct")
                    found_train.changed_arrival = datetime.strptime(changes.get("ct"), "%y%m%d%H%M") if ct else None
                    found_train.changed_arrival_path = changes.get("cpth")

                    for message in changes:
                        found_train.arrival_messages.append(Message(
                            id=message.get("id"),
                            code=message.get("c"),
                            timestamp=message.get("ts-tts"),
                            type_code=message.get("t"),
                        ))

        return trains
