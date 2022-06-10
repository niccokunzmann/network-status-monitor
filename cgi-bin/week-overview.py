#!/usr/bin/python3
import os
import sys
from collections import defaultdict
import json

print("Content-Type: text/javascript")
print("")
print("")

HERE = os.path.dirname(sys.argv[0])
LOGS = os.path.join(HERE, "..", "bin", "logs")
PING = os.path.join(LOGS, "ping.log.csv")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

total_count = defaultdict(lambda: 1)
total_success = defaultdict(lambda: 1)

days = [""]
DAY = 0
SUCCESS = 4

with open(PING) as ping:
    for line in ping:
        data = line.split(";")
        day = data[DAY]
        success = data[SUCCESS]
        total_count[day] += 1
        if int(success):
            total_success[day] += 1

result = []

for day in DAYS:
    result.append(int(total_success[day] * 100 / total_count[day]))

print("""

window.addEventListener("load", function() {{
  showWeekOverview(
{week}
  );
}});

""".format(week=json.dumps(result, indent=2)))
