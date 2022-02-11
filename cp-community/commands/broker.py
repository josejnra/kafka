import click
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
