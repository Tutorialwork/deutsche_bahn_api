from typing import NamedTuple


class Station(NamedTuple):
    eva_nr: int
    ds100: str
    ifopt: str
    name: str
    traffic_type: str
    longitude: float
    latitude: float
    operator: str
    operator_nr: int
    status: str
