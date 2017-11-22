import configparser
from urllib.parse import urljoin

import click
import cups

from .config import validate_config
from .testing import test_cups, test_pretix
from .printing import print_queue


@click.group()
def main():
    pass


@main.command()
@click.argument('configfile', type=click.Path(exists=True))
@click.option('--printer/--no-printer', default=True, help='Test printer connection')
@click.option('--pretix/--no-pretix', default=True, help='Test pretix connection')
def test(configfile, printer, pretix):
    config = configparser.ConfigParser()
    config.read(configfile)
    validate_config(config)
    if config['printtool']['type'] == 'cups' and printer:
        test_cups(config)
    if pretix:
        test_pretix(config)


@main.command(name='print')
@click.argument('configfile', type=click.Path(exists=True))
def c_print(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    validate_config(config)
    print_queue(config)


@main.command()
@click.option('--type', type=click.Choice(['cups']), default='cups')
def setup(type):
    click.echo(click.style('Welcome to the pretix-printtool setup!', fg='green'))

    if type == 'cups':
        click.echo('You will now be prompted all information required to setup your printer via CUPS.')
        click.echo('')
        click.echo(click.style('Printer settings', fg='blue'))

        conn = cups.Connection()
        qnames = list(conn.getPrinters().keys())
        click.echo('The following print queues are installed on your system:')
        for q in qnames:
            click.echo(' - ' + q)

        printqueue = click.prompt('Print queue name', type=click.Choice(qnames))

    click.echo('')
    click.echo(click.style('pretix information', fg='blue'))
    api_server = click.prompt('pretix Server', default='https://pretix.eu/')
    api_organizer = click.prompt('Short name of your organizer account', type=click.STRING)
    click.echo('You will now need an API key. If you do not have one yet, you can create one as part of a team here:')
    click.echo(urljoin(api_server, '/control/organizer/{}/teams'.format(api_organizer)))
    click.echo('The key needs to created for a team with the permissions "can view orders" and "can change orders" '
               'for all events that you want to print orders for.')
    api_key = click.prompt('API key')

    click.echo('')
    click.echo(click.style('Other information', fg='blue'))
    filename = click.prompt('Configuration file', default=api_organizer + '.cfg', type=click.Path(exists=False))

    config = configparser.ConfigParser()
    config['printtool'] = {
        'type': type
    }
    if type == 'cups':
        config['cups'] = {
            'queue': printqueue
        }
    config['pretix'] = {
        'server': api_server,
        'organizer': api_organizer,
        'key': api_key
    }
    with open(filename, 'w') as configfile:
        config.write(configfile)

    click.echo('')
    click.echo(click.style('Configuration file created!', fg='green'))
    click.echo('')
    click.echo('You can now run')
    click.echo('    pretix-printtool test %s' % filename)
    click.echo('to test the connection.')
