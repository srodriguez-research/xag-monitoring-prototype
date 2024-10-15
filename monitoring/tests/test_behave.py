from uss.behave import (count_scenarios_by_status, find_scenarios,
                        parse_behave_report)


def test_parse_behave_report():
    result = parse_behave_report(
        "tests/resources/reports/trace-kitchen-and-shop-ok-report.json"
    )
    assert result is not None
    assert result["status"] == "passed"
    assert len(result["elements"]) is 9


def test_find_scenarios():
    result = parse_behave_report(
        "tests/resources/reports/trace-kitchen-and-shop-ok-report.json"
    )
    scenarios = find_scenarios(result)
    assert len(scenarios) == 9


def test_count_by_status_ok():
    result = parse_behave_report(
        "tests/resources/reports/trace-kitchen-and-shop-ok-report.json"
    )
    scenarios = find_scenarios(result)
    count = count_scenarios_by_status(scenarios)

    assert count["passed"] == 4
    assert count["skipped"] == 5
    assert count["failed"] == 0


def test_count_by_status_fail():
    result = parse_behave_report(
        "tests/resources/reports/trace-kitchen-and-shop-fail-report.json"
    )
    scenarios = find_scenarios(result)
    count = count_scenarios_by_status(scenarios)

    assert count["passed"] == 3
    assert count["skipped"] == 5
    assert count["failed"] == 1
