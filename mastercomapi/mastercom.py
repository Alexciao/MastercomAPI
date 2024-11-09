import json
import os
from mastercomapi.structures import Student
import requests
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Mastercom:

    def __init__(
        self,
        instance: str = None,
        username: str = None,
        password: str = None,
        base_url: str = None,
        stripe_mid: str = None,
        stripe_sid: str = None,
        json_file: str | None = None,
        store_token: bool = False,
    ) -> None:
        """
        Mastercom API Client. You can either initialize
        the client with parameters or by passing in a JSON file.

        :param instance: The instance of the school
        :param username: The username you use to login to Mastercom Genitori
        :param password: The password of the account
        :param base_url: The base URL of the school's Mastercom website
        :param stripe_mid: The __stripe_mid cookie
        :param stripe_sid: The __stripe_sid cookie
        :param json_file: The path to the JSON file containing the credentials
        :param store_token: Whether to store the JWT token in a file
        """

        if json_file:
            self._load_from_json(json_file)
        elif all([instance, username, password, base_url, stripe_mid, stripe_sid]):
            self.instance = instance
            self.username = username
            self.password = password
            self.base_url = base_url
            self.stripe_mid = stripe_mid
            self.stripe_sid = stripe_sid
        else:
            raise ValueError(
                "Not all credentials were provided! To fix this, you can either provide a JSON file with all the credentials (recommended) or pass them into the class. Please remember to keep your creds safe."
            )

        self.store = store_token

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

    def _load_from_json(self, json_file: str) -> None:
        """Load credentials from a JSON file."""
        with open(json_file, "r") as file:
            data = json.load(file)
            try:
                self.instance = data["instance"]
                self.username = data["username"]
                self.password = data["password"]
                self.base_url = data["base_url"]
                self.stripe_mid = data["stripe_mid"]
                self.stripe_sid = data["stripe_sid"]
            except KeyError as e:
                raise ValueError(f"Missing key in JSON file: {e}")

    def authenticate(self) -> dict:
        if self.store and os.path.exists("mc_token.json"):
            with open("mc_token.json", "r") as file:
                return json.load(file)

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
        resp = response.json()

        if self.store:
            with open("mc_token.json", "w") as file:
                json.dump(resp, file)

        return resp

    def get_student(self, student_int: int = 0) -> Student:
        _data = self.auth.get("studenti")[student_int]

        return Student(
            _data, session=self.session, base_url=self.base_url, instance=self.instance
        )
