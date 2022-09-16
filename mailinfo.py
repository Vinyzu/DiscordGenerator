import requests
import json
import random
import string

class MailInfo:
    global DOMAINS
    global DOMAIN
    global TOKEN
    
    with open("config.json", "r") as conf: config = json.load(conf)
    DOMAINS = config["EMAIL STUFF"]["CUSTOM DOMAINS"]
    DOMAIN = random.choice(DOMAINS)
    TOKEN = "qgk2auEHq94bq5w8s_Fk78Iyt3xJrs9U7ESND5SHWbo"

    def generateInbox(rush=False):
        CHARS = string.ascii_letters + string.digits
        ALIAS = "".join(random.choice(CHARS) for _ in range(11))
        EMAIL = f"{ALIAS}@{DOMAIN}"
        return Inbox(EMAIL, TOKEN)

    """
    getEmail gets the emails from an inbox object
    and returns a list of Email objects
    """
    
    def getEmails(inbox):
        s = TempMail.makeHTTPRequest(f"/custom/{TOKEN}/{DOMAIN}")
        data = json.loads(s)

        # if no emails are found, return an empty list
        # else return a list of email
        if data["email"] == None:
            return ["None"]
        else:
            emails = []
            for email in data["email"]:
                emails.append(Email(email["from"], email["to"], email["subject"], email["body"], email["html"], email["date"]))
            return emails


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
        return ("Email (sender={}, recipient={}, subject={}, body={}, html={}, date={} )".format(self.sender, self.recipient, self.subject, self.body, self.html, self.date))


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
        return ("Inbox (address={}, token={} )".format(self.address, self.token))
