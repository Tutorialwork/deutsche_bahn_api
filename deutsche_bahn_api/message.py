import json
import pkgutil


def resolve_message_by_code(code: int) -> str:
    json_raw = pkgutil.get_data(__name__, "static/message_codes.json")
    message_codes = json.loads(json_raw)
    for code_object in message_codes:
        if code_object['code'] == code:
            return code_object['message']


class Message:
    id: str
    code: str
    message: str
    time: str
