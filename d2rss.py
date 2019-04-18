#!/usr/bin/env python3

from bs4 import BeautifulSoup
from flask import Flask, request
import PyRSS2Gen
import datetime
import d2

app = Flask(__name__)

def get_entries(url, username, password):
    content = d2.fetch_content(url, username, password, False)
    soup = BeautifulSoup(content.text, "lxml")
    rows = soup.find_all("tr")
    entries = []
    if rows:
        # Apache
        for row in rows[3:-1]:
            if row.find_all("a")[0]['href'].endswith("/"):
                entries.extend(get_entries(url + ("" if url.endswith("/") else "/") + row.find_all("a")[0]['href'], username, password))
            else:
                entries.append(PyRSS2Gen.RSSItem(
                    title = row.find_all("a")[0].text,
                    link = row.find_all("a")[0]['href'],
                    guid = PyRSS2Gen.Guid(row.find_all("a")[0].text),
                    pubDate = datetime.datetime.strptime(row.find_all("td")[2].text.strip(), "%Y-%m-%d %H:%M")))
    else:
        # Nginx
        rows = soup.find_all("a")
        if rows[0]['href'] == "../":
            rows = rows[1:]
        for row in rows:
            if row['href'].endswith("/"):
                entries.extend(get_entries(url + ("" if url.endswith("/") else "/") + row['href'], username, password))
            else:
                entries.append(PyRSS2Gen.RSSItem(
                    title = row.text,
                    link = row['href'],
                    guid = PyRSS2Gen.Guid(row.text),
                    pubDate = datetime.datetime.strptime(" ".join(row.next_sibling.strip(" ").split(" ")[0:2]), "%d-%b-%Y %H:%M")))
    return entries

def fetch(url, username, password):
    return PyRSS2Gen.RSS2(
            title = url,
            link = url,
            lastBuildDate = datetime.datetime.now(),
            items = get_entries(url, username, password),
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
