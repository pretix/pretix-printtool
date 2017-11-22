import click
import cups
import requests
from requests import RequestException

from .config import get_endpoint


def test_cups(config):
    click.echo('Connecting to CUPS...')
    conn = cups.Connection()

    click.echo('Fetching printer list...')
    p = conn.getPrinters()

    click.echo('Looking for correct queue...')
    printername = config['cups']['queue']
    if printername not in p:
        click.echo(click.style('Printer not found: %s' % printername, fg='red'))
    else:
        printer = p[printername]
        state = {
            cups.IPP_PRINTER_BUSY: ('busy', 'yellow'),
            cups.IPP_PRINTER_IDLE: ('idle', 'green'),
            cups.IPP_PRINTER_IS_DEACTIVATED: ('deactivated', 'red'),
            cups.IPP_PRINTER_PROCESSING: ('processing', 'yellow'),
            cups.IPP_PRINTER_STOPPED: ('stopped', 'red'),
        }
        click.echo(click.style(
            'Printer state: %s' % state[printer['printer-state']][0],
            fg=state[printer['printer-state']][1]
        ))


def test_pretix(config):
    click.echo('Testing pretix connection...')
    try:
        r = requests.get(get_endpoint(config), headers={
            'Authorization': 'Token {}'.format(config['pretix']['key'])
        })
        if 'results' in r.json():
            click.echo(click.style('Connection successful.', fg='green'))
        else:
            click.echo(click.style('Could not read response: %s' % str(r.text), fg='red'))
    except (RequestException, OSError) as e:
        click.echo(click.style('Connection error: %s' % str(e), fg='red'))
    except ValueError as e:
        click.echo(click.style('Could not read response: %s' % str(e), fg='red'))
