JAR_NAME=$(shell mvn help:evaluate -Dexpression=project.build.finalName | grep -v '\[')

dev:
	@mvn spring-boot:run

build:
	@mvn initialize
	@mvn clean install

run:
	java -jar ./target/$(JAR_NAME).jar -Djava.library.path=./libs
