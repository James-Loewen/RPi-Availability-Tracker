import os.path
from datetime import datetime, timezone

import requests
import pytz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

params = {
    # options: ["CM4", "PI3", "PI4", "PIZERO"]
    "cat": ["PIZERO"],
    # options: AT, BE, CA, CN, FR, DE, IT, JP, NL,
    #          PL, PT, ZA, ES, SE, CH, UK, US
    "country": ["US", "CA"]
}


def handle_error(err):
    err_date = datetime.now()
    with open(os.path.join("C:\\Users\\james\\Desktop\\programming\\Python Codes\\RPi Email\\error-files",
                           f"{err_date.strftime('%Y-%m-%d')}.error"), "a") as err_file:
        err_file.write(f"========================================\n{err}\n{err_date.strftime('%I:%M:%S %p')}")


def get_latest_item():
    title = None
    link = None
    pub_date_EDT = None

    try:
        ua = UserAgent()
        # One of the available user-agents may not have worked...
        # headers = {"User-Agent": ua.random}
        headers = {"User-Agent": ua.ff}  # We'll try just using FireFox U-As
        # res = requests.get("https://rpilocator.com/feed/", headers=headers, params=params)
        res = requests.get("https://rpilocator.com/feed/", headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'xml')

        if soup.channel.item:
            title = soup.channel.item.title.text
            link = soup.channel.item.link.text
            # This formatting was an after-thought...
            # I might make this its own module
            pub_date_GMT = soup.channel.item.pubDate.text
            dtobj = datetime.strptime(pub_date_GMT, '%a, %d %b %Y %H:%M:%S %Z')
            dtobj = dtobj.replace(tzinfo=timezone.utc)
            dtobj = dtobj.astimezone(pytz.timezone("US/Eastern"))
            pub_date_EDT = dtobj.strftime('%a, %d %b %Y %I:%M:%S %p (%Z)')
            # return title, link, pub_date_EDT

    except requests.exceptions.RequestException as err:
        handle_error(err)

    return title, link, pub_date_EDT


class Item():
    def __init__(self):
        result = get_latest_item()
        self.title, self.link, self.date = result

