from confluent_kafka import Consumer, TopicPartition


consumer = Consumer(
    {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest',
    }
)


def consume_session_window(consumer, timeout=1, session_max=5):
    session = 0
    try:
        while True:
            message = consumer.poll(timeout)
            if message is None:
                session += 1
                if session > session_max:
                    break
                continue
            if message.error():
                print("Consumer error: {}".format(message.error()))
                continue
            yield message
    except Exception as e:
        print(e)
    finally:
        consumer.close()


def consume(consumer, timeout):
    try:
        while True:
            message = consumer.poll(timeout)
            if message is None:
                continue
            if message.error():
                print("Consumer error: {}".format(message.error()))
                continue
            yield message
    except Exception as e:
        print(e)
    finally:
        consumer.close()


def confluent_consumer(topic_name: str):
    consumer.subscribe([topic_name])
    for msg in consume(consumer, 1.0):
        print(msg.topic())
        print(msg.partition())
        print(msg.offset())
        print(msg.key().decode('utf-8'))
        print(msg.value().decode('utf-8'))


def confluent_consumer_partition(topic_name: str):
    consumer.assign([TopicPartition(topic_name, 0)])
    for msg in consume(consumer, 1.0):
        print(msg.topic())
        print(msg.partition())
        print(msg.offset())
        print(msg.key().decode('utf-8'))
        print(msg.value().decode('utf-8'))


if __name__ == '__main__':
    confluent_consumer("locations")
