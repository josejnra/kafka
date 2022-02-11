import click

from commands.broker import kafka


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """
        Cli commands for kafka services
    """


cli.add_command(kafka)


if __name__ == '__main__':
    cli()
