import os
from datetime import datetime, timedelta

from rpi_request import get_latest_item

# try:
#     with open(f"{today.strftime(date_format)}.log") as log:
#         data = [line.strip() for line in log.read().split("========================================")][-1]
# except FileNotFoundError:
#     yesterday = today - timedelta(days=1)
#     with open(f"{yesterday.strftime(date_format)}.log") as log:
#         data = [line.strip() for line in log.read().split("========================================")][-1]
#
# with open(f"{today.strftime(date_format)}.log", "a") as log:
#     # log.write("========================================\nEat a whole hard-boiled egg, you fuck\nAll right, you don't actually have to...\n")
#     log.write(f"\n========================================\n{data}")

class Item():
    def __init__(self):
        result = get_latest_item()
        self.title, self.link, self.date = result

man = Item()

print(man.title)
print(man.link)
print(man.date)

# with open(os.path.join("C:\\Users\\james\\Desktop\\programming\\Python Codes\\RPi Email\\log-files", ))