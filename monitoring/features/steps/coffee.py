import json

from behave import *  # pylint: disable=wildcard-import
from behave.runner import Context

from features.environment import pprint
from uss.loki import build_tags
from uss.tempo import array_to_dict_by


def build_context_tags(context: Context) -> dict:
    context_tags = {
        "feature": context.feature.name,
        "scenario": context.scenario.name,
        "step": context.step.name,
        "traceId": context.trace["traceId"],  # Not sure this is the best way to link
        "spanId": context.span["spanId"],  # Not sure this is the best way to link
    }
    return build_tags(context_tags)


@given("I believe {belief} is {value}")
def step_impl(context, belief, value):
    value = bool(value)

    if "goal-plan" in context.scenario.tags:
        span = context.span
        belief2find = f"xag.query.{belief}"

        #  Has this rating considered
        context.given_applies = (belief2find in span) and context.given_applies
        if context.given_applies:
            spanBel = span[belief2find]
            context.given_applies = (spanBel == value) and context.given_applies

    else:
        assert None == "Should not be here!!"


@then("plan {plan} is applicable")
def step_impl(context: Context, plan):

    # Check if the plan in not the applicablePlans
    # then the engine FAILED to comply to requirements
    if not context.given_applies:
        context.scenario.skip("Given conditions do not apply")
        return

    result = json.loads(context.span["xag.actions.call.return"])
    # Anything above 0 is a potentially applicable plan
    rating = result["rating"]
    failed_msg = f"Failed to verify story={context.feature.name} scenario={context.scenario.name} for traceId={context.trace["traceId"]} in spanId={context.span["spanId"]}"
    pprint(result)
    if rating <= 0:
        context.logger.critical(
            failed_msg,
            extra=build_context_tags(context),
        )
    assert rating > 0, failed_msg


@when("I adopt the {goal} goal")
def step_impl(context, goal):
    pass


@when("I evaluate current_goal success")
def step_impl(context):
    pass


@then("goal success is true")
def step_impl(context):
    pass
