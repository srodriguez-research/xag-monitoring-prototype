from uss.tempo import array_to_dict_by, parse_trace_json


def test_array_to_dict_by():
    arr = [
        {"questionId": "1", "title": "title 1", "marks": 10},
        {"questionId": "2", "title": "title 2", "marks": 11},
    ]

    d = array_to_dict_by(arr, "questionId")
    assert "1" in d
    assert "2" in d
    assert "3" not in d

    assert d["1"]["title"] == "title 1"
    assert d["2"]["title"] == "title 2"
    assert d["2"]["marks"] == 11


def test_parse_trace_json():
    trace = parse_trace_json("tests/resources/trace.json")
    assert trace["traceIdB64"] == "EORX8p8V4xOK1/7Xc61aSg=="
    assert trace["traceId"] == "10e457f29f15e3138ad7fed773ad5a4a"
    assert len(trace["spans"]) == 4
    span = trace["spans"][0]
    assert span["name"] == "goal_revision"
    assert span["xag.query.goals.active"] == "[GetCoffee]"
    assert span["xag.trigger.name"] == "ReviewGoals"

    assert span["traceIdB64"] == "EORX8p8V4xOK1/7Xc61aSg=="
    assert span["spanIdB64"] == "MhcH6Tuzqcs="
    assert trace["traceId"] == "10e457f29f15e3138ad7fed773ad5a4a"
    assert span["spanId"] == "321707e93bb3a9cb"
