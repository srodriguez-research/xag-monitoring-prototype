import os

from behave import parser
from behave.model import Feature, Scenario, Step
from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

_ = load_dotenv()  # take environment variable

FEATURES_DIR = os.getenv("FEATURES_DIR")
TRACES_DIR = os.getenv("TRACES_DIR")


@app.route("/")
def explain_trace():
    trace_id = ""
    # tracefile = os.path.join(TRACES_DIR, trace_id)

    # parse the trace to get spans

    # Select span with plan revision

    feature_file = os.path.join(FEATURES_DIR, "getcoffee.feature")

    feature_text = open(feature_file).read()
    feature: Feature = parser.parse_file(feature_file)
    scenario: Scenario = feature.scenarios[0]
    scenario_text = ""

    return render_template(
        "explain_trace.html", scenario=scenario, feature_text=feature_text
    )
