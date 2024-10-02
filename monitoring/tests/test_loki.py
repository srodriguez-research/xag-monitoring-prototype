from uss.loki import build_tags


def test_build_tags():
    out = build_tags({"mytag": "tagvalue"})
    assert out["tags"]["service"] == "story-verification"
    assert out["tags"]["mytag"] == "tagvalue"
