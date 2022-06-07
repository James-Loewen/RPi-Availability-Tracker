#!/usr/bin/env python3
import os
from datetime import datetime, timedelta

from send_email import send_email
from rpi_request import get_latest_item

date_format = "%Y-%m-%d"
today = datetime.now()

try:
    with open(f"{today.strftime(date_format)}.log") as log:
        data = [line.strip() for line in log.read().split("========================================")][-1]
except FileNotFoundError:
    yesterday = today - timedelta(days=1)
    with open(f"{yesterday.strftime(date_format)}.log") as log:
        data = [line.strip() for line in log.read().split("========================================")][-1]

with open(f"{today.strftime(date_format)}.log", "a") as log:
    # log.write("========================================\nEat a whole hard-boiled egg, you fuck\nAll right, you don't actually have to...\n")
    log.write(f"\n========================================\n{data}")

# item = get_latest_item()
# print(item)
# sleep(wait_time)
#
# while True:
#     new_item = get_latest_item()
#
#     if new_item == item or new_item == None:
#         sleep(wait_time)
#     else:
#         item = new_item
#         send_email("RPi Stock Update", item)
#         print(f"========================================\n{item}")
#         sleep(wait_time)
