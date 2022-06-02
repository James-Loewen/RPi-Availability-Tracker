from datetime import datetime, timezone

import requests
import pytz
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent

params = {
    "cat": ["PI4", "PIZERO"],
    "country": ["US", "UK", "CA", "DE"]
}


def get_latest_item():
    item_str = None

    try:
        headers = {"User-Agent": FakeUserAgent().random}
        res = requests.get("https://rpilocator.com/feed/", headers=headers, params=params)
        res.raise_for_status()
        # I opted to use (and install) the package lxml
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
            pub_date_EDT = dtobj.strftime('%a, %d %b %Y %H:%M:%S %p (%Z)')
            # item_str = (title, link, pub_date_EDT)
            item_str = f"Title: {title}\nLink: {link}\n{pub_date_EDT}"
        else:
            item_str = f"No current entries"

    except requests.exceptions.RequestException as err:
        print(err)

    return item_str
