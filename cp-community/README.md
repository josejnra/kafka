## Docker Compose
The defined [docker-compose.yaml](../cp-community/docker-compose.yaml) has the following services:

- zookeeper
- kafka-broker1
- kafka-broker2
- schema-registry
- ksqldb-server
- ksqldb-cli
- kafka-connect
- kafka-rest
- ksql-datagen
- control-center
- minio
- postgres
- pgadmin

### Some commands
#### Zookeeper
```shell
docker container exec -it zookeeper bash
```

List available brokers:
```shell
zookeeper-shell zookeeper:2181 ls /brokers/ids
```

A broker's details:
```shell
zookeeper-shell zookeeper:2181 get /brokers/ids/1
```

#### Kafka Connect
```shell
docker container exec -it kafka-connect bash
```

List available brokers:
```shell
kafka-broker-api-versions --bootstrap-server kafka-broker1:29092 | awk '/id/{print $1}'
```

Describe a topic:
```shell
kafka-topics --describe --topic topic-name --bootstrap-server kafka-broker1:29092
```
