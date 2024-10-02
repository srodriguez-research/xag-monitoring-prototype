from behave import *  # pylint: disable=wildcard-import
from behave.runner import Context

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
    spans = array_to_dict_by(context.trace["spans"], "name")
    value = bool(value)

    if not hasattr(context, "given_applies"):
        context.given_applies = True

    if "goal-plan" in context.scenario.tags:
        span = spans["plan_revision"]
        context.span = span
        spanBel = span[f"xag.query.{belief}"]
        context.given_applies = (spanBel == value) and context.given_applies
    else:
        assert None == "Should not be here!!"


@then("plan {plan} is applicable")
def step_impl(context: Context, plan):

    # Check the pre conditions apply (given)
    # If not, we can not say it failed.
    if context.given_applies:
        # Check if the plan in not the applicablePlans
        # then the engine FAILED to comply to requirements
        if plan not in context.span[f"xag.query.applicablePlans"]:
            # print(f"{context.trace=}")
            # print(f"{context.span=}")
            context.logger.critical(
                f"Failed to verify story={context.feature.name} for traceId={context.trace["traceId"]} in spanId={context.span["spanId"]}",
                extra=build_context_tags(context),
            )


@when("I adopt the {goal} goal")
def step_impl(context, goal):
    pass


@when("I evaluate current_goal success")
def step_impl(context):
    pass


@then("goal success is true")
def step_impl(context):
    pass
