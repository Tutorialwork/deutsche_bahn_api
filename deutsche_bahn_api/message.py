import json
import pkgutil
from datetime import datetime


def code_to_message(code: str) -> str:
    json_raw = pkgutil.get_data(__name__, "static/message_codes.json")
    message_codes = json.loads(json_raw)
    for code_object in message_codes:
        if code_object['code'] == code:
            return code_object['message']


def extend_type(type: str) -> str:
    return {
        'h': 'HIM',
        'q': 'QUALITY CHANGE',
        'f': 'FREE',
        'd': 'CAUSE OF DELAY',
        'i': 'IBIS',
        'u': 'UNASSIGNED IBIS MESSAGE',
        'r': 'DISRUPTION',
        'c': 'CONNECTION',
    }.get(type)


class Message:
    id: str
    code: str
    timestamp: datetime
    type_code: str
    priority: int
    category: str
    from_timestamp: datetime
    to_timestamp: datetime

    message: str
    type: str

    def __init__(self, id: str = None, code: str = None, timestamp: str = None, type_code: str = None,
                 priority: int = None, category: str = None, from_timestamp: str = None, to_timestamp: str = None):
        self.id = id
        self.code = code
        self.message = code_to_message(code)
        self.timestamp = datetime.strptime(timestamp, "%y-%m-%d %H:%M:%S.%f")
        self.type_code = type_code
        self.type = extend_type(type_code)
        self.priority = priority
        self.category = category
        if from_timestamp:
            self.from_timestamp = datetime.strptime(from_timestamp, "%y%m%d%H%M")
        if to_timestamp:
            self.to_timestamp = datetime.strptime(to_timestamp, "%y%m%d%H%M")
