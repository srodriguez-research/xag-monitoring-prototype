export JAVA_TOOL_OPTIONS="-javaagent:../libs/opentelemetry-javaagent.jar"
export OTEL_RESOURCE_ATTRIBUTES=service.name=coffee-mock

mvn clean package
java -jar ./target/coffee-mock-0.1-SNAPSHOT.jar
