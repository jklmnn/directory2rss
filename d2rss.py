#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import PyRSS2Gen
import datetime

app = Flask(__name__)

def get_entries(content):
    soup = BeautifulSoup(content, "lxml")
    rows = soup.find_all("tr")
    return [PyRSS2Gen.RSSItem(
        title = row.find_all("a")[0].text,
        link = row.find_all("a")[0]['href'],
        guid = PyRSS2Gen.Guid(row.find_all("a")[0].text),
        pubDate = datetime.datetime.strptime(row.find_all("td")[2].text.strip(), "%Y-%m-%d %H:%M")
        ) for row in rows[2:-1]]

def fetch(url, username, password):
    if username and password:
        content  = requests.get(url, auth=(username, password), verify=False)
    else:
        content  = requests.get(url, verify=False)
    print(content.headers)

    return PyRSS2Gen.RSS2(
            title = url,
            link = url,
            lastBuildDate = datetime.datetime.now(),
            items = get_entries(content.text),
            description = ""
            )


@app.route('/')
def get_data():
    url = request.args.get("url")
    username = request.args.get("user")
    password = request.args.get("pass")
    if url:
        return fetch(url, username, password).to_xml()
    return "no url specified"


if __name__ == "__main__":

    app.run(debug=True)