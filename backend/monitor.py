import requests
import enum
import time
import datetime

from util import log

class ServerState(enum.Enum):
    Running = enum.auto()
    Crashed = enum.auto()
    Busy = enum.auto()


CONFIG_DB_ADDR = ""


def checkstates():
    t = datetime.datetime.now()
    res = requests.get(f"{CONFIG_DB_ADDR}/_all_docs")
    config_files = [doc for doc in res["rows"] if doc['server']['type'] != "monitor"]

    crashed = []

    for doc in config_files:
        if not doc["server"]["running"]:
            continue
        ts = datetime.datetime.fromisoformat(doc["server"]["last_sync"])
        secs = (t - ts).total_seconds()  
        if secs > 2 * int(doc["server"]["heartbeat_period"]):
            crashed.append(doc)
    return crashed


def restart():
    pass


def run(sec: int):
    while True:
        time.sleep(sec)
        crashed_uis = checkstates()
        if crashed_uis:
            log("Crashed: " + ",".join([doc["_id"] for doc in crashed_uis]))
            restart(crashed_uis)
