from uss.service import verify_trace


def test_verify_trace():
    out = verify_trace("tests/resources/trace.json")
    assert out.returncode == 0

    out = verify_trace("tests/resources/trace2.json")
    assert out.returncode == 0
