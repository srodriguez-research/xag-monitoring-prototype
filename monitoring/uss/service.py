import json
import logging
import os
import subprocess
from pathlib import Path

from uss.tempo import get_trace, search_tempo

SERVICE_NAME = os.environ["SERVICE_NAME"]


def verify_trace(trace_file):
    command = f"behave --no-capture -D trace={trace_file}"
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


def monitor_traces():
    store_dir = Path(os.environ("TRACES_DIR"))
    store_dir.mkdir(parents=True, exist_ok=True)
    traceql = "{" + f'resource.service.name="{SERVICE_NAME}"' + "}"
    search = search_tempo(traceql)
    traces = search["traces"]
    for trace in traces:
        trace_id = trace["traceID"]
        trace_store_path = Path(os.path.join(store_dir, trace_id))
        if not trace_store_path.exists():
            logging.debug(f"getting trace {trace_id}")
            with open(trace_store_path, "w") as fp:
                json.dump(get_trace(trace_id), fp)
                fp.close()

            verify_trace(trace_store_path)
