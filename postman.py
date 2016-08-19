#!/usr/bin/env python
# encoding: utf-8

import urlparse
import argparse

import requests


class Postman(object):
    base_url = "https://kindle4rss.com"
    login_url = urlparse.urljoin(base_url, "/login/")
    send_url = urlparse.urljoin(base_url, "/send_now/")

    def __init__(self):
        self.session = requests.session()

    def login(self, username, password):
        response = self.session.post(
            self.login_url, {
                "email_address": username,
                "password": password,
            },
            verify=False,
        )
        return response.find(username) >= 0

    def send_to_kindle(self):
        for i in range(3):  # retry for 3 times
            try:
                response = self.session.post(self.send_url)
                if response.status_code == 200:
                    break
            except requests.HTTPError:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("u", "username", help="login email")
    parser.add_argument("p", "password", help="login password")

    args = parser.parse_args()

    postman = Postman()
    if postman.login(args.username, args.password):
        postman.send_to_kindle()

