#!/usr/bin/env python3

import sys
import argparse
import os
import re
import threading
import requests
from bs4 import BeautifulSoup

threads = []

def get_entries(content, match):
    soup = BeautifulSoup(content, "lxml")
    rows = soup.find_all("tr")
    if rows:
        # Apache
        rows = [row.find_all("a")[0]['href'] for row in rows[3:-1]]
    else:
        # Nginx
        rows = soup.find_all("a")
        if rows[0]['href'] == "../":
            rows = rows[1:]
        rows = [r['href'] for r in rows]
    return filter(lambda entry: entry.endswith('/') or (match.search(entry) if match else entry != '/'), rows)

def fetch(url, verify, recursive, quotes, curl, match, single):
    content  = requests.get(url, verify=verify)
    for link in [entry if entry.startswith("http") else url + ("" if url.endswith("/") else "/") + entry for entry in get_entries(content.text, match)]:
        quote = "\"" if quotes else ""
        if not link.endswith('/'):
            print(quote + link + quote)
        if recursive and link.endswith("/"):
            run(link, verify, recursive, quotes, curl, match, single)
        elif curl:
            os.system("curl {}-O {}".format("-k " if not verify else "", link))

def run(url, verify, recursive, quotes, curl, match, single):
    if single:
        fetch(url, verify, recursive, quotes, curl, match, single)
    else:
        thread = threading.Thread(target=fetch, args=(url, verify, recursive, quotes, curl, match, single))
        threads.append(thread)
        thread.start()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help="url")
    parser.add_argument('--recursive', '-r', action='store_true', help="recursive")
    parser.add_argument('--noverify', '-n', action='store_true', help="do not verify https certificates")
    parser.add_argument('--quote', '-q', action='store_true', help="enquote links in \"\" for shell processing")
    parser.add_argument('--curl', '-c', action='store_true', help="download file with curl")
    parser.add_argument('--match', '-m', help="only show results matching the regex string (python regex)")
    parser.add_argument('--single', '-s', action='store_true', help="run single threaded")
    return parser.parse_args(sys.argv[1:])

if __name__ == "__main__":

    args = get_args()

    url = args.url

    run(
            args.url,
            not args.noverify,
            args.recursive,
            args.quote,
            args.curl,
            re.compile(args.match) if args.match else None,
            args.single
            )
    for t in threads:
        t.join()
