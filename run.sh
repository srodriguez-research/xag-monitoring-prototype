export JAVA_TOOL_OPTIONS="-javaagent:libs/opentelemetry-javaagent.jar"
# export OTEL_SERVICE_NAME="xag-test"
# export OTEL_EXPORTER=otlp_span
# export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:3200
# export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_RESOURCE_ATTRIBUTES=service.name=xag-test

mvn clean package
java -jar ./target/tempo-demo-0.1-SNAPSHOT.jar
