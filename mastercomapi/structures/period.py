from datetime import datetime


class Period:
    def __init__(self, response: dict) -> None:
        self.response = response

        self.subject = self.response.get("titolo")
        self.teacher = self.response.get("sottotitolo")

        self.start = datetime.fromisoformat(self.response.get("data_ora_inizio"))
        self.end = datetime.fromisoformat(self.response.get("data_ora_fine"))

    def __str__(self) -> str:
        return f"{self.subject} - {self.teacher} - {self.start} - {self.end}"

    def __repr__(self) -> str:
        return f"{self.subject} - {self.teacher} - {self.start} - {self.end}"

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "teacher": self.teacher,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }
