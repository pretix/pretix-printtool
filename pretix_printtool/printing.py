import sys
from tempfile import NamedTemporaryFile

import click
import cups
import requests
import time
from requests import RequestException

from .config import get_endpoint


def print_queue(config):
    click.echo('Connecting to CUPS...')
    conn = cups.Connection()

    while True:
        click.echo('Downloading next PDF from pretix...')
        try:
            r = requests.get(get_endpoint(config) + 'poll/?status=new&method=ship&method=collect', headers={
                'Authorization': 'Token {}'.format(config['pretix']['key'])
            })
        except (RequestException, OSError) as e:
            click.echo(click.style('Connection error: %s' % str(e), fg='red'))
            sys.exit(2)
        except ValueError as e:
            click.echo(click.style('Could not read response: %s' % str(e), fg='red'))
            sys.exit(2)
        if r.status_code == 204:
            click.echo(click.style('No more orders available.', fg='green'))
            sys.exit(0)
        elif r.status_code != 200:
            click.echo(click.style('Invalid response code: %d' % r.status_code, fg='red'))
            sys.exit(3)

        ordercode = r.headers['X-Pretix-Order-Code']
        with NamedTemporaryFile() as pdf:
            pdf.write(r.content)
            pdf.flush()

            click.echo(click.style('Sending print job…', fg='green'))
            jobid = conn.printFile(config['cups']['queue'], pdf.name, "pretix Ticket", {})

        while True:
            a = conn.getJobAttributes(jobid)

            if a['job-state'] == cups.IPP_JOB_ABORTED:
                click.echo(click.style('Print job was aborted!', fg='red'))
                sys.exit(4)
            elif a['job-state'] == cups.IPP_JOB_CANCELED:
                click.echo(click.style('Print job was canceled!', fg='red'))
                sys.exit(4)
            elif a['job-state'] == cups.IPP_JOB_COMPLETED:
                click.echo(click.style('Print job was completed!', fg='green'))
                break
            elif a['job-state'] == cups.IPP_JOB_HELD:
                click.echo(click.style('Print job is on hold!', fg='red'))
                sys.exit(4)
            elif a['job-state'] == cups.IPP_JOB_PENDING:
                click.echo(click.style('Print job is pending…', fg='yellow'))
            elif a['job-state'] == cups.IPP_JOB_PROCESSING:
                pass
            elif a['job-state'] == cups.IPP_JOB_STOPPED:
                click.echo(click.style('Print job is stopped!', fg='red'))
                sys.exit(4)

            time.sleep(0.5)

        click.echo(click.style('Printed!', fg='green'))
        click.echo('Marking as sent…')

        try:
            r = requests.post(get_endpoint(config) + ordercode + '/ack/', headers={
                'Authorization': 'Token {}'.format(config['pretix']['key'])
            })
        except (RequestException, OSError) as e:
            click.echo(click.style('Connection error: %s' % str(e), fg='red'))
            sys.exit(2)
        except ValueError as e:
            click.echo(click.style('Could not read response: %s' % str(e), fg='red'))
            sys.exit(2)
        if r.status_code == 204:
            click.echo(click.style('Order marked as sent.', fg='green'))
        elif r.status_code != 200:
            click.echo(click.style('Invalid response code: %d' % r.status_code, fg='red'))
            sys.exit(3)
