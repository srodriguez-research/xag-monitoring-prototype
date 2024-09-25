import logging

import coloredlogs

from uss.service import monitor_traces

coloredlogs.install(level="DEBUG")
import time

if __name__ == "__main__":
    while True:
        monitor_traces()
        time.sleep(1)
