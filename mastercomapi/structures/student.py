import requests
from datetime import datetime


class Student:
    def __init__(
        self, response: dict, session: requests.Session, base_url: str, instance: str
    ) -> None:
        self.response = response

        self.id = self.response.get("id")
        self.school = self.response.get("id_scuola")
        self.name = self.response.get("nome")
        self.picture = self.response.get("foto")
        self.current_year = self.response.get("anno_corrente")

        self.session = session
        self.base_url = base_url
        self.instance = instance

    @property
    def current_class(self):
        years = self.response.get("anni")
        for year in years:
            if year.get("id") == self.current_year:
                return year.get("classe")

        return None

    def get_grades(self) -> list:
        from mastercomapi.structures import Grade

        url = f"{self.base_url}/api/v3/scuole/{self.instance}/studenti/{self.id}/{self.current_year}/voti_plain"

        response = self.session.get(url=url).json()
        grades = []

        for _grade in response:
            grade = Grade(_grade)
            grades.append(grade)

        return grades

    def get_timetable(
        self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> list:
        from mastercomapi.structures import Period

        if start_date is None:
            start_date = datetime.now()

        if end_date is None:
            end_date = start_date

        start_date_fmt = start_date.strftime("%Y-%m-%d")
        end_date_fmt = end_date.strftime("%Y-%m-%d")

        url = f"{self.base_url}/api/v3/scuole/{self.instance}/studenti/{self.id}/{self.current_year}/orario_plain?data_inizio={start_date_fmt}&data_fine={end_date_fmt}"

        response = self.session.get(url=url).json()
        periods = []

        for timeslot in response:
            period = Period(timeslot)
            periods.append(period)

        return periods

    def __str__(self) -> str:
        return f"{self.name} ({self.class_name}) - {self.id} - {self.school} - {self.get_class()}"

    def __repr__(self) -> str:
        return f"<Student {self.name} ({self.class_name})>"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "school": self.school,
            "class": self.get_class(),
            "picture": self.picture,
        }
