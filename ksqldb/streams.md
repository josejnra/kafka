## Streams
There are three kinds of queries in ksqlDB: persistent, push, and pull. Each gives you different ways to work with rows of events.

##### Persistent
Persistent queries are server-side queries that run indefinitely processing rows of events. You issue persistent queries by deriving new streams and new tables from existing streams or tables.

##### Push
A push query is a form of query issued by a client that subscribes to a result as it changes in real-time.

### Create a Stream
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
