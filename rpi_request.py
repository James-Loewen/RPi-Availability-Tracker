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


def get_latest_item():
    item_str = None

    try:
        ua = UserAgent()
        # One of the available user-agents may not have worked...
        # headers = {"User-Agent": ua.random}
        headers = {"User-Agent": ua.ff} # We'll try just using FireFox U-As
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
            pub_date_EDT = dtobj.strftime('%a, %d %b %Y %I:%M:%S %p (%Z)')
            # item_str = (title, link, pub_date_EDT)
            item_str = f"Title: {title}\nLink: {link}\n{pub_date_EDT}"
        else:
            item_str = f"No current entries"

    except requests.exceptions.RequestException as err:
        err_time_UTC = datetime.now(timezone.utc)
        err_time_EDT = err_time_UTC.astimezone(pytz.timezone("US/Eastern"))
        err_time = err_time_EDT.strftime("%a, %d %b %Y %I:%M:%S %p (%Z)")
        print(f"========================================\n{err}\n{err_time}")

    return item_str
