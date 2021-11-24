import os

import requests
from dateutil import parser
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

# consts
load_dotenv()
app = Flask(__name__)
main_url = "https://zccsinghvik.zendesk.com/api/v2/"
API_EMAIL = os.environ.get("EMAIL")
API_TOKEN = os.environ.get("TOKEN")


def prettify_ticket(ticket):
    """
    makes ticket info pretty
    """
    ticket_time = parser.parse(ticket["created_at"])
    ticket["created_at"] = f"{ticket_time.year}/{ticket_time.month}/{ticket_time.day}"

    ticket["status"] = str(ticket["status"]).capitalize()
    ticket["priority"] = str(ticket["priority"]).capitalize()
    return ticket


@app.route("/tickets", methods=["GET", "POST"])
def tickets():
    """
    route for viewing all tickets
    """
    if request.method == "GET":
        request_url = request.args.get(
            "request_url", default=f"{main_url}tickets.json?page[size]=25", type=str
        )
        page = request.args.get("page_num", default=1, type=int)
        error = request.args.get("error", default=None, type=str)
        response = requests.get(request_url, auth=(f"{API_EMAIL}/token", API_TOKEN))

        if response.status_code > 299:
            if request_url != f"{main_url}tickets.json?page[size]=25":
                # try hitting the default page
                return redirect(url_for("tickets", error="Oops something went wrong"))
            # otherwise its probably some server error
            return render_template("error.html")

        data = response.json()

        next_link = None
        prev_link = data["links"]["prev"]

        if data["meta"]["has_more"]:
            next_link = data["links"]["next"]

        if page == 1:
            prev_link = None

        for ticket in data["tickets"]:
            # make dates pretty
            ticket = prettify_ticket(ticket)

        return render_template(
            "view_all.html",
            ticket_data=data["tickets"],
            next_link=next_link,
            prev_link=prev_link,
            error=error,
            page=page,
        )
    else:
        id = request.form["ticket_id"]
        return redirect(url_for("ticket_id", id=id))


@app.route("/ticket/<id>", methods=["GET"])
def ticket_id(id):
    """
    :param id: ticket id
    route for viewing details of a specific ticket
    """
    response = requests.get(
        f"{main_url}tickets/{id}.json", auth=(f"{API_EMAIL}/token", API_TOKEN)
    )
    if response.status_code == 200:
        ticket = response.json()["ticket"]
        """
        the relevant data:
            id, subject, description, priority, status, time created, requester_id,
            submitter_id, organization_id
        """
        # prettify
        ticket = prettify_ticket(ticket)

        org_response = requests.get(
            f"{main_url}organizations/{ticket['organization_id']}.json",
            auth=(f"{API_EMAIL}/token", API_TOKEN),
        )
        org = None
        if org_response.status_code == 200:
            print(org_response.json())
            org = org_response.json()["organization"]["name"]
        req_response = requests.get(
            f"{main_url}users/{ticket['requester_id']}.json",
            auth=(f"{API_EMAIL}/token", API_TOKEN),
        )
        req = None
        if req_response.status_code == 200:
            print(req_response.json())
            req = req_response.json()["user"]["name"]
        sub_response = requests.get(
            f"{main_url}users/{ticket['submitter_id']}.json",
            auth=(f"{API_EMAIL}/token", API_TOKEN),
        )
        sub = None
        if sub_response.status_code == 200:
            sub = sub_response.json()["user"]["name"]
        return render_template(
            "view_one.html", ticket=ticket, org=org, req=req, sub=sub
        )
    else:
        text = response.json()
        if text.get("error") == "RecordNotFound":
            return redirect(
                url_for("tickets", error="Could not find ticket with that ID")
            )
        return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
