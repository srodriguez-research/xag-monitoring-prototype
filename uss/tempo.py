import base64
import json


def base64_to_hex(trace_id_base64) -> str:
    return base64.b16encode(base64.b64decode(trace_id_base64)).decode("utf-8").lower()


def array_to_dict_by(arr, key) -> dict:
    res = dict()
    for a in arr:
        res[a[key]] = a
    return res


def parse_trace_json(filepath) -> dict:
    trace = dict()
    data = json.load(open(filepath))
    spans = []
    trace_id = None
    trace_id_base64 = None
    for s in data["trace"]["resourceSpans"][0]["scopeSpans"][0]["spans"]:
        trace_id = base64_to_hex(s["traceId"])
        s["spanIdB64"] = s["spanId"]
        s["traceIdB64"] = s["traceId"]
        s["spanId"] = base64_to_hex(s["spanId"])

        trace_id_base64 = s["traceId"]
        trace_id = base64_to_hex(s["traceId"])
        s["traceId"] = trace_id

        for a in s["attributes"]:
            if "stringValue" in a["value"]:
                s[a["key"]] = a["value"]["stringValue"]
            if "intValue" in a["value"]:
                s[a["key"]] = int(a["value"]["intValue"])
            if "boolValue" in a["value"]:
                s[a["key"]] = bool(a["value"]["boolValue"])

        spans.append(s)

    trace["spans"] = spans
    trace["traceId"] = trace_id
    trace["traceIdB64"] = trace_id_base64

    return trace
