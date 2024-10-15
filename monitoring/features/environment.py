import json
import logging

import logging_loki
from behave.model import Scenario, Status
from behave.runner import Context

from uss.loki import build_tags
from uss.tempo import parse_trace_json


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

    logging.debug(f"behave trace {trace_file} parsing complete")
    context.trace = trace
    context.trace_id = context.trace["traceId"]
    context.explainer_url = f"http://localhost:5000/{context.trace_id}"

    logger.debug(f"Starting verification of traceId={trace['traceId']}")
    context.logger = logger


def before_feature(context, feature):
    pass


def before_scenario(context, scenario: Scenario):
    context.given_applies = True
    context.xag_process = "TBC"
    context.span = None
    scenario.failed_message = None

    # Find the correct process to verify this scenario
    if any(t for t in scenario.tags if t == "goal-plan"):
        context.xag_process = "PLAN_RATING"

    if any(t for t in scenario.tags if t == "goal-plan-preference"):
        context.xag_process = "PLAN_META_RATING"

    # Check if this scenario was used in the decision
    find_span(context, scenario)

    if context.span is None:
        scenario.skip(
            f"Scenario {scenario.name} not listed in decision criteria of any span in the trace"
        )
        return

    context.logger.debug(f"Starting verification of trace")


# set the current step to log it later as part of the tags
def before_step(context, step):
    context.step = step


def build_context_tags(context: Context) -> dict:
    context_tags = {
        "feature": context.feature.name,
        "scenario": context.scenario.name,
        "feature_status": context.feature.status.name.upper(),
        "scenario_status": context.scenario.status.name.upper(),
        # "traceId": context.trace["traceId"],  # Not sure this is the best way to link
        # "spanId": context.span["spanId"],  # Not sure this is the best way to link
    }
    return build_tags(context_tags)


def after_scenario(context, scenario):
    infomsg = f"story={context.feature.name} scenario={context.scenario.name} for traceId={context.trace["traceId"]} in spanId={context.span["spanId"]}"
    explainmsg = f"Explanation: {context.explainer_url}"

    match scenario.status:
        case Status.failed:
            msg = f"FAILED verification {infomsg}"
            msg = f"{msg}\n Reason: {scenario.failed_message}"
            msg = f"{msg}\n {explainmsg}"
            context.logger.critical(
                msg,
                extra=build_context_tags(context),
            )

        case _:
            msg = f"{scenario.status.name.upper()} verification {infomsg}"
            msg = f"{msg}\n {explainmsg}"
            context.logger.info(
                msg,
                extra=build_context_tags(context),
            )


def find_span(context: Context, scenario: Scenario):
    all_spans = context.trace["spans"]
    scenario_name = scenario.name.split("-- @", 1)[0].strip()
    found = list(
        filter(
            lambda x: x["name"] == context.xag_process
            and scenario_name in x["xag.process.criteria.id"],
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
