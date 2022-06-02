#!/usr/bin/env python3

from time import sleep

from send_email import send_email
from rpi_request import get_latest_item

# Owner of https://rpilocator.com/ requests that
# folks don't make requests more than once per minute
wait_time = 60
item = get_latest_item()
print(item)
sleep(wait_time)

while True:
    new_item = get_latest_item()

    if new_item == item or new_item == None:
        sleep(wait_time)
    else:
        item = new_item
        send_email("RPi Stock Update", item)
        print(f"========================================\n{item}")
        sleep(wait_time)
