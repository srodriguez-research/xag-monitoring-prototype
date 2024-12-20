# Monitoring and Verification of Explainable Agents 

This repository is provided as part of our work for AAMAS 2025 (extended abstract) and IJCAI 2025.

## Configuration

If monitoring will be started using docker compose, you have to configure which `service` (i.e. agent system) it will be monitoring.
In the docker compose file for the monitor service:
```
      - SERVICE_NAME=coffee-mock
```

**By default monitoring is not started using docker**


## Running


### Starting Grafana services

Traces and logs are managed by Grafana suite of applications. 
To start

```shell
mkdir -p data/tempo-data
docker compose up -d
open http://localhost:3000/explore
```

To shutdown:
```
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
