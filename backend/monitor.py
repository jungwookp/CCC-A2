import requests
from threading import Thread
import enum

class ServerState(enum.Enum):
    Running = enum.auto()
    Crashed = enum.auto()
    Busy = enum.auto()


class Monitor:

    config_addr: str  # addr of config database
    def __init__(self, config_addr) -> None:
        self.config_addr = config_addr

    def check_state(self, doc, now):
        server = doc["server"]
        pass
    
    def start():
        pass

