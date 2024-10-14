import json
import os

from behave import parser
from behave.model import Feature, Scenario, Step
from dotenv import load_dotenv
from flask import Flask, render_template

from uss.tempo import parse_trace_json

app = Flask(__name__)

_ = load_dotenv()  # take environment variable

FEATURES_DIR = os.getenv("FEATURES_DIR")
TRACES_DIR = os.getenv("TRACES_DIR")


@app.route("/")
def explain_plan_selection():
    trace_id = "trace.json"
    tracefile = os.path.join(TRACES_DIR, trace_id)

    # Select span with plan revision

    feature_file = os.path.join(FEATURES_DIR, "getcoffee.feature")

    feature_text = open(feature_file).read()
    feature: Feature = parser.parse_file(feature_file)
    scenario: Scenario = feature.scenarios[0]

    beliefs = {"haveMoney": False, "staffCardAvailable": True, "annInOffice": False}

    # debug = False
    debug = False
    # parse the trace to get spans
    spans = parse_trace_json(tracefile)
    # process_to_find = "PLAN_REVISION"
    # process_to_find = "PLAN_SELECTION"
    process_to_find = "PLAN_META_RATING"
    # process_to_find = "PLAN_RATING"
    # span = next(s for s in spans["spans"] if s["name"] == process_to_find)
    span = [s for s in spans["spans"] if s["name"] == process_to_find]
    span = json.dumps(span, indent=2)
    # span = ""

    selected_plan = "KitchenCoffee"
    return render_template(
        "explain_plan_selection.html",
        span=span,
        spans=spans,
        selected_plan=selected_plan,
        beliefs=beliefs,
        scenario=scenario,
        feature_text=feature_text,
        debug=debug,
    )
