import json


def resolve_message_by_code(code: int) -> str:
    with open('static/message_codes.json') as message_codes_file:
        message_codes = json.load(message_codes_file)
        for code_object in message_codes:
            if code_object['code'] == code:
                return code_object['message']


class Message:
    id: str
    code: str
    message: str
    time: str

