#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import PyRSS2Gen
import datetime

app = Flask(__name__)

def get_entries(url, verify):
    content  = requests.get(url, verify=verify)
    soup = BeautifulSoup(content.text, "lxml")
    rows = soup.find_all("tr")
    entries = []
    if rows:
        # Apache
        for row in rows[3:-1]:
            if row.find_all("a")[0]['href'].endswith("/"):
                entries.extend(get_entries(url + ("" if url.endswith("/") else "/") + row.find_all("a")[0]['href'], verify))
            else:
                entries.append(PyRSS2Gen.RSSItem(
                    title = row.find_all("a")[0].text,
                    link = url + ("" if url.endswith("/") else "/") + row.find_all("a")[0]['href'],
                    guid = PyRSS2Gen.Guid(row.find_all("a")[0].text),
                    pubDate = datetime.datetime.strptime(row.find_all("td")[2].text.strip(), "%Y-%m-%d %H:%M")))
    else:
        # Nginx
        rows = soup.find_all("a")
        if rows[0]['href'] == "../":
            rows = rows[1:]
        for row in rows:
            if row['href'].endswith("/"):
                entries.extend(get_entries(url + ("" if url.endswith("/") else "/") + row['href'], verify))
            else:
                entries.append(PyRSS2Gen.RSSItem(
                    title = row['href'],
                    link = url + ("" if url.endswith("/") else "/") + row['href'],
                    guid = PyRSS2Gen.Guid(row.text),
                    pubDate = datetime.datetime.strptime(" ".join(row.next_sibling.strip(" ").split(" ")[0:2]), "%d-%b-%Y %H:%M")))
    return entries

def fetch(url, verify):
    return PyRSS2Gen.RSS2(
            title = url,
            link = url,
            lastBuildDate = datetime.datetime.now(),
            items = get_entries(url, verify),
            description = ""
            )


@app.route('/')
def get_data():
    url = request.args.get("url")
    noverify = request.args.get("noverify")
    if url:
        return fetch(url, noverify != "yes").to_xml()
    return "no url specified"


if __name__ == "__main__":

    app.run(debug=True)
