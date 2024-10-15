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
def step_impl_bel(context, belief, value):
    value = bool(value)

    if "goal-plan" in context.scenario.tags:
        span = context.span
        belief2find = f"xag.query.{belief}"

        #  Has this rating considered
        if belief2find not in span:
            context.scenario.skip(f"Belief {belief2find} was not used in this decision")
            context.given_applies = False
            return

        spanBel = span[belief2find]

        if spanBel != value:
            context.scenario.skip(
                f"Belief {belief2find} was {spanBel} instead for {value}"
            )
            context.given_applies = False
            return

    else:
        assert None == "Should not be here!!"


@given("I have an applicable plan with valuing {valuing} {value}")
def step_impl_valuing(context: Context, valuing, value):
    result = json.loads(context.span["xag.actions.call.return"])

    # lets find plans matching this valuing
    if not hasattr(context, "valuing_matching_plans"):
        # load all and filter later
        context.valuing_matching_plans = result

    matching = []
    for plan in context.valuing_matching_plans:
        # The plan is applicable only if the previous (local) rating was > 0.
        applicable = plan["previousRatingElement"]["rating"] > 0

        if applicable and plan["valuings"][valuing] == value:
            matching.append(plan)
    context.valuing_matching_plans = matching

    if len(context.valuing_matching_plans) == 0:
        context.scenario.skip(
            f"No spans matches this plan-rating scenario. Requires {valuing} is {value}"
        )


@then("plan {plan} is applicable")
def step_impl_applicable(context: Context, plan):

    # Check if the plan in not the applicablePlans
    # then the engine FAILED to comply to requirements
    result = json.loads(context.span["xag.actions.call.return"])
    # Anything above 0 is a potentially applicable plan
    rating = result["rating"]
    failed_msg = f"Failed to verify story={context.feature.name} scenario={context.scenario.name} for traceId={context.trace["traceId"]} in spanId={context.span["spanId"]}"
    if rating <= 0:
        context.logger.critical(
            failed_msg,
            extra=build_context_tags(context),
        )
    assert rating > 0, failed_msg


@then("I rate it with {rating}")
def step_impl_rate(context, rating):
    rating = float(rating)
    for plan in context.valuing_matching_plans:
        # pprint(plan)
        # assert False
        failed_msg = (
            f"rating for plan {plan['plan']} is {plan['rating']} but should be {rating}"
        )
        if plan["rating"] != rating:
            context.logger.critical(
                failed_msg,
                extra=build_context_tags(context),
            )
            pprint(plan)
        assert plan["rating"] == rating, failed_msg


@then("goal success is true")
def step_impl_goal_sucess(context):
    pass


@then("I select the highest-rated plan")
def step_impl_select_highest(context):
    # Verified by engine
    pass


####################################################
# @When are not checked, the decsion has been made.
# we are verifying it was correct.
####################################################


@when("I adopt the {goal} goal")
def step_impl_adopt_goal(context, goal):
    pass


@when("I evaluate current_goal success")
def step_impl_current_goal(context):
    pass


@when("I select the plan")
def step_impl_select_plan(context):
    pass
