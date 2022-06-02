#!/usr/bin/env python3

from time import sleep

from rpi_email import send_email
from rpi_request import get_latest_item

# Owner of https://rpilocator.com/ requests that
# folks don't make requests more than once per minute
wait_time = 60
item = get_latest_item()

if item != None:
    print(f"Starting item is:\nTitle: {item[0]}\nLink: {item[1]}\n{item[2]}")
else:
    print(f"Starting item is:\nTitle: None\nLink: None")

sleep(60)

while True:
    new_item = get_latest_item()

    if new_item == item or new_item == None:
        sleep(wait_time)
    else:
        item = new_item
        send_email(item[0], f"{item[2]}\n{item[1]}")
        print(f"========================================\nTitle: {item[0]}\nBody: {item[1]}\n{item[2]}")
        sleep(wait_time)
