import sys
from urllib.parse import urljoin

import click


def validate_config(config):
    validate_pretix_config(config)
    if 'printtool' not in config:
        click.echo(click.style('Invalid config file: Does not contain printtool section', fg='red'))
        sys.exit(1)
    if 'type' not in config['printtool']:
        click.echo(click.style('Invalid config file: Does not contain print server type', fg='red'))
        sys.exit(1)
    if config['printtool']['type'] == 'cups':
        validate_cups_config(config)
    else:
        click.echo(click.style('Invalid config file: Unknown type %s' % config['printtool']['type'], fg='red'))
        sys.exit(1)


def validate_cups_config(config):
    if 'cups' not in config:
        click.echo(click.style('Invalid config file: Does not contain cups section', fg='red'))
        sys.exit(1)

    for f in ('queue',):
        if f not in config['cups']:
            click.echo(click.style('Invalid config file: Does not contain value for cups.%s' % f, fg='red'))
            sys.exit(1)


def validate_pretix_config(config):
    if 'pretix' not in config:
        click.echo(click.style('Invalid config file: Does not contain pretix section', fg='red'))
        sys.exit(1)

    for f in ('organizer', 'server', 'key'):
        if f not in config['pretix']:
            click.echo(click.style('Invalid config file: Does not contain value for pretix.%s' % f, fg='red'))
            sys.exit(1)


def get_endpoint(config):
    return urljoin(
        config['pretix']['server'],
        '/api/v1/organizers/{}/printjobs/'.format(config['pretix']['organizer'])
    )
