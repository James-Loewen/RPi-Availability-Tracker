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
    try:
        os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), "error-files"))
    except FileExistsError:
        pass
    finally:
        err_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "error-files")
    err_date = datetime.now()
    with open(os.path.join(err_path, f"{err_date.strftime('%Y-%m-%d')}.error"), "a") as err_file:
        if err_file.tell() == 0:
            err_file.write(f"{err}\n{err_date.strftime('%a, %d %b %Y %I:%M:%S %p')}\n")
        else:
            err_file.write(f"{'='*40}\n{err}\n{err_date.strftime('%a, %d %b %Y %I:%M:%S %p')}\n")



def get_latest_item():
    title = None
    link = None
    pub_date_EDT = None

    try:
        ua = UserAgent()
        headers = {"User-Agent": ua.ff}
        res = requests.get("https://rpilocator.com/feed/", headers=headers, params=params)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "xml")

        if soup.channel.item:
            title = soup.channel.item.title.text
            link = soup.channel.item.link.text
            pub_date_GMT = soup.channel.item.pubDate.text
            dtobj = datetime.strptime(pub_date_GMT, "%a, %d %b %Y %H:%M:%S %Z")
            dtobj = dtobj.replace(tzinfo=timezone.utc)
            dtobj = dtobj.astimezone(pytz.timezone("US/Eastern"))
            pub_date_EDT = dtobj.strftime("%a, %d %b %Y %I:%M:%S %p (%Z)")

    except requests.exceptions.RequestException as err:
        handle_error(err)

    return title, link, pub_date_EDT


class Item:
    def __init__(self):
        result = get_latest_item()
        self.title, self.link, self.date = result
