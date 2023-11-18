import requests
from typing import Optional
from datetime import datetime, timedelta


class Requester:
    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_headers(self) -> dict[str, str]:
        return {
            "DB-Api-Key": self.client_secret,
            "DB-Client-Id": self.client_id,
        }

    def test_credentials(self) -> bool:
        response = requests.get(
            "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/BLS",
            headers=self.get_headers()
        )
        return response.status_code == 200

    def request_timetable(self, eva_nr: str, hour: Optional[int] = None, date: Optional[datetime] = None) -> str:
        hour_date: datetime = datetime.now()
        if hour:
            hour_date = datetime.strptime(str(hour), "%H")
        date_string: str = datetime.now().strftime("%y%m%d")
        if date is not None:
            date_string = date.strftime("%y%m%d")
        hour: str = hour_date.strftime("%H")
        response = requests.get(
            f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
            f"/plan/{eva_nr}/{date_string}/{hour}",
            headers=self.get_headers()
        )
        if response.status_code == 410:
            return self.request_timetable(eva_nr, int(hour), datetime.now() + timedelta(days=1))
        elif response.status_code == 401:
            raise Exception("Can't request timetable because the credentials are not correct. Please make sure that "
                            "you providing the correct credentials.")
        elif response.status_code != 200:
            raise Exception("Can't request timetable! The request failed with the HTTP status code {}: {}"
                            .format(response.status_code, response.text))
        return response.text

    def request_timetable_changes(self, eva_nr: str) -> str:
        response = requests.get(
            f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{eva_nr}",
            headers=self.get_headers()
        )
        if response.status_code == 410:
            return self.request_timetable(eva_nr)
        elif response.status_code == 401:
            raise Exception("Can't request timetable because the credentials are not correct. Please make sure that "
                            "you providing the correct credentials.")
        elif response.status_code != 200:
            raise Exception("Can't request timetable! The request failed with the HTTP status code {}: {}"
                            .format(response.status_code, response.text))
        return response.text
