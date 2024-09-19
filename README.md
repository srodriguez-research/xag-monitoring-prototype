# Opentelemetry instrumentation 

## Running

```shell
mkdir tempo-data
docker compose up -d
open http://localhost:3000/explore
docker compose down -v 
```


`tempo-data` stores all data for local use only.

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
