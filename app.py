import sys

from flask import Flask, redirect, render_template, request, url_for

from utils import *

# consts
app = Flask(__name__)
MAIN_URL = f"https://{API_DOMAIN}.zendesk.com/api/v2/"
DEFAULT_URL = f"{MAIN_URL}tickets.json?page[size]=25"


@app.route("/", methods=["GET", "POST"])
def tickets():
    """
    route for viewing all tickets
    """
    if request.method == "GET":
        request_url = request.args.get("request_url", default=DEFAULT_URL, type=str)
        page = request.args.get("page_num", default=1, type=int)
        error = request.args.get("error", default=None, type=str)

        if MAIN_URL not in request_url:
            request_url = DEFAULT_URL
            page = 1

        response = make_request(request_url)

        if response.status_code > 299:
            if request_url != DEFAULT_URL:
                # try hitting the default page
                return redirect(url_for("tickets", error="Oops something went wrong"))
            # otherwise its probably some server error
            return render_template("error.html"), 404

        data = response.json()

        next_link = None
        prev_link = data["links"]["prev"]

        if data["meta"]["has_more"]:
            next_link = data["links"]["next"]

        if page == 1:
            prev_link = None
        data["tickets"] = list(map(lambda t: prettify_ticket(t), data["tickets"]))

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
    response = make_request(f"{MAIN_URL}tickets/{id}.json")

    if response.status_code == 200:
        ticket = response.json()["ticket"]
        """
        the relevant data:
            id, subject, description, priority, status, time created, requester_id,
            submitter_id, organization_id
        """

        ticket = prettify_ticket(ticket)

        org = verify_response(
            f"{MAIN_URL}organizations/{ticket['organization_id']}.json", "organization"
        )
        req = verify_response(f"{MAIN_URL}users/{ticket['requester_id']}.json", "user")
        sub = verify_response(f"{MAIN_URL}users/{ticket['submitter_id']}.json", "user")
        return render_template(
            "view_one.html", ticket=ticket, org=org, req=req, sub=sub
        )

    else:
        try:
            text = response.json()
        except:
            return render_template("error.html")
        if text.get("error") == "RecordNotFound":
            return redirect(
                url_for("tickets", error="Could not find ticket with that ID")
            )
        return render_template("error.html")


def create_app():
    return app


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        port = 8000
    else:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = 8000
    app.run(debug=True, host="localhost", port=port)
