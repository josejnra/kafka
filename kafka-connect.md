# Kafka Connect
Kafka Connect is a free, open-source component of Apache Kafka that works as a centralized data hub for simple data integration between databases, key-value stores, search indexes, and file systems.

Kafka Connect is a tool for scalably and reliably streaming data between Apache Kafka® and other data systems. It makes it simple to quickly define connectors that move large data sets into and out of Kafka. Kafka Connect can ingest entire databases or collect metrics from all your application servers into Kafka topics, making the data available for stream processing with low latency. An export connector can deliver data from Kafka topics into secondary indexes like Elasticsearch or into batch systems such as Hadoop for offline analysis.

## How it works
Kafka Connect includes two types of connectors:

- **Source connector**: Ingests entire databases and streams table updates to Kafka topics. A source connector can also collect metrics from all your application servers and store these in Kafka topics, making the data available for stream processing with low latency.
- **Sink connector**: Delivers data from Kafka topics into secondary indexes such as Elasticsearch, or batch systems such as Hadoop for offline analysis.


## Standalone vs. Distributed Mode
**Standalone mode** is useful for development and testing Kafka Connect on a local machine. It can also be used for environments that typically use single agents (for example, sending web server logs to Kafka).

**Distributed mode** runs Connect workers on multiple machines (nodes). These form a Connect cluster. Kafka Connect distributes running connectors across the cluster. You can add more nodes or remove nodes as your needs evolve.

Distributed mode is also more fault tolerant. If a node unexpectedly leaves the cluster, Kafka Connect automatically distributes the work of that node to other nodes in the cluster. And, because Kafka Connect stores connector configurations, status, and offset information inside the Kafka cluster where it is safely replicated, losing the node where a Connect worker runs does not result in any lost data.

## Connectors
Connectors in Kafka Connect define where data should be copied to and from. A **connector instance** is a logical job that is responsible for managing the copying of data between Kafka and another system. All of the classes that implement or are used by a connector are defined in a **connector plugin**.

## Tasks
Tasks are the main actor in the data model for Connect. Each connector instance coordinates a set of **tasks** that actually copy the data. By allowing the connector to break a single job into many tasks, Kafka Connect provides built-in support for parallelism and scalable data copying with very little configuration. These tasks have no state stored within them. Task state is stored in Kafka in special topics `config.storage.topic` and `status.storage.topic` and managed by the associated connector. As such, tasks may be started, stopped, or restarted at any time in order to provide a resilient, scalable data pipeline.
<p align="center">
    <img src="images/data-model-simple.png" alt="High level representation of data passing through a Connect source task into Kafka. Note that internal offsets are stored either in Kafka or on disk rather than within the task itself." />
</p>

## Workers
Connectors and tasks are logical units of work and must be scheduled to execute in a process. Kafka Connect calls these processes **workers** and has two types of workers: standalone and distributed.

### Standalone Workers
Standalone mode is the simplest mode, where a single process is responsible for executing all connectors and tasks.

Since it is a single process, it requires minimal configuration. Standalone mode is convenient for getting started, during development, and in certain situations where only one process makes sense, such as collecting logs from a host. However, because there is only a single process, it also has more limited functionality: scalability is limited to the single process and there is no fault tolerance beyond any monitoring you add to the single process.

### Distributed Workers
Distributed mode provides scalability and automatic fault tolerance for Kafka Connect. In distributed mode, you start many worker processes using the same `group.id` and they automatically coordinate to schedule execution of connectors and tasks across all available workers. If you add a worker, shut down a worker, or a worker fails unexpectedly, the rest of the workers detect this and automatically coordinate to redistribute connectors and tasks across the updated set of available workers. Note the similarity to consumer group rebalance. Under the covers, connect workers are using consumer groups to coordinate and rebalance.

All workers with the same `group.id` will be in the same connect cluster. For example, if worker-a has `group.id=connect-cluster-a` and worker-b has the same `group.id`, worker-a and worker-b will form a cluster called `connect-cluster-a`.
<p align="center">
    <img src="images/worker-model-basics.png" alt="A three-node Kafka Connect distributed mode cluster. Connectors (monitoring the source or sink system for changes that require reconfiguring tasks) and tasks (copying a subset of a connector’s data) are automatically balanced across the active workers. The division of work between tasks is shown by the partitions that each task is assigned." />
</p>

## Converters
Converters are necessary to have a Kafka Connect deployment support a particular data format when writing to or reading from Kafka. Tasks use converters to change the format of data from bytes to a Connect internal data format and vice versa.

By default, Confluent Platform provides the following converters:

- **AvroConverter** io.confluent.connect.avro.AvroConverter: use with Schema Registry
- **ProtobufConverter** io.confluent.connect.protobuf.ProtobufConverter: use with Schema Registry
- **JsonSchemaConverter** io.confluent.connect.json.JsonSchemaConverter: use with Schema Registry
- **JsonConverter** org.apache.kafka.connect.json.JsonConverter (without Schema Registry): use with structured data
- **StringConverter** org.apache.kafka.connect.storage.StringConverter: simple string format
- **ByteArrayConverter** org.apache.kafka.connect.converters.ByteArrayConverter: provides a “pass-through” option that does no conversion

Converters are decoupled from connectors themselves to allow for reuse of converters between connectors naturally. For example, using the same Avro converter, the JDBC Source Connector can write Avro data to Kafka and the HDFS Sink Connector can read Avro data from Kafka. This means the same converter can be used even though, for example, the JDBC source returns a `ResultSet` that is eventually written to HDFS as a parquet file.

<p align="center">
    <img src="images/converter-basics.png" alt="The graphic shows how converters are used when reading from a database using a JDBC Source Connector, writing to Kafka, and finally, writing to HDFS with an HDFS Sink Connector." />
</p>

## Transforms
Connectors can be configured with transformations to make simple and lightweight modifications to individual messages. This can be convenient for minor data adjustments and event routing, and multiple transformations can be chained together in the connector configuration. However, more complex transformations and operations that apply to multiple messages are best implemented with ksqlDB and Kafka Streams.

A transform is a simple function that accepts one record as an input and outputs a modified record. All transforms provided by Kafka Connect perform simple but commonly useful modifications.

When transforms are used with a source connector, Kafka Connect passes each source record produced by the connector through the first transformation, which makes its modifications and outputs a new source record. This updated source record is then passed to the next transform in the chain, which generates a new modified source record. This continues for the remaining transforms. The final updated source record is converted to the binary form and written to Kafka.

Transforms can also be used with sink connectors. Kafka Connect reads message from Kafka and converts the binary representation to a sink record. If there is a transform, Kafka Connect passes the record through the first transformation, which makes its modifications and outputs a new, updated sink record. The updated sink record is then passed through the next transform in the chain, which generates a new sink record. This continues for the remaining transforms, and the final updated sink record is then passed to the sink connector for processing.


## Dead Letter Queue
An invalid record may occur for a number of reasons. One example is when a record arrives at the sink connector serialized in JSON format, but the sink connector configuration is expecting Avro format. When an invalid record cannot be processed by a sink connector, the error is handled based on the connector configuration property `errors.tolerance`.

Dead letter queues are only applicable for sink connectors.

There are two valid values for this configuration property: `none` (default) or `all`.

When `errors.tolerance` is set to `none` an error or invalid record causes the connector task to immediately fail and the connector goes into a failed state. To resolve this issue, you would need to review the Kafka Connect Worker log to find out what caused the failure, correct it, and restart the connector.

When `errors.tolerance` is set to `all`, all errors or invalid records are ignored and processing continues. No errors are written to the Connect Worker log. To determine if records are failing you must use internal metrics or count the number of records at the source and compare that with the number of records processed.

An error-handling feature is available that will route all invalid records to a special topic and report the error. This topic contains a **dead letter queue** of records that could not be processed by the sink connector.

An example GCS sink connector configuration with dead letter queueing enabled is shown below:
```json
 {
  "name": "gcs-sink-01",
  "config": {
    "connector.class": "io.confluent.connect.gcs.GcsSinkConnector",
    "tasks.max": "1",
    "topics": "gcs_topic",
    "gcs.bucket.name": "<my-gcs-bucket>",
    "gcs.part.size": "5242880",
    "flush.size": "3",
    "storage.class": "io.confluent.connect.gcs.storage.GcsStorage",
    "format.class": "io.confluent.connect.gcs.format.avro.AvroFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://localhost:8081",
    "schema.compatibility": "NONE",
    "confluent.topic.bootstrap.servers": "localhost:9092",
    "confluent.topic.replication.factor": "1",
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "dlq-gcs-sink-01"
  }
}
```
Even if the dead letter topic contains the records that failed, it does not show why. You can add the following additional configuration property to include failed record header information.
```text
errors.deadletterqueue.context.headers.enable = true
```

## Referencies
- [Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html)
