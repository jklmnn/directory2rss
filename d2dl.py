#!/usr/bin/env python3

import sys
import argparse
import os
import re
import d2

def get_entries(content, match):
    soup = BeautifulSoup(content, "lxml")
    rows = soup.find_all("tr")
    if rows:
        # Apache
        return filter(lambda entry: entry != '/' or match.search(entry) if match else entry != '/',
                [row.find_all("a")[0]['href'] for row in rows[3:-1]])
    else:
        # Nginx
        rows = soup.find_all("a")
        if rows[0]['href'] == "../":
            rows = rows[1:]
        return [r['href'] for r in rows]

def fetch(url, username, password, verify, match):
    content = d2.fetch_content(url, username, password, verify)
    return [entry if entry.startswith("http") else url + ("" if url.endswith("/") else "/") + entry for entry in get_entries(content.text, match)]

def run(url, username, password, verify, recursive, quotes, curl, match):
    for link in fetch(url, username, password, verify, match):
        quote = "\"" if quotes else ""
        print(quote + link + quote)
        if recursive and link.endswith("/"):
            run(link, username, password, verify, recursive, quotes, curl, match)
        elif curl:
            os.system("curl {}{}-O {}".format("-k " if not verify else "",
                "-u \"{}:{}\" ".format(username, password) if username and password else "",link))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help="url")
    parser.add_argument('--username', '-u', help="usernamw")
    parser.add_argument('--password', '-p', help="password")
    parser.add_argument('--recursive', '-r', action='store_true', help="recursive")
    parser.add_argument('--noverify', '-n', action='store_true', help="do not verify https certificates")
    parser.add_argument('--quote', '-q', action='store_true', help="enquote links in \"\" for shell processing")
    parser.add_argument('--curl', '-c', action='store_true', help="download file with curl")
    parser.add_argument('--match', '-m', help="only show results matching the regex string (python regex)")
    return parser.parse_args(sys.argv[1:])

if __name__ == "__main__":

    args = get_args()

    username = args.username
    password = args.password
    url = args.url

    run(
            args.url,
            args.username,
            args.password,
            not args.noverify,
            args.recursive,
            args.quote,
            args.curl,
            re.compile(args.match) if args.match else None
            )
