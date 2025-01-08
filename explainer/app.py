import os
from pathlib import Path

from behave.model import Feature, Scenario, Step
from dotenv import load_dotenv
from flask import Flask, render_template
from ollama import ChatResponse, chat

from uss.behave import find_scenarios, parse_behave_report
from uss.tempo import parse_trace_json

app = Flask(__name__)
_ = load_dotenv()  # take environment variable

FEATURES_DIR = os.getenv("FEATURES_DIR")
TRACES_DATA_DIR: str = "data"  # os.getenv("TRACES_DATA_DIR")
FEATURE_TEXT = " "


@app.route("/")
def explain_plan_selection():
    # TRACE_ID = "ac4ccbc701cb3c4087227130ba445af5" # plan rating
    TRACE_ID = "ac4ccbc701cb3c4087227130ba445af5"
    trace = parse_trace_json(os.path.join(TRACES_DATA_DIR, "traces_store", TRACE_ID))

    report = parse_behave_report(
        os.path.join(TRACES_DATA_DIR, "reports", f"{TRACE_ID}-report.json")
    )

    filename = report["location"].split(":")[0]
    feature_file_path = Path(os.path.join(FEATURES_DIR, "..", filename))
    with open(feature_file_path) as ff:
        FEATURE_TEXT = ff.read()

    scenarios = find_scenarios(report)
    scenarios_failed = filter(lambda s: s["status"] == "failed", scenarios)
    scenarios_passed = filter(lambda s: s["status"] == "passed", scenarios)
    scenarios_skipped = filter(lambda s: s["status"] == "skipped", scenarios)

    return render_template(
        "explain_plan_selection_with_report.html",
        debug=True,
        report=report,
        trace=trace,
        scenarios_failed=scenarios_failed,
        scenarios_passed=scenarios_passed,
        scenarios_skipped=scenarios_skipped,
    )


def build_prompt_failed(scenario) -> str:
    prompt = f"""
The specification below defines the acceptable decisions for an intelligent agent.
Statements starting with "Given" refer to the agent's beliefs at the time of making the decision;
Statement with "When" was the decision the agent was try to make;
And Statement with "Then" was my expected behaviour which in this case I failed to comply to.

Specification:
            {FEATURE_TEXT}
Explain in first person why the scenario below is failing:
{togherkin(scenario)}
    """
    return prompt


def togherkin(scenario) -> str:
    text = ""
    for step in scenario["steps"]:
        if "result" in step:
            step_status = step["result"]["status"]
        else:
            step_status = "unevaluated"
        text += f"{step['keyword']} {step['name']} ( step {step_status})"

    return text


def status2color(status: str) -> str:

    if status == "passed":
        return "green"

    if status == "skipped":
        return "yellow"

    if status == "failed":
        return "red"

    return "purple"


def scenario_breakdown(scenario):
    given = []
    when = None
    then = []

    for step in scenario["steps"]:

        step_status = "uneval"
        if "result" in step:
            step_status = step["result"]["status"]

        step["status"] = step_status

        match step["keyword"].lower():
            case "given":
                given.append(step)

            case "when":
                when = step
            case "then":
                then.append(step)
    return [given, when, then]


def llm(prompt: str) -> str:

    response: ChatResponse = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.message.content


def past_tense(text: str) -> str:
    return llm(f"write in past tense: {text}")


def explain_failed_step(step) -> str:
    msg = step["result"]["error_message"].replace("Assertion Failed:", "")
    prompt = f"rewrite explanation. Just print result: I failed to {step['name']}, because {msg} "

    print(prompt)
    return llm(prompt)


def find_span_for_scenario(scenario, trace):
    CRITERIA_KEY = "xag.process.criteria.id"
    name = scenario["name"].split("--")[0].strip()
    print(f"## finding {name}")
    for span in trace["spans"]:
        if CRITERIA_KEY in span and name in span[CRITERIA_KEY]:
            print(f"## {span=}")
            return span
    return None


def llm_explain(scenario) -> str:
    return llm(build_prompt_failed(scenario))


app.jinja_env.filters["status2color"] = status2color
app.jinja_env.filters["llm"] = llm
app.jinja_env.filters["llm_explain"] = llm_explain
app.jinja_env.filters["past_tense"] = past_tense
app.jinja_env.filters["explain_failed_step"] = explain_failed_step
app.jinja_env.globals.update(scenario_breakdown=scenario_breakdown)
app.jinja_env.globals.update(find_span_for_scenario=find_span_for_scenario)


if __name__ == "__main__":
    app.run(debug=True)
