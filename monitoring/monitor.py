import coloredlogs
from prometheus_client import start_http_server

from uss.service import monitor_traces

coloredlogs.install(level="DEBUG")
import time

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        monitor_traces()
        time.sleep(1)
