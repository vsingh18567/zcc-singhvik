import os

import requests
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

API_DOMAIN = os.environ.get("DOMAIN")
API_EMAIL = os.environ.get("EMAIL")
API_TOKEN = os.environ.get("TOKEN")


def make_request(url):
    return requests.get(url, auth=(f"{API_EMAIL}/token", API_TOKEN))


def prettify_ticket(ticket):
    """
    makes ticket info pretty
    """
    ticket_time = parser.parse(ticket["created_at"])
    ticket["created_at"] = f"{ticket_time.year}/{ticket_time.month}/{ticket_time.day}"

    ticket["status"] = str(ticket["status"]).capitalize()
    ticket["priority"] = str(ticket["priority"]).capitalize()
    return ticket


def verify_response(url, keyword):
    """
    checks if response is status 200 and if so, finds the name of the keyword
    """
    res = make_request(url)
    return res.json()[keyword]["name"] if res.status_code == 200 else None
