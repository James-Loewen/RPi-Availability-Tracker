#!/usr/bin/env python3
import os.path
from datetime import datetime, timedelta

from send_email import send_email
from rpi_request import Item

date_format = "%Y-%m-%d"
today = datetime.now()

try:
    os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), "log-files"))
except FileExistsError:
    pass
finally:
    log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "log-files")

try:
    with open(os.path.join(log_path, f"{today.strftime(date_format)}.log")) as log:
        last_item = [line.strip() for line in log.read().split("="*40)][-1].strip()
except FileNotFoundError:
    try:
        yesterday = today - timedelta(days=1)
        with open(os.path.join(log_path, f"{yesterday.strftime(date_format)}.log")) as log:
            last_item = [line.strip() for line in log.read().split("="*40)][-1].strip()
    except FileNotFoundError:
        last_item = ['']

new_item = Item()

if new_item.title is not None and f"{new_item.title}\n{new_item.link}\n{new_item.date}" != last_item:
    with open(os.path.join(log_path, f"{today.strftime(date_format)}.log"), "a") as log:
        if log.tell() == 0:
            log.write(f"{new_item.title}\n{new_item.link}\n{new_item.date}\n")
        else:
            log.write(f"{'='*40}\n{new_item.title}\n{new_item.link}\n{new_item.date}\n")
    send_email(new_item.title, f"{new_item.link}\n{new_item.date}")
