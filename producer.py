import json
import random
from uuid import uuid1

from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:29092'})


def user_messsage(size: int) -> bytes:
    for _ in range(size):
        yield json.dumps({
            "nome": random.choice(["john", "alex", "jack", "whindersson"]),
            "id": random.randint(1, 1000)
        }).encode('utf-8')


def location_messsage(size: int) -> bytes:
    for _ in range(size):
        yield json.dumps({
            "profileId": str(uuid1(random.randint(1, 10000))),
            "latitude": random.uniform(-14, -20),
            "longitude": random.uniform(-40, -50)
        }).encode('utf-8')


def get_message_generator(topic_name: str, size: int):
    generator = {
        "users": user_messsage(size),
        "locations": location_messsage(size)
    }.get(topic_name)

    if not generator:
        raise KeyError('There is no such message generator:', topic_name)

    return generator


def delivery_report(err, decoded_message, original_message):
    if err is not None:
        print(err)


def confluent_producer_async(topic_name: str, size: int = 1000000):
    for msg in get_message_generator(topic_name, size):
        producer.produce(
            topic=topic_name,
            key=str(uuid1(random.randint(1, 10000))),
            value=msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
    producer.flush()


def confluent_producer_sync(topic_name: str, size: int = 1000000):
    for msg in get_message_generator(topic_name, size):
        producer.produce(
            topic=topic_name,
            key=str(uuid1(random.randint(1, 10000))),
            value=msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
        producer.flush()


if __name__ == '__main__':
    confluent_producer_sync('locations', 10000)
