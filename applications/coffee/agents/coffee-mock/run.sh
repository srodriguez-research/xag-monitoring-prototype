
mvn clean package

export JAVA_TOOL_OPTIONS="-javaagent:./target/opentelemetry-javaagent.jar"
export OTEL_RESOURCE_ATTRIBUTES=service.name=coffee-mock

java -jar target/coffee-mock-0.1-SNAPSHOT.jar
