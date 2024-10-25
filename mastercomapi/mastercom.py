from mastercomapi.structures import Student
import requests
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Mastercom:
    def __init__(
        self,
        instance: str,
        username: str,
        password: str,
        base_url: str,
        stripe_mid: str,
        stripe_sid: str,
    ) -> None:
        """
        Mastercom API Client

        :param instance: The instance of the school
        :param username: The username you use to login to Mastercom Genitori
        :param password: The password of the account
        :param base_url: The base URL of the school's Mastercom website
        :param stripe_mid: The __stripe_mid cookie
        :param stripe_sid: The __stripe_sid cookie
        """

        self.instance = instance
        self.username = username
        self.password = password
        self.base_url = base_url

        # Create a session object
        self.session = requests.Session()

        # Set cookies explicitly
        self.session.cookies.update(
            {
                "__stripe_mid": stripe_mid,
                "__stripe_sid": stripe_sid,
            }
        )

        # Authenticate and store token
        self.auth = self.authenticate()

        self.jwt = self.auth.get("token")

        # Update the session with the authorization token
        self.session.headers.update({"Authorization": f"JWT {self.jwt}"})

        log.info(f"Authenticated as {self.auth.get('nome')} {self.auth.get('cognome')}")

    def authenticate(self) -> dict:
        url = f"{self.base_url}/api/v4/utenti/login/"
        data = {
            "mastercom": self.instance,
            "utente": self.username,
            "password": self.password,
        }

        # Send the POST request
        response = self.session.post(url=url, json=data)

        # Raise an exception if the request fails
        response.raise_for_status()

        # Return the JSON response
        return response.json()

    def get_student(self, student_int: int = 0) -> Student:
        _data = self.auth.get("studenti")[student_int]

        return Student(
            _data, session=self.session, base_url=self.base_url, instance=self.instance
        )
