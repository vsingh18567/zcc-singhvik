import os
from unittest import TestCase, main, mock

import flask_unittest
from flask_testing import TestCase as FTestCase

from app import DEFAULT_URL, MAIN_URL, create_app
from utils import *


class TestUtils(TestCase):
    def test_good_request(self):
        self.assertEqual(make_request(DEFAULT_URL).status_code, 200)

    def test_prettify(self):
        ticket = {
            "created_at": "2021-11-21T17:14:21Z",
            "status": "open",
            "priority": None,
        }
        pretty = prettify_ticket(ticket)
        self.assertEqual(pretty["created_at"], "2021/11/21")
        self.assertEqual(pretty["status"], "Open")
        self.assertEqual(pretty["priority"], "None")

    def test_good_verify(self):
        url = f"{MAIN_URL}users/1903513328187.json"
        self.assertEqual(verify_response(url, "user"), "The Customer")

    def test_bad_verify(self):
        url = f"{MAIN_URL}users/111111111111.json"
        self.assertEqual(verify_response(url, "user"), None)


class TestTemplates(FTestCase):
    def create_app(self):
        return create_app()

    def test_view_all(self):
        r = self.client.get("/")
        self.assert200(r)
        self.assert_template_used("view_all.html")
        self.assertContext("prev_link", None)
        self.assertContext("page", 1)
        self.assertEqual(len(self.get_context_variable("ticket_data")), 25)

    def test_bad_request_url(self):
        r = self.client.get(
            "/?request_url=https%3A%2F%2Fzccsinghvik.zendesk.co%2Fapi%2Fv2%2Ftickets.json%3Fpage%255Bafter%255D%3DeyJvIjoibmljZV9pZCIsInYiOiJhUmtBQUFBQUFBQUEifQ%253D%253D%26page%255Bsize%255D%3D25&page_num=2"
        )
        # there is an error in the request url (its .co instead of .com), but it should redirect to the default url
        self.assert200(r)
        self.assertContext("page", 1)

    def test_get_ticket(self):
        r = self.client.get("/ticket/1")
        self.assert200(r)
        self.assert_template_used("view_one.html")
        t = self.get_context_variable("ticket")
        self.assertEqual(t["id"], 1)

    def test_bad_ticket(self):
        r = self.client.get("/ticket/1000")
        # should redirect
        self.assertStatus(r, 302)


class TestResponses(flask_unittest.ClientTestCase):
    """
    Test that we redirect to error.html with a 404 status code when auth is bad
    """

    app = create_app()

    @mock.patch("utils.API_TOKEN", "bad")
    def test_bad_auth(self, client):
        r = client.get("/")
        self.assertStatus(r, 404)

    @mock.patch("utils.API_TOKEN", "bad")
    def test_bad_auth2(self, client):
        r = client.get("/tickets/1")
        self.assertStatus(r, 404)


if __name__ == "__main__":
    main()
