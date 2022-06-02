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
    item_obj = None

    try:
        headers = {"User-Agent": FakeUserAgent().random}

        res = requests.get("https://rpilocator.com/feed/", headers=headers, params=params)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'xml')

        if soup.channel.item:
            title = soup.channel.item.title.text
            link = soup.channel.item.link.text
            pub_date_GMT = soup.channel.item.pubDate.text
            dtobj = datetime.strptime(pub_date_GMT, '%a, %d %b %Y %H:%M:%S %Z')
            dtobj = dtobj.replace(tzinfo=timezone.utc)
            dtobj = dtobj.astimezone(pytz.timezone("US/Eastern"))
            pub_date_EDT = dtobj.strftime('%a, %d %b %Y %H:%M:%S %p (%Z)')

            item_obj = (title, link, pub_date_EDT)

    except requests.exceptions.RequestException as err:
        print(f"========================================\n{err}")

    return item_obj

