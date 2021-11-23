from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import json
import os

# consts
load_dotenv()
app = Flask(__name__)
url = "https://zccsinghvik.zendesk.com/api/v2/"
API_EMAIL = os.environ.get('EMAIL')
API_TOKEN = os.environ.get('TOKEN')
tickets = []


@app.route('/tickets')
def hello_world():
    global tickets
    tickets = requests.get(url + "tickets", auth=(f"{API_EMAIL}/token", API_TOKEN)).json()["tickets"]
    return render_template('view_all.html', ticket_data=tickets)

if __name__ == "__main__":
    app.run(debug=True)
