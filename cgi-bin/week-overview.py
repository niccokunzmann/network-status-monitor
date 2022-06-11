#!/usr/bin/python3
import os
import sys
from collections import defaultdict
import json
import datetime

print("Content-Type: text/javascript")
print("")
print("")

HERE = os.path.dirname(sys.argv[0])
LOGS = os.path.join(HERE, "..", "bin", "logs")
PING = os.path.join(LOGS, "ping.log.csv")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SLOTS_PER_DAY = [(hour, minute) for hour in range(25) for minute in (15, 45)]

SLOTS_PER_DAY.pop(-1)

total_count = defaultdict(lambda: 1)
total_success = defaultdict(lambda: 1)

time_count = defaultdict(lambda: [1] * len(SLOTS_PER_DAY))
time_success = defaultdict(lambda: [1] * len(SLOTS_PER_DAY))

days = [""]
DAY = 0
DATE = 1
TIME = 2
SUCCESS = 4

lastUpdate = (0,0)
lastUpdateStatus = 2

lastSuccess = (0,0)

with open(PING) as ping:
    for line in ping:
        data = line.split(";")
        day = data[DAY]
        success = data[SUCCESS]
        time = tuple(map(int, data[TIME].split(":")))
        date = tuple(map(int, data[DATE].split("-")))
        dt = date + time
        if dt > lastUpdate:
            lastUpdate = dt
            lastUpdateStatus = int(success)
        for slot_i, slot in enumerate(SLOTS_PER_DAY):
            if slot > time:
                break
#        print(data[TIME], slot_i, slot)
        total_count[day] += 1
        time_count[day][slot_i] += 1
        if int(success):
            total_success[day] += 1
            time_success[day][slot_i] += 1
            if dt > lastSuccess:
                lastSuccess = dt
week = []
uptimes = []

for day in DAYS:
    week.append(int(0.5 + total_success[day] * 100 / total_count[day]))
    uptimes.append([int(0.5 + time_success[day][i] * 100 / time_count[day][i]) for i in range(len(SLOTS_PER_DAY))])

print("""

window.addEventListener("load", function() {{
  showWeekOverview(
{week}
  );
  showDays(
{slots},
{uptimes}
);
  setCurrentStatus({lastSuccess}, {lastUpdateStatus}, {lastUpdate});
}});
/*
""".format(
  week = json.dumps(week, indent=2),
  slots = json.dumps([str(h) + (":30" if m == 45 else ":00") for h, m in SLOTS_PER_DAY], indent=2),
  uptimes = json.dumps(uptimes, indent=2),
  lastUpdate = int((datetime.datetime.now() - datetime.datetime(*lastUpdate)).total_seconds()),
  lastSuccess = int((datetime.datetime.now() - datetime.datetime(*lastSuccess)).total_seconds()),
  lastUpdateStatus = lastUpdateStatus
))

print("SLOTS_PER_DAY: ", SLOTS_PER_DAY)

print("*/")
