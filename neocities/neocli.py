#!/usr/bin/env python
import neocities
import requests
import os
import click
from tabulate import tabulate
import shutil

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"], token_normalize_func=lambda x: x.lower()
)

supExt = [
    ".html",
    ".htm",
    ".jpg",
    ".png",
    ".gif",
    ".svg",
    ".ico",
    ".md",
    ".markdown",
    ".js",
    ".json",
    ".geojson",
    ".css",
    ".txt",
    ".text",
    ".csv",
    ".tsv",
    ".xml",
    ".eot",
    ".ttf",
    ".woff",
    ".woff2",
    ".mid",
    ".midi",
]


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.argument("site", required=False)
def info(site):
    """Display information about a NeoCities site."""
    if site:
        site = site.rstrip(".neocities.org")
        response = nc.info(site)
    else:
        response = nc.info()
    if "info" in response:
        response = response["info"]
    else:
        print(response)
        return
    rows = [[key, response[key]] for key in response]
    table = tabulate(rows)
    print(table)


@cli.command()
@click.argument("source", required=True, type=click.File("rb"))
@click.argument("destination", required=False)
def upload(source, destination):
    """Upload one or more files to a NeoCities site.
    Source refers to a local file.
    Destination refers to the remote file name and location.
    """
    if destination and "." not in destination:
        click.echo("Invalid target; specify a target path file extension.")
        return 1
    nc.upload((source.name, destination if destination else source.name))


@cli.command()
@click.argument("filenames", required=True, nargs=-1)
def delete(filenames):
    """Delete one or more files from a NeoCities site."""
    nc.delete(filenames)


@cli.command()
@click.argument("site", required=False)
def list(site):
    """List files of a NeoCities site."""
    if site:
        site = site.rstrip(".neocities.org")
        response = nc.listitems(site)
    else:
        response = nc.listitems()

    if "files" in response:
        files = response["files"]
    else:
        print(response)
        return
    table = tabulate(files, "keys")

    print(table)


@cli.command()
@click.argument("dirc", required=True)
def push(dirc):
    """Push recursively directory to NeoCities site"""
    files = []
    for root, dirs, dirfiles, in os.walk(dirc):
        for name in dirfiles:
            files.append((os.path.join(root, name),
                          os.path.relpath(os.path.join(root, name), dirc)))
    for filename, dest in files:
        if os.path.splitext(filename)[1].lower() in supExt:
            nc.upload((filename, dest))


def main():
    username = os.environ.get("NEOCITIES_USER")
    password = os.environ.get("NEOCITIES_PASS")
    api_key = os.environ.get("NEOCITIES_API_KEY")
    global nc
    nc = neocities.NeoCities(username, password, api_key)
    cli(obj={})


if __name__ == "__main__":
    main()
