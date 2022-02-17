import json
from pprint import pprint

import click
import requests
from http.client import HTTPConnection
HTTPConnection._http_vsn_str = "HTTP/1.1"

ksqldb_url = "http://localhost:8088/"
header = {
    "Accept": "application/vnd.ksql.v1+json",
    "Content-Type": "application/vnd.ksql.v1+json"
}


@click.group()
def ksqldb():
    """
        Commands to run against ksqlDB server
    """


@ksqldb.command()
def info():
    """
        Server status

        Example:
            query info
    """
    response = requests.get(url=ksqldb_url + "info", headers=header)
    click.echo(pprint(json.loads(response.text)))


@ksqldb.command()
def list_streams():
    """
        List streams

        Example:
            query list-streams
    """
    body = {
        "ksql": "LIST STREAMS;",
        "streamsProperties": {}
    }
    response = requests.post(url=ksqldb_url + "ksql", json=body, headers=header)
    click.echo(pprint(json.loads(response.text)))


@ksqldb.command()
@click.option("--statement", "-s", help="Query statement.", required=True)
@click.option("--streams-properties", "-p", type=dict, default={}, help="Streams properties.", show_default=True)
def query(statement: str, streams_properties: dict):
    """
        Query an existing stream

        Example:
            query -s "SELECT * FROM users EMIT CHANGES;"
    """
    body = {
        "ksql": statement,
        "streamsProperties": streams_properties
    }
    response = requests.post(url=ksqldb_url + "query", json=body, headers=header)
    click.echo(pprint(json.loads(response.text)))
