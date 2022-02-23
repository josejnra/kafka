import json
from pprint import pprint

import click
import requests
from http.client import HTTPConnection
HTTPConnection._http_vsn_str = "HTTP/1.1"

rest_proxy_url = "http://localhost:8082/"
header = {
    "Content-Type": "application/json"
}


@click.group()
def rest_proxy():
    """
        Commands to run against kafka rest proxy
    """


@rest_proxy.command()
def get_clusters():
    """
        Get kafka clusters

        Example:
            rest-proxy list-clusters
    """
    response = requests.get(url=rest_proxy_url + "v3/clusters", headers=header)
    click.echo(pprint(json.loads(response.text)))


@rest_proxy.command()
@click.option("--cluster-id", "-i", help="Cluster ID.", required=True)
@click.option("--topic-name", "-t", type=str, help="Topic name.", required=True)
@click.option("--num-partitions", "-n", type=int, default=2, help="Number of partitions.", show_default=True)
@click.option("--configs", "-c", type=list, default=[], help="Other configs.", show_default=True)
def create_topic(cluster_id: str, topic_name: str, num_partitions: int, configs: list):
    """
        Create topic

        Example:
            rest-proxy create-topic -i N-Py2kKRR1KwpMk4lRHQ0A -t users
    """
    body = {
        "topic_name": topic_name,
        "partitions_count": num_partitions,
        "configs": configs
    }
    response = requests.post(url=rest_proxy_url + f"v3/clusters/{cluster_id}/topics", headers=header, json=body)
    click.echo(pprint(json.loads(response.text)))


@rest_proxy.command()
@click.option("--topic-name", "-t", type=str, help="Topic name.", required=True)
def produce(topic_name: str):
    """
        Send message

        Example:
            rest-proxy produce
    """
    head = {
        "Accept": "application/vnd.kafka.v2+json",
        "Content-Type": "application/vnd.kafka.json.v2+json"
    }
    body = {"records": [{"key": "alice", "value": {"count": 0}},
                        {"key": "alice", "value": {"count": 1}},
                        {"key": "alice", "value": {"count": 2}}]}

    response = requests.post(url=rest_proxy_url + f"topics/{topic_name}", json=body, headers=head)
    click.echo(pprint(json.loads(response.text)))
