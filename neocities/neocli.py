#!/usr/bin/env python
import neocities
import sys
import os
import requests
import click
from tabulate import tabulate


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda x: x.lower()
    )

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.argument('site', required=False)
def info(site):
    """Display information about a NeoCities site."""
    if site:
        site = site.rstrip('.neocities.org')
        response = nc.info(site)
    else:
        response = nc.info()
    if 'info' in response:
        response = response['info']
    else:
        print(response)
        return
    rows = [[key, response[key]] for key in response]
    table = tabulate(rows)
    print(table)


@cli.command()
@click.argument('source', required=True, type=click.File('rb'))
@click.argument('destination', required=False)
def upload(source, destination):
    """Upload one or more files to a NeoCities site.
    Source refers to a local file.
    Destination refers to the remote file name and location.
    """
    if not '.' in destination:
        click.echo("Invalid target; please specify a file extension for the target path.")
        return 1
    nc.upload((source.name, destination if destination else source.name))

@cli.command()
@click.argument('filenames', required=True, nargs=-1)
def delete(filenames):
    """Delete one or more files from a NeoCities site."""
    nc.delete(filenames)

@cli.command()
@click.argument('site', required=False)
def list(site):
    """List files of a NeoCities site."""
    if site:
        site = site.rstrip('.neocities.org')
        response = nc.listitems(site)
    else:
        response = nc.listitems()

    if 'files' in response:
        files = response['files']
    else:
        print(response)
        return
    headers = files[0].keys()
    table = tabulate(files, "keys")

    print(table)


def main():
    username = os.environ["NEOCITIES_USER"]
    password = os.environ["NEOCITIES_PASS"]
    nc = neocities.NeoCities(username, password)
    cli(obj={})

if __name__ == "__main__":
    main()

