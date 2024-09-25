import json
import logging
import os
import subprocess
from pathlib import Path

from uss.tempo import get_trace, search_tempo


def verify_trace(trace_file):
    cmd = f"poetry run behave --no-capture -D trace={trace_file}"
    logging.debug(f"Running behave as subprocess with commnad {cmd}")
    s = subprocess.run(cmd, check=False)
    return s


def monitor_traces():
    store_dir = Path("target/traces_store")
    store_dir.mkdir(parents=True, exist_ok=True)
    SERV_NAME = "xag-test"
    traceql = "{" + f'resource.service.name="{SERV_NAME}"' + "}"
    search = search_tempo(traceql)
    traces = search["traces"]
    for trace in traces:
        trace_id = trace["traceID"]
        trace_store_path = Path(os.path.join(store_dir, trace_id))
        if not trace_store_path.exists():
            logging.debug(f"getting trace {trace_id}")
            with open(trace_store_path, "w") as fp:
                json.dump(get_trace(trace_id), fp)
                verify_trace(trace_store_path)
