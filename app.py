from flask import Flask
import requests
from decouple import config

# consts
app = Flask(__name__)
url = "https://zccsinghvik.zendesk.com/api/v2/"
API_EMAIL = config('EMAIL')
API_TOKEN = config('TOKEN')

@app.route('/')
def hello_world():
    data = requests.get(url + "tickets", auth=(f"{API_EMAIL}/token", API_TOKEN))
    print(data.text)

    return "<p>Hello World </p>"