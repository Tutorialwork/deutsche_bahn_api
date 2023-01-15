from typing import NamedTuple


class Station(NamedTuple):
    EVA_NR: int
    DS100: str
    IFOPT: str
    NAME: str
    Verkehr: str
    Laenge: str
    Breite: str
    Betreiber_Name: str
    Betreiber_Nr: int
    Status: str
