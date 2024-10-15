import json
import logging

import logging_loki
from behave.model import Scenario
from behave.runner import Context

from uss.tempo import array_to_dict_by, parse_trace_json


def get_logger():
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
    return logger


def before_all(context):
    logger = get_logger()

    # Get the trace to verify from cli
    trace_file = context.config.userdata["trace"]
    logging.debug(f"behave starting verification of trace {trace_file}")
    if trace_file == None:
        raise Exception("Must provide a trace to parse ")
    trace = parse_trace_json(trace_file)
    # print("#########################################")
    # pprint(trace)
    # print("#########################################")

    logging.debug(f"behave trace {trace_file} parsing complete")
    context.trace = trace

    logger.info(f"Starting verification of traceId={trace['traceId']}")
    context.logger = logger


def before_feature(context, feature):
    context.logger.info(f"Starting verification of trace")


def before_scenario(context, scenario: Scenario):
    context.given_applies = True
    context.xag_process = "TBC"
    context.span = None

    # Find the correct process to verify this scenario
    if any(t for t in scenario.tags if t == "goal-plan"):
        context.xag_process = "PLAN_RATING"

    # Check if this scenario was used in the decision
    find_span(context, scenario)

    if context.span is None:
        scenario.skip(
            f"Scenario {scenario.name} not listed in decision criteria of any span in the trace"
        )
        return

    context.logger.info(f"Starting verification of trace")


# set the current step to log it later as part of the tags
def before_step(context, step):
    context.step = step


def find_span(context: Context, scenario: Scenario):
    all_spans = context.trace["spans"]
    found = list(
        filter(
            lambda x: x["name"] == context.xag_process
            and scenario.name in x["xag.process.criteria.id"],
            all_spans,
        )
    )
    # print("###################################")
    # print(f"Found for {scenario.name}")
    # pprint(found)

    if len(found) == 1:
        context.span = found[0]


def pprint(d):
    print(json.dumps(d, indent=2))
