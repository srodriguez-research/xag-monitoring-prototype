import pytest

from uss.service import verify_trace


@pytest.mark.skip("Behave doesn't support multiple configuration files.")
def test_verify_trace():
    out = verify_trace("tests/resources/trace.json")
    assert out.returncode == 0

    out = verify_trace("tests/resources/trace2.json")
    assert out.returncode == 0
