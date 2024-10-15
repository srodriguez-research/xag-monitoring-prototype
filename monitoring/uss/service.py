import json
import logging
import os
import subprocess
from pathlib import Path

from prometheus_client import Counter

from uss.behave import *
from uss.tempo import get_trace, search_tempo

REPORTS_DIR = os.environ["REPORTS_DIR"]

counters = {
    "passed": Counter("passed", "Scenarios Passed"),
    "failed": Counter("failed", "Scenarios Failed"),
    "skipped": Counter("skipped", "Scenarios Skipped"),
}


def verify_trace(trace_file, report_file):
    extras = f"-f json -o {report_file}"
    command = f"behave {extras} -D trace={trace_file}"
    workdir = os.getcwd()
    logging.debug(f"Running behave as subprocess [{command=}, {workdir=}")

    result = subprocess.run(
        command.split(),
        cwd=workdir,
        capture_output=True,  # Python >= 3.7 only
        text=True,  # Python >= 3.7 only
        check=False,
    )
    return result


def log_stats(report_file):
    report = parse_behave_report(report_file)
    scenarios = find_scenarios(report)
    count = count_scenarios_by_status(scenarios)
    for status in count:
        counters[status].inc(count[status])


def monitor_traces():
    TRACES_DIR = os.environ["TRACES_DIR"]
    SERVICE_NAME = os.environ["SERVICE_NAME"]
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)
    store_dir = Path(TRACES_DIR)
    store_dir.mkdir(parents=True, exist_ok=True)
    xag_process = "PLAN_META_RATING"
    traceql = (
        "{"
        + f'resource.service.name="{SERVICE_NAME}"'
        + "&&"
        + f'name="{xag_process}"'
        + "}"
    )
    search = search_tempo(traceql)
    traces = search["traces"]
    for trace in traces:
        trace_id = trace["traceID"]
        trace_store_path = Path(os.path.join(store_dir, trace_id))
        trace_report_path = Path(os.path.join(REPORTS_DIR, f"{trace_id }-report.json"))
        if not trace_store_path.exists():
            logging.debug(f"getting trace {trace_id}")
            with open(trace_store_path, "w") as fp:
                json.dump(get_trace(trace_id), fp)
                fp.close()

            verify_trace(trace_file=trace_store_path, report_file=trace_report_path)
            # log_stats(report_file=trace_report_path)
