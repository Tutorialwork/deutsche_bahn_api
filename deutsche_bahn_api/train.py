from __future__ import annotations

from deutsche_bahn_api.train_changes import TrainChanges


class Train:
    stop_id: str
    trip_type: str
    train_type: str
    train_number: str
    train_line: str | None
    platform: str
    passed_stations: str | None
    stations: str
    arrival: str
    departure: str | None
    train_changes: TrainChanges | None


