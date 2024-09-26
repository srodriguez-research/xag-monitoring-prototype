# Opentelemetry instrumentation 

## Running

```shell
mkdir -p data/tempo-data
docker compose up -d
open http://localhost:3000/explore
docker compose down -v 
```



`tempo-data` stores all data for local use only.


# Running python

```shell

poetry shell
behave --no-capture -D trace=data/traces_store/1368ab4fde5b47e9756b85726803ed91 
```

Editing with vim
```
source $(poetry env info --path)/bin/activate
```
### Reports
`brew install allure`

## References


### Opentelemetry
Libraries and SDKs:
 - https://github.com/open-telemetry/opentelemetry-java


TODO: https://www.youtube.com/watch?v=Hink0jF8c28

Tutorials, Videos and other References:
- https://opentelemetry.io/docs/languages/java/instrumentation/
- https://www.youtube.com/watch?v=hXTlV_RnELc and https://github.com/davidgeorgehope/custom-instrumentation-examples


### Grafana Tempo

- https://github.com/grafana/tempo/tree/main/example/docker-compose/local
