# source: https://github.com/tempmail-lol/api-python/tree/main/TempMail
import json
import random

import httpx

DOMAINS = ["gmailb.tk", "gmailb.ml", "gmailb.ga"]


class TempMail:
    global BASE_URL
    BASE_URL = "https://api.tempmail.lol"

    """
    Make a request to the tempmail.lol api with a given endpoint
    The content of the request is a json string and is returned as a string object
    """

    def makeHTTPRequest(self):
        headers = {
            "User-Agent": "TempMailPythonAPI/1.0",
            "Accept": "application/json"
        }
        try:
            connection = httpx.get(BASE_URL + self, headers=headers)
            if connection.status_code >= 400:
                raise Exception(f"HTTP Error: {str(connection.status_code)}")
        except Exception as e:
            print(e)
            return None

        return connection.text

    """
    GenerateInbox will generate an inbox with an address and a token
    and returns an Inbox object
    > rush = False will generate a normal inbox with no rush (https://tempmail.lol/news/2022/08/03/introducing-rush-mode-for-tempmail/)
    """
    def generateInbox(self):
        try:
            random_domain = random.choice(DOMAINS)
            s = TempMail.makeHTTPRequest(f"/generate/{random_domain}")
        except:
            print(f"Website responded with: {s}")
        data = json.loads(s)
        return Inbox(data["address"], data["token"])

    """
    getEmail gets the emails from an inbox object
    and returns a list of Email objects
    """
    def getEmails(self):
        s = TempMail.makeHTTPRequest(f"/auth/{self.token}")
        data = json.loads(s)

        # Raise an exception if the token is invalid
        if "token" in s:
            if data["token"] == "invalid":
                raise Exception("Invalid Token")

        # if no emails are found, return an empty list
        # else return a list of email
        if data["email"] is None:
            return ["None"]
        else:
            return [
                Email(
                    email["from"],
                    email["to"],
                    email["subject"],
                    email["body"],
                    email["html"],
                    email["date"],
                )
                for email in data["email"]
            ]

class Email:
    def __init__(self, sender, recipient, subject, body, html, date):
        # make the propertys immutable using @property
        self._sender = sender
        self._recipient = recipient
        self._subject = subject
        self._body = body
        self._html = html
        self._date = date

    @property
    def sender(self):
        return self._sender

    @property
    def recipient(self):
        return self._recipient

    @property
    def subject(self):
        return self._subject

    @property
    def body(self):
        return self._body

    @property
    def html(self):
        return self._html

    @property
    def date(self):
        return self._date

    def __repr__(self):
        return f"Email (sender={self.sender}, recipient={self.recipient}, subject={self.subject}, body={self.body}, html={self.html}, date={self.date} )"

class Inbox:
    def __init__(self, address, token):
        # make the propertys immutable using @property
        self._address = address
        self._token = token

    @property
    def address(self):
        return self._address

    @property
    def token(self):
        return self._token

    def __repr__(self):
        return f"Inbox (address={self.address}, token={self.token} )"