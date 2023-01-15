from deutsche_bahn_api.message import Message


class TrainChanges:
    """ This class represents changed train attributes. """
    departure: str
    arrival: str
    passed_stations: str
    stations: str
    platform: str
    messages: list[Message]
