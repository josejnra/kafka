import click

from commands.broker import kafka
from commands.ksqldb import ksqldb
from commands.rest import rest_proxy


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """
        Cli commands for kafka services
    """


cli.add_command(kafka)
cli.add_command(ksqldb)
cli.add_command(rest_proxy)


if __name__ == '__main__':
    cli()
