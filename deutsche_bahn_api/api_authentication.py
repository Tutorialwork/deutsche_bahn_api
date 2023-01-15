import requests


class ApiAuthentication:
    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def test_credentials(self) -> bool:
        response = requests.get(
            "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/BLS",
            headers={
                "DB-Api-Key": self.client_secret,
                "DB-Client-Id": self.client_id,
            }
        )
        return response.status_code == 200

    def get_headers(self) -> dict[str, str]:
        return {
                "DB-Api-Key": self.client_secret,
                "DB-Client-Id": self.client_id,
            }

