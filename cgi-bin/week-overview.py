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
DOWNLOAD = os.path.join(LOGS, "download.log.csv")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SLOTS_PER_DAY = [(hour, minute) for hour in range(25) for minute in (15, 45)]

SLOTS_PER_DAY.pop(-1)

###### PING

total_count = defaultdict(lambda: 1)
total_success = defaultdict(lambda: 1)

time_count = defaultdict(lambda: [1] * len(SLOTS_PER_DAY))
time_success = defaultdict(lambda: [1] * len(SLOTS_PER_DAY))

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

######## DOWNLOAD

I_BPS = 3

download_rates = defaultdict(lambda: [[] for i in range(len(SLOTS_PER_DAY))])

with open(DOWNLOAD) as download:
    for line in download:
        data = line.split(";")
        day = data[DAY]
        bps = int(data[I_BPS])
        time = tuple(map(int, data[TIME].split(":")))
        for slot_i, slot in enumerate(SLOTS_PER_DAY):
            if slot > time:
                break
#        print(data[TIME], slot_i, slot)
        download_rates[day][slot_i].append(bps)

download_median = []

for day in DAYS:
    rates = []
    download_median.append(rates)
    for rate in download_rates[day]:
        if not rate:
            rates.append(0)
            continue
        rate.sort()
        median = rate[(len(rate) + 1) // 2]
        rates.append(median)

###### WEEK STATISTICS

week = []
uptimes = []

for day in DAYS:
    week.append(int(0.5 + total_success[day] * 100 / total_count[day]))
    uptimes.append([int(0.5 + time_success[day][i] * 100 / time_count[day][i]) for i in range(len(SLOTS_PER_DAY))])


##### OUTPUT AS JAVASCRIPT

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
  setDownloadSpeed(
{slots},
{downloadBps}
  );
/*
""".format(
  week = json.dumps(week, indent=2),
  slots = json.dumps([str(h) + (":30" if m == 45 else ":00") for h, m in SLOTS_PER_DAY], indent=2),
  uptimes = json.dumps(uptimes, indent=2),
  lastUpdate = int((datetime.datetime.now() - datetime.datetime(*lastUpdate)).total_seconds()),
  lastSuccess = int((datetime.datetime.now() - datetime.datetime(*lastSuccess)).total_seconds()),
  lastUpdateStatus = lastUpdateStatus,
  downloadBps = json.dumps(download_median, indent=2)
))

print("SLOTS_PER_DAY: ", SLOTS_PER_DAY)

print("*/")
