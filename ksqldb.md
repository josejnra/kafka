# ksqlDB
ksqlDB is a database that's purpose-built for stream processing applications. The main focus of stream processing is modeling computation over unbounded streams of events.

ksqlDB is actually a Kafka Streams application, meaning that ksqlDB is a completely different product with different capabilities, but uses Kafka Streams internally. Hence, there are both similarities and differences.
- **Deployment**: Unlike ksqlDB, the Kafka Streams API is a library in your app code! Thus, the main difference is that ksqlDB is a platform service while Kafka Streams is a customer user service. You do not allocate servers to deploy Kafka Streams like you do with ksqlDB.
- **User Experience**: Kafka Streams runs tasks in parallel for the relevant partitions that need to be processed, and the complexity and amount of partitions utilized will increase your CPU utilization. Since we are working with writing an application and deploying our code, it’s a totally different user experience from that of ksqlDB. Rather, Kafka Streams is ultimately an API tool for Java application teams that have a CI/CD pipeline and are comfortable with distributed computing.

## Events
ksqlDB aims to raise the abstraction from working with a lower-level stream processor. Usually, an event is called a "row", as if it were a row in a relational database. Each row is composed of a series of columns. Columns are either read from the event's key or value. ksqlDB also supports a ROWTIME pseudo column, available on every row, that represents the time of the event. In addition, windowed sources have WINDOWSTART and WINDOWEND system columns.

## Materialized Views
Streams and tables are closely related. A stream is a sequence of events that you can derive a table from. For example, a sequence of credit scores for a loan applicant can change over time. The sequence of credit scores is a stream. But this stream can be interpreted as a table to describe the applicant's current credit score.

The benefit of a *materialized view* is that it evaluates a query on the changes only (the delta), instead of evaluating the query on the entire table.

When a new event is integrated, the current state of the view evolves into a new state. This transition happens by applying the aggregation function that defines the view with the current state and the new event. When a new event is integrated, the aggregation function that defines the view is applied only on this new event, leading to a new state for the view. In this way, a view is never "fully recomputed" when new events arrive. Instead, the view adjusts incrementally to account for the new information, which means that queries against materialized views are highly efficient.

In ksqlDB, a table can be materialized into a view or not. If a table is created directly on top of a Kafka topic, it's not materialized. Non-materialized tables can't be queried, because they would be highly inefficient. On the other hand, if a table is derived from another collection, ksqlDB materializes its results, and you can make queries against it.

ksqlDB leverages the idea of stream/table duality by storing both components of each table. The current state of a table is stored locally and ephemerally on a specific server by using RocksDB.

## Streams
A stream is a partitioned, immutable, append-only collection that represents a series of historical facts. For example, the rows of a stream could model a sequence of financial transactions, like "Alice sent $100 to Bob", followed by "Charlie sent $50 to Bob". Once a row is inserted into a stream, it can never change. New rows can be appended at the end of the stream, but existing rows can never be updated or deleted. Each row is stored in a particular partition. Every row, implicitly or explicitly, has a key that represents its identity. All rows with the same key reside in the same partition.

## Tables
A table is a mutable, partitioned collection that models change over time. In contrast with a stream, which represents a historical sequence of events, a table represents what is true as of "now". For example, you might use a table to model the locations where someone has lived as a stream: first Miami, then New York, then London, and so forth.

Tables work by leveraging the keys of each row. If a sequence of rows shares a key, the last row for a given key represents the most up-to-date information for that key's identity. A background process periodically runs and deletes all but the newest rows for each key.

## Queries
There are three kinds of queries in ksqlDB: persistent, push, and pull. Each gives you different ways to work with rows of events.

### Persistent
Persistent queries are server-side queries that run indefinitely processing rows of events. You issue persistent queries by deriving new streams and new tables from existing streams or tables.

### Push
A push query is a form of query issued by a client that subscribes to a result as it changes in real-time. A good example of a push query is subscribing to a particular user's geographic location. The query requests the map coordinates, and because it's a push query, any change to the location is "pushed" over a long-lived connection to the client as soon as it occurs. We need to user `emit changes` in order to indicate a query is a push query. The result of a push query isn't persisted to a backing Kafka topic. If you need to persist the result of a query to a Kafka topic, use a `CREATE TABLE AS SELECT` or `CREATE STREAM AS SELECT` statement.

### Pull
A pull query is a form of query issued by a client that retrieves a result as of "now", like a query against a traditional RDBS. Because it's a pull query, it returns immediately with a finite result and closes its connection. This is ideal for rendering a user interface once, at page load time. It's generally a good fit for any sort of synchronous control flow.

Execute a pull query by sending an HTTP request to the ksqlDB REST API, and the API responds with a single response.

## Useful Commands
### Create a Stream
Connect to the console by running:
```shell
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

A stream essentially associates a schema with an underlying Kafka topic.
```shell
CREATE STREAM riderLocations (profileId VARCHAR, latitude DOUBLE, longitude DOUBLE)
  WITH (kafka_topic='locations', value_format='json', partitions=1);
```

* __kafka_topic__: Name of the Kafka topic underlying the stream. The topic to read from. In this case it will be automatically created because it doesn't exist yet, but streams may also be created over topics that already exist.

* __value_format__ - Encoding of the messages stored in the Kafka topic. For JSON encoding, each row will be stored as a JSON object whose keys/values are column names/values. For example: 
```json
{
  "profileId": "c2309eec",
  "latitude": 37.7877,
  "longitude": -122.4205
}
```

* __partitions__ - Number of partitions to create for the locations topic. Note that this parameter is not needed for topics that already exist.

### Create Materialized Views
```shell
CREATE TABLE currentLocation AS
  SELECT profileId,
         LATEST_BY_OFFSET(latitude) AS la,
         LATEST_BY_OFFSET(longitude) AS lo
  FROM riderlocations
  GROUP BY profileId
  EMIT CHANGES;
```

```shell
CREATE TABLE ridersNearMountainView AS
  SELECT ROUND(GEO_DISTANCE(la, lo, 37.4133, -122.1162), -1) AS distanceInMiles,
         COLLECT_LIST(profileId) AS riders,
         COUNT(*) AS count
  FROM currentLocation
  GROUP BY ROUND(GEO_DISTANCE(la, lo, 37.4133, -122.1162), -1);
```

### Push Query
```shell
# Within 50 Miles of (-15.411, -45.1162)
SELECT * FROM riderLocations
WHERE GEO_DISTANCE(latitude, longitude, -15.411, -45.1162) <= 50 EMIT CHANGES;
```

### Pull Query
```shell
SET 'ksql.query.pull.table.scan.enabled'='true';
SELECT * from ridersNearMountainView WHERE distanceInMiles <= 10;
```
### Persistent Query
```shell
```

### Populate Stream
```shell
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('c2309eec', 37.7877, -122.4205);
```

### List Topics
```shell
ksql> list topics extended;
```

### Queries
```shell
ksql> show queries;
```

### Terminate Query
```shell
ksql> terminate query_id;
```

### Streams
```shell
ksql> show streams;
```

### Delete Stream
Before deleting a stream make sure you have terminated all the queries that are using it.
```shell
ksql> drop stream stream_name;
```

### Print events from stream
```shell
ksql> print stream_name;
```

## Data Generator
Inside ksqldb-server run the following command to generate synthetic test data.
```shell
ksql-datagen bootstrap-server=kafka-broker1:29092 schemaRegistryUrl=schema-registry:8081 schema=./userprofile.avro value-format=json key=userid topic=userprofile maxInterval=5000 iterations=10
```
where as `userprofile.avro` is:
```json
{
  "namespace": "streams",
  "name": "userprofile",
  "type": "record",
  "fields": [
    {
      "name": "userid",
      "type": {
        "type": "string",
        "arg.properties": {
          "iteration": {
            "start": 1000,
            "step": 1
          }
        }
      }
    },
    {
      "name": "firstname",
      "type": {
        "type": "string",
        "arg.properties": {
          "options": [
            "Alice",
            "Bob",
            "Carol",
            "Dan",
            "Eve",
            "Frank",
            "Grace",
            "Heidi",
            "Ivan"
          ]
        }
      }
    },
    {
      "name": "lastname",
      "type": {
        "type": "string",
        "arg.properties": {
          "options": [
            "Smith",
            "Jones",
            "Coen",
            "Fawcett",
            "Edison",
            "Jones",
            "Dotty"
          ]
        }
      }
    },
    {
      "name": "countrycode",
      "type": {
        "type": "string",
        "arg.properties": {
          "options": [
            "AU",
            "IN",
            "GB",
            "US"
          ]
        }
      }
    },
    {
      "name": "rating",
      "type": {
        "type": "string",
        "arg.properties": {
          "options": [
            "3.4",
            "3.9",
            "2.2",
            "4.4",
            "3.7",
            "4.9"
          ]
        }
      }
    }
  ]
}
```

## Referencies
- [Kafka Streams vs ksqlDB Compared](https://www.confluent.io/blog/kafka-streams-vs-ksqldb-compared/)
- [Events](https://docs.ksqldb.io/en/latest/concepts/events/)
- [Streams](https://docs.ksqldb.io/en/latest/concepts/streams/)
- [Tables](https://docs.ksqldb.io/en/latest/concepts/tables/)
- 