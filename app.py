from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import json
import os

# consts
load_dotenv()
app = Flask(__name__)
main_url = "https://zccsinghvik.zendesk.com/api/v2/"
API_EMAIL = os.environ.get('EMAIL')
API_TOKEN = os.environ.get('TOKEN')


@app.route('/tickets')
def hello_world(url=None):
    if not url:
        url = f"{main_url}tickets.json?page[size]=25"
    data = requests.get(url, auth=(f"{API_EMAIL}/token", API_TOKEN)).json()
    has_more = data['meta']['has_more']
    next_link = None
    prev_link = data['links']['prev']
    if has_more:
        next_link = data['links']['next']

    return render_template('view_all.html', ticket_data=data["tickets"], next_link=next_link, prev_link=prev_link)


@app.route('/ticket/<id>')
def ticket_id(id):
    return render_template("view_one.html")


if __name__ == "__main__":
    app.run(debug=True)
