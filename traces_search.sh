# TRACEQL="{status=error}"
SERV_NAME=xag-test
TRACEQL="{resource.service.name=\"$SERV_NAME\"}"

curl -G -s http://localhost:3200/api/search --data-urlencode "q=$TRACEQL" | jq
