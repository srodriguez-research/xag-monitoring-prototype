import logging
from pathlib import Path

import coloredlogs

from uss.service import verify_trace

coloredlogs.install(level="DEBUG")
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Verify Trace",
        description="Verifies a single tracefile",
    )
    parser.add_argument("trace_filename")
    args = parser.parse_args()
    trace_file = args.trace_filename
    tracename = Path(trace_file).name
    verify_trace(trace_file, f"data/reports/{tracename}-report.json")
