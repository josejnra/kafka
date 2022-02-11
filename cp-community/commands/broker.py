import json
import random
from uuid import uuid1


import click
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient


CONF = {
    "bootstrap.servers": "localhost:9092,localhost:9192"
}


@click.group()
def kafka():
    """
        Commands on kafka brokers
    """


@kafka.command()
@click.option("--topic-name", "-t", help="Topic name to describe.")
def list_topics(topic_name: str):
    """
        List topics
    """
    kadmin = AdminClient(CONF)
    for topic in kadmin.list_topics(topic=topic_name).topics:
        click.echo(topic)


@kafka.command()
@click.option("--topic-name", "-t", help="Topic name to describe.", required=True)
def describe_topic(topic_name: str):
    """
        Describe topic
    """
    kadmin = AdminClient(CONF)

    for key, value in kadmin.list_topics(topic=topic_name).topics.items():
        click.echo(f"{key} {value}")
        for k, v in value.partitions.items():
            click.echo(f"{k} Partition id : {v} leader : {v.leader}  replica: {v.replicas}")


@click.group()
def consumer():
    """
        Commands to consume messages
    """


kafka.add_command(consumer)


@consumer.command()
@click.option("--topic-name", "-t", help="Topic name to consume messages.", required=True)
@click.option("--offset", "-o",
              type=click.Choice(['earliest', 'latest']),
              default="latest",
              help="Offset type.",
              show_default=True)
@click.option("--group-id", "-g", default="mygroup", help="Group id.", show_default=True)
def consume_messages(topic_name: str, offset: str, group_id: str):
    consumer_config = {
            "group.id": group_id,
            "auto.offset.reset": offset,
        }

    consumer_config.update(**CONF)
    consumer = Consumer(consumer_config)

    consumer.subscribe([topic_name])
    for msg in consume(consumer, 1.0):
        click.echo(msg.topic())
        click.echo(msg.partition())
        click.echo(msg.offset())
        click.echo(msg.key().decode('utf-8'))
        click.echo(msg.value().decode('utf-8'))


def consume(consumer: Consumer, timeout):
    try:
        while True:
            message = consumer.poll(timeout)
            if message is None:
                continue
            if message.error():
                click.echo("Consumer error: {}".format(message.error()))
                continue
            yield message
    except Exception as e:
        click.echo(e)
    finally:
        consumer.close()


@click.group()
def producer():
    """
        Commands to produce messages
    """


kafka.add_command(producer)


@producer.command()
@click.option("--topic-name", "-t", help="Topic name send messages.", required=True)
@click.option("--count", "-c", default=10, help="Number of messages to produce.", show_default=True)
def users(topic_name: str, count: int):
    send_message(topic_name, "user", count)


@producer.command()
@click.option("--topic-name", "-t", help="Topic name to send messages.", required=True)
@click.option("--count", "-c", default=10, help="Number of messages to produce.", show_default=True)
def locations(topic_name: str, count: int):
    send_message(topic_name, "location", count)


def send_message(topic_name: str, message_type: str, count: int):
    producer = Producer(CONF)
    for msg in get_message_generator(message_type, count):
        producer.produce(
            topic=topic_name,
            key=str(uuid1(random.randint(1, 10000))),
            value=msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
    producer.flush()


def get_message_generator(message_type: str, size: int):
    generator = {
        "user": user_messsage(size),
        "location": location_messsage(size)
    }.get(message_type)

    if not generator:
        raise KeyError('There is no such message generator:', message_type)

    return generator


def delivery_report(err, decoded_message, original_message):
    if err is not None:
        click.echo(err)


def user_messsage(count: int) -> bytes:
    for _ in range(count):
        yield json.dumps({
            "nome": random.choice(["john", "alex", "jack", "whindersson"]),
            "id": random.randint(1, 1000)
        }).encode('utf-8')


def location_messsage(count: int) -> bytes:
    for _ in range(count):
        yield json.dumps({
            "profileId": str(uuid1(random.randint(1, 10000))),
            "latitude": random.uniform(-14, -20),
            "longitude": random.uniform(-40, -50)
        }).encode('utf-8')
