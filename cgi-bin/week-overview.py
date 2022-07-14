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
NETWORK = os.path.join(LOGS, "network.log.csv")
TODAY = "today"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", TODAY]
SLOTS_PER_DAY = [(hour, minute) for hour in range(25) for minute in (15, 45)]

SLOTS_PER_DAY.pop(-1)
TODAY_DT = datetime.date.today()
today = (TODAY_DT.year, TODAY_DT.month, TODAY_DT.day)

###### PING


# day: count
total_count = defaultdict(lambda: 0)
total_success = defaultdict(lambda: 0)

# day: slot: count
time_count = defaultdict(lambda: [0] * len(SLOTS_PER_DAY))
time_success = defaultdict(lambda: [0] * len(SLOTS_PER_DAY))

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
        if date == today:
            total_count[TODAY] += 1
            time_count[TODAY][slot_i] += 1
        if int(success):
            total_success[day] += 1
            time_success[day][slot_i] += 1
            if date == today:
                total_success[TODAY] += 1
                time_success[TODAY][slot_i] += 1
            if dt > lastSuccess:
                lastSuccess = dt

######## DOWNLOAD

I_BPS = 3


def median(l):
    """Return the Median of the list with at least one element."""
    l = l[:]
    l.sort()
    median = l[(len(l) + 1) // 2]
    return median



def getSlots(path, index, crunch):
    """Get the slot value from the value at index.
    crunch the data list with median or max or average ...
    """
    download_rates = defaultdict(lambda: [[] for i in range(len(SLOTS_PER_DAY))])

    with open(path) as download:
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
                rates.append(None)
                continue
            rates.append(crunch(rate))

    return download_median

download_median = getSlots(DOWNLOAD, I_BPS, median)

###### People in the network

people = getSlots(NETWORK, 3, max)

###### WEEK STATISTICS

week = []
uptimes = []

for day in DAYS:
    week.append(None if total_count[day] == 0 else int(0.5 + total_success[day] * 100 / total_count[day]))
    uptimes.append([
        (None if time_count[day][i] == 0 else int(0.5 + time_success[day][i] * 100 / time_count[day][i]))
        for i in range(len(SLOTS_PER_DAY))
    ])

current = week[7:]
current_uptimes = uptimes[7:]

today_total = current[0]
today_uptime = current_uptimes[0]

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
  setDevices(
{slots},
{people}
  );
  setTodayUptime(
{slots},
{today_uptime},
{today_total}
  );
/*
""".format(
  today_total = json.dumps(today_total),
  today_uptime = json.dumps(today_uptime),
  week = json.dumps(week, indent=2),
  slots = json.dumps([str(h) + (":30" if m == 45 else ":00") for h, m in SLOTS_PER_DAY], indent=2),
  uptimes = json.dumps(uptimes, indent=2),
  lastUpdate = int((datetime.datetime.now() - datetime.datetime(*lastUpdate)).total_seconds()),
  lastSuccess = int((datetime.datetime.now() - datetime.datetime(*lastSuccess)).total_seconds()),
  lastUpdateStatus = lastUpdateStatus,
  downloadBps = json.dumps(download_median, indent=2),
  people = json.dumps(people, indent=2),
))

print("SLOTS_PER_DAY: ", SLOTS_PER_DAY)

print("*/")
