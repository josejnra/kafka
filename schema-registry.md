# Schema Registry
Confluent Schema Registry provides a serving layer for metadata. It provides a RESTful interface for storing and retrieving Avro, JSON Schema, and Protobuf schemas. It stores a versioned history of all schemas based on a specified subject name strategy, provides multiple compatibility settings and allows evolution of schemas according to the configured compatibility settings and expanded support for these schema types. It provides serializers that plug into Apache Kafka® clients that handle schema storage and retrieval for Kafka messages that are sent in any of the supported formats.

Schema Registry lives outside of and separately from Kafka brokers. Producers and consumers still talk to Kafka to publish and read data (messages) to topics. Concurrently, they can also talk to Schema Registry to send and retrieve schemas that describe the data models for the messages.

<p align="center">
    <img src="images/schema-registry-and-kafka.png" alt="Confluent Schema Registry for storing and retrieving schemas" />
</p>
Schema Registry is a distributed storage layer for schemas which uses Kafka as its underlying storage mechanism. Some key design decisions:
- Assigns globally unique ID to each registered schema. Allocated IDs are guaranteed to be monotonically increasing and unique, but not necessarily consecutive.
- Kafka provides the durable backend, and functions as a write-ahead changelog for the state of Schema Registry and the schemas it contains.
- Schema Registry is designed to be distributed, with single-primary architecture, and ZooKeeper/Kafka coordinates primary election (based on the configuration).

An alternative to confluent schema registry is [Karapace](https://aiven.io/blog/aiven-launches-karapace-for-kafka-schema-and-cluster-management#:~:text=Open%20mic-,Aiven%20launches%20Karapace%20for%20Kafka%20Schema%20and%20cluster%20management,Schema%20Registry%20and%20Kafka%20REST). An open source solution.
## Schemas, Subjects, and Topics
A Kafka topic contains messages, and each message is a key-value pair. Either the message key or the message value, or both, can be serialized as Avro, JSON, or Protobuf. A schema defines the structure of the data format. The Kafka topic name can be independent of the schema name. Schema Registry defines a scope in which schemas can evolve, and that scope is the subject. The name of the subject depends on the configured subject name strategy, which by default is set to derive subject name from topic name.

## Supported Formats
The following schema formats are supported out-of-the box with Confluent Platform, with serializers, deserializers, and command line tools available for each format:

| **Format**      | **Producer**                                                        | **Consumer**                                                          |
|-------------|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Avro        | io.confluent.kafka.serializers.KafkaAvroSerializer              | io.confluent.kafka.serializers.KafkaAvroDeserializer              |
| ProtoBuf    | io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer | io.confluent.kafka.serializers.protobuf.KafkaProtobufDeserializer |
| JSON Schema | io.confluent.kafka.serializers.json.KafkaJsonSchemaSerializer   | io.confluent.kafka.serializers.json.KafkaJsonSchemaDeserializer   |

## Referencies
- [Schema Registry Overview](https://docs.confluent.io/platform/current/schema-registry/index.html)
