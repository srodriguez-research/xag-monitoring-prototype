import os

from behave.model import Feature, Scenario, Step
from dotenv import load_dotenv
from flask import Flask, render_template

from uss.behave import find_scenarios, parse_behave_report
from uss.tempo import parse_trace_json

app = Flask(__name__)
_ = load_dotenv()  # take environment variable

FEATURES_DIR = os.getenv("FEATURES_DIR")
TRACES_DATA_DIR: str = "data"  # os.getenv("TRACES_DATA_DIR")


@app.route("/")
def explain_plan_selection():
    TRACE_ID = "7a9fc1aaf821f7d6a6f06366c7c2136a"
    trace = parse_trace_json(os.path.join(TRACES_DATA_DIR, "traces_store", TRACE_ID))
    report = parse_behave_report(
        os.path.join(TRACES_DATA_DIR, "reports", f"{TRACE_ID}-report.json")
    )

    scenarios = find_scenarios(report)

    return render_template(
        "explain_plan_selection_with_report.html",
        debug=True,
        report=report,
        trace=trace,
        scenarios=scenarios,
    )


if __name__ == "__main__":
    app.run(debug=True)
