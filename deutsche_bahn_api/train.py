from deutsche_bahn_api.message import Message
from datetime import datetime


class Train:
    # Meta
    id: str
    message: Message | None

    # Trip label
    train_type: str
    train_number: str

    # Arrival
    planned_arrival: datetime | None = None
    changed_arrival: datetime | None = None
    planned_arrival_path: str | None
    changed_arrival_path: str | None
    arrival_messages: list[Message] | None = []

    # Departure
    train_line: str | None
    planned_platform: str
    changed_platform: str | None
    planned_departure: datetime | None = None
    changed_departure: datetime | None = None
    planned_departure_path: str
    changed_departure_path: str | None
    departure_messages: list[Message] | None = []

    def __str__(self):
        return (
            "{:>3} {:<5} || {:^16} | {:^5} || {:^16} | {:^5}"
        ).format(self.train_type,
                 self.train_number,
                 datetime.strftime(self.planned_arrival, "%Y-%m-%d %H:%M") if self.planned_arrival is not None else "",
                 self.get_arrival_delay(),
                 datetime.strftime(self.planned_departure, "%Y-%m-%d %H:%M") if self.planned_departure is not None else "",
                 self.get_departure_delay(),
                 )

    def get_arrival_delay(self) -> int | str:
        if self.planned_arrival and self.changed_arrival:
            return int((self.changed_arrival - self.planned_arrival).total_seconds() / 60)
        return ""

    def get_departure_delay(self) -> int | str:
        if self.planned_departure and self.changed_departure:
            return int((self.changed_departure - self.planned_departure).total_seconds() / 60)
        return ""
