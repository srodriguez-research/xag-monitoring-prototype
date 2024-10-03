# Monitoring and Verification of Explainable Agents 

This repository is provided as part of our work for AAMAS 2025

## Configuration

In the docker compose file for the monitor service

```
      - SERVICE_NAME=coffee-mock
```

## Running

```shell
mkdir -p data/tempo-data
docker compose up -d
open http://localhost:3000/explore
docker compose down -v 
```



`tempo-data` stores all data for local use only.


### Running monitoring system locally on single trace

```shell
poetry shell
behave --no-capture -D trace=data/traces_store/1368ab4fde5b47e9756b85726803ed91 
```

Editing with vim
```
source $(poetry env info --path)/bin/activate
```

### Reports
Intall allure
`brew install allure`

# Querying Tempo directly

Get a single trace by id:

```
TRACE_ID=f92b7616e40843b75c5ee7cfba5553e7
curl -G -s http://localhost:3200/api/v2/traces/$TRACE_ID | jq
```

Search traces by service name:
```
# Get traces with error status
# TRACEQL="{status=error}"

export SERV_NAME=coffee-mock
export TRACEQL="{resource.service.name=\"$SERV_NAME\"}"


curl -G -s http://localhost:3200/api/search --data-urlencode "q=$TRACEQL" | jq
```
