# ksqlDB
ksqlDB is a database that's purpose-built for stream processing applications. The main focus of stream processing is modeling computation over unbounded streams of events.

## Streams
There are three kinds of queries in ksqlDB: persistent, push, and pull. Each gives you different ways to work with rows of events.

## Queries
There are three kinds of queries in ksqlDB: persistent, push, and pull. Each gives you different ways to work with rows of events.

### Persistent
Persistent queries are server-side queries that run indefinitely processing rows of events. You issue persistent queries by deriving new streams and new tables from existing streams or tables.

### Push
A push query is a form of query issued by a client that subscribes to a result as it changes in real-time. A good example of a push query is subscribing to a particular user's geographic location. The query requests the map coordinates, and because it's a push query, any change to the location is "pushed" over a long-lived connection to the client as soon as it occurs. We need to user `emit changes` in order to indicate a query is a push query. The result of a push query isn't persisted to a backing Kafka topic. If you need to persist the result of a query to a Kafka topic, use a CREATE TABLE AS SELECT or CREATE STREAM AS SELECT statement.

### Pull
A pull query is a form of query issued by a client that retrieves a result as of "now", like a query against a traditional RDBS. Because it's a pull query, it returns immediately with a finite result and closes its connection. This is ideal for rendering a user interface once, at page load time. It's generally a good fit for any sort of synchronous control flow.

## Create a Stream
A stream essentially associates a schema with an underlying Kafka topic.
```shell
CREATE STREAM riderLocations (profileId VARCHAR, latitude DOUBLE, longitude DOUBLE)
  WITH (kafka_topic='locations', value_format='json');
```

* __kafka_topic__: Name of the Kafka topic underlying the stream. The topic to read from. 
  In this case it will be automatically created because it doesn't exist yet,
  but streams may also be created over topics that already exist.

* __value_format__ - Encoding of the messages stored in the Kafka topic. For JSON encoding, 
  each row will be stored as a JSON object whose keys/values are column names/values.
  For example: 
  ```json
  {
    "profileId": "c2309eec",
    "latitude": 37.7877,
    "longitude": -122.4205
  }
  ```

* __partitions__ - Number of partitions to create for the locations topic. 
  Note that this parameter is not needed for topics that already exist.


### Persistent Query
```shell
# Within 50 Miles of (-15.411, -45.1162)
SELECT * FROM riderLocations
WHERE GEO_DISTANCE(latitude, longitude, -15.411, -45.1162) <= 50 EMIT CHANGES;
```


### Populate Stream
```shell
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('c2309eec', 37.7877, -122.4205);
```

## Some commands
### Open Shell
```shell
ksql http://ksqldb-server:8088
```

### List Topics
```shell
ksql> list topics extended;
```

#### Queries
```shell
ksql> show queries;
```

#### Terminate Query
```shell
ksql> terminate query_id;
```

#### Streams
```shell
ksql> show streams;
```

#### Delete Stream
Before deleting a stream make sure you have terminated all the queries that are using it.
```shell
ksql> drop stream stream_name;
```

#### Print events from stream
```shell
ksql> print stream_name;
```

## Referencies
