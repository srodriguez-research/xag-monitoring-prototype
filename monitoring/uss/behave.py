import json


def parse_behave_report(filename):
    return json.loads(open(filename).read())[0]


def find_scenarios(report: dict) -> list:
    scenarios = []
    for elem in report["elements"]:
        if elem["type"] == "scenario":
            scenarios.append(elem)
    return scenarios


def count_scenarios_by_status(scenarios: list) -> dict:
    out = {
        "passed": 0,
        "skipped": 0,
        "failed": 0,
    }
    for s in scenarios:
        status = s["status"]
        out[status] = out[status] + 1

    return out
