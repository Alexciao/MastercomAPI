from datetime import datetime


class Grade:
    def __init__(self, response: dict) -> None:
        self.response = response

        self.subject = self.response.get("titolo")
        self.type = self.response.get("sottotitolo")
        self.description = self.response.get("dettaglio")
        self.grade_display = self.response.get("simbolo")
        self.grade = self.response.get("voto_numerico")
        self.weight = self.response.get("valore_peso")

        self.date = datetime.fromisoformat(self.response.get("data"))

    def __str__(self) -> str:
        return f"{self.subject} - {self.grade_display} - {self.date}"

    def __repr__(self) -> str:
        return f"{self.subject} - {self.grade_display} - {self.date}"

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "type": self.type,
            "description": self.description,
            "grade_display": self.grade_display,
            "grade": self.grade,
            "weight": self.weight,
            "date": self.date.isoformat(),
        }
