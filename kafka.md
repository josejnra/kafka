# Kafka
## Useful Commands
#### Create Topic
```shell
kafka-topics --create --topic quickstart-events --bootstrap-server localhost:9092
```
An Alternative to create a topic is using `--zookeeper` as parameter. This way we do need to point every broker
which belongs to the cluster.
```shell
kafka-topics --create --topic quickstart-events --partitions 4 --replication-factor 1 --zookeeper localhost:2181
```

#### Describe Topic
```shell
kafka-topics --describe --topic quickstart-events --bootstrap-server localhost:9092
```

#### Producer Console
```shell
kafka-console-producer --broker-list localhost:9092 --topic topic_name
```

#### Consumer Console
```shell
kafka-console-consumer --bootstrap-server localhost:9092 --topic topic_name
```

#### List Topics
```shell
kafka-topics --list --bootstrap-server localhost:9092
```

#### Delete a Topic
```shell
kafka-topics --zookeeper localhost:2181 --delete --topic lib_events
```

#### Version
```shell
confluent version kafka
kafka-topics --version
confluent version ksql-server
```

### Connect
#### List Connectors
```shell
curl -X GET http://localhost:8000/connectors
```

#### Delete a Connector
```shell
curl -X DELETE http://localhost:8000/connectors/connector-name
```

#### Submit a new Connector
```shell
curl -X POST -H 'Content-Type:application/json' --data @"./connector_config.json" http://localhost:8000/connectors/
```

#### Atualizar connect sink
```shell
curl -X PUT -H "Content-Type: application/json" --data @"./connector_config.json" localhost:8000/connectors/connector_name/config
```

### Others
#### Check any log from any service from Confluent Platform
```shell
journalctl -u confluent-kafka-connect
```


## Referencies
- [Apache Kafka Primer](https://docs.ksqldb.io/en/latest/concepts/apache-kafka-primer/)




{"name": "jose", "id": 10, "campoNovo": 123}
{"name": "jose", "campoNovo": 123}
{"Name": "jose", "campoNovo": 123}

{"NAME": "jose", "ID": 10, "campoNovo": 123}
{"NAME": "jose", "ID": 10, "campo_novo": 123}


CREATE OR REPLACE STREAM users (name VARCHAR, id INTEGER, campoNovo INTEGER) WITH (kafka_topic='users', value_format='json', partitions=1);


1000:{"userid":"1000","firstname":"Jose","lastname":"Edison","countrycode":"US","rating":"2.2"}
