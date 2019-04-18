
import requests
from bs4 import BeautifulSoup

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

def fetch_content(url, username, password, verify):
    if username and password:
        content  = requests.get(url, auth=(username, password), verify=verify)
    else:
        content  = requests.get(url, verify=verify)
    return content
