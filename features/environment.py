import logging

import logging_loki

from uss.tempo import parse_trace_json


def before_all(context):
    # Get the trace to verify from cli
    trace_file = context.config.userdata["trace"]
    if trace_file == None:
        raise Exception("Must provide a trace to parse ")
    trace = parse_trace_json(trace_file)
    context.trace = trace

    handler = logging_loki.LokiHandler(
        url="http://localhost:3100/loki/api/v1/push",
        tags={"application": "story-verification-app"},
        # auth=("username", "password"),
        version="1",
    )

    logger = logging.getLogger("story-verification-logger")
    fmt = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.info(f"Starting verification of traceId={trace['traceId']}")
    context.logger = logger


def before_each(context):
    context.logger.info(f"Starting verification of trace")


# set the current step to log it later as part of the tags
def before_step(context, step):
    context.step = step
