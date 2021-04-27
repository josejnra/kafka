## Useful Commands
### Kafka
#### Create Topic
```shell
$ kafka-topics --create --topic quickstart-events --bootstrap-server localhost:9092
```
An Alternative to create a topic is using `--zookeeper` as parameter. This way we do need to point every broker
which belongs to the cluster.
```shell
$ kafka-topics --create --topic quickstart-events --partitions 4 --replication-factor 1 --zookeeper localhost:2181
```

#### Describe Topic
```shell
$ kafka-topics --describe --topic quickstart-events --bootstrap-server localhost:9092
```

#### Producer Console
```shell
$ kafka-console-producer --broker-list localhost:9092 --topic topic_name
```

#### Consumer Console
```shell
$ kafka-console-consumer --bootstrap-server localhost:9092 --topic topic_name
```

#### List Topics
```shell
$ kafka-topics --list --bootstrap-server localhost:9092
```

#### Delete a Topic
```shell
$ kafka-topics --zookeeper localhost:2181 --delete --topic lib_events
```

#### Version
```shell
$ confluent version kafka
$ kafka-topics --version
$ confluent version ksql-server
```

### Connect
#### List Connectors
```shell
$ curl -X GET http://localhost:8000/connectors
```

#### Delete a Connector
```shell
$ curl -X DELETE http://localhost:8000/connectors/connector-name
```

#### Submit a new Connector
```shell
$ curl -X POST -H 'Content-Type:application/json' --data @"./connector_config.json" http://localhost:8000/connectors/
```

#### Atualizar connect sink
```shell
$ curl -X PUT -H "Content-Type: application/json" --data @"./connector_config.json" localhost:8000/connectors/connector_name/config
```

### KSQL
#### Open Shell
```shell
$ sudo ksql http://localhost:8088
```

#### Queries
```shell
show queries;
```

#### Terminate Query
```shell
terminate query_id;
```

#### Streams
```shell
show streams;
```

#### Delete Stream
Before deleting a stream make sure you have terminated all the queries that are using it.
```shell
drop stream stream_name;
```

#### Print events from stream
```shell
print stream_name;
```


### Others
#### Check any log from any service from Confluent Platform
```shell
$ journalctl -u confluent-kafka-connect
```
